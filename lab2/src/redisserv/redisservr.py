import redis
import datetime
import logging
import colorama
colorama.init()

logging.basicConfig(filename="./events.log", level=logging.INFO)


class RedisServ(object):
    def __init__(self):
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)

    def registr(self, user_name):
        if self.__r.hget('users:', user_name):
            raise Exception(f"\n Unfortunately, username\n \'{user_name}\' already taken.\n Please, try another)")
        user_id = self.__r.incr('user:id:')
        pipel = self.__r.pipeline(True)
        pipel.hset('users:', user_name, user_id)
        pipel.hmset(f"user:{user_id}", {
            'login': user_name,
            'id': user_id,
            'queue': 0,
            'checking': 0,
            'blocked': 0,
            'sent': 0,
            'delivered': 0
        })
        pipel.execute()
        logging.info(f"User {user_name} registered at {datetime.datetime.now()} \n")
        return user_id

    def sgn_in(self, user_name):
        user_id = self.__r.hget("users:", user_name)

        if not user_id:
            raise Exception(f"User {user_name} does not exist ")

        self.__r.sadd("online:", user_name)
        logging.info(f"User {user_name} logged in at {datetime.datetime.now()} \n")
        self.__r.publish('users', "User %s signed in" % self.__r.hmget(f"user:{user_id}", 'login')[0])
        return int(user_id)

    def sgn_out(self, user_id) -> int:
        logging.info(f"User '{user_id}' signed out at {datetime.datetime.now()} \n")
        self.__r.publish('users', "User '%s' signed out" % self.__r.hmget(f"user:{user_id}", 'login')[0])
        return self.__r.srem("online:", self.__r.hmget(f"user:{user_id}", 'login')[0])

    def create_mess(self, message_text, getter, sender_id) -> int:

        message_id = int(self.__r.incr('message:id:'))
        receiver_id = self.__r.hget("users:", getter)

        if not receiver_id:
            raise Exception(f"\n User '{getter}' does not exist!\n You can't send a message")

        pipel = self.__r.pipeline(True)

        pipel.hmset('message:%s' % message_id, {
            'text': message_text,
            'id': message_id,
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'status': "created"
        })
        pipel.lpush("queue:", message_id)
        pipel.hmset('message:%s' % message_id, {
            'status': 'queue'
        })
        pipel.zincrby("sent:", 1, "user:%s" % self.__r.hmget(f"user:{sender_id}", 'login')[0])
        pipel.hincrby(f"user:{sender_id}", "queue", 1)
        pipel.execute()

        return message_id

    def get_mess(self, user_id):
        mess = self.__r.smembers(f"sent to:{user_id}")
        mess_list = []
        for mess_id in mess:
            mess = self.__r.hmget(f"mess:{mess_id}", ["sender_id", "text", "status"])
            sender_id = mess[0]
            mess_list.append("From '%s' - '%s'" % (self.__r.hmget("user:%s" % sender_id, 'login')[0], mess[1]))
            if mess[2] != "delivered":
                pipel = self.__r.pipeline(True)
                pipel.hset(f"mess:{mess_id}", "status", "delivered")
                pipel.hincrby(f"user:{sender_id}", "sent", -1)
                pipel.hincrby(f"user:{sender_id}", "delivered", 1)
                pipel.execute()
        return mess_list

    def get_most_senders(self, most_senders_quantity) -> list:
        return self.__r.zrange("sent:", 0, int(most_senders_quantity) - 1, desc=True, withscores=True)

    def get_most_spamers(self, most_receivers_quantity) -> list:
        return self.__r.zrange("spam:", 0, int(most_receivers_quantity) - 1, desc=True, withscores=True)

    def get_mess_statistics(self, user_id):
        curr_user = self.__r.hmget(f"user:{user_id}", ['queue', 'checking', 'blocked', 'sent', 'delivered'])
        return " [In queue] - %s\n [Checking] -" \
               " %s\n [Blocked] - %s\n [Sent] - %s\n [Delivered] - %s" % \
               tuple(curr_user)

    def get_active_users(self) -> list:
        return self.__r.smembers("online:")

