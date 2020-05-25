import random
import time
from threading import Thread
import redis
from menu import Menu
class Worker(Thread):

    def __init__(self, delay):
        Thread.__init__(self)
        self.loop = True
        self.r = redis.Redis(charset="utf-8", decode_responses=True)
        self.delay = delay

    def run(self):
        while self.loop:
            mess = self.r.brpop("queue:")
            if mess:
                mess_id = int(mess[1])

                self.r.hmset(f"mess:{mess_id}", {
                    'status': 'checking'
                })
                mess = self.r.hmget(f"mess:{mess_id}", ["writer_id", "receiver_id"])
                writer_id = int(mess[0])
                receiver_id = int(mess[1])
                self.r.hincrby(f"user:{writer_id}", "queue", -1)
                self.r.hincrby(f"user:{writer_id}", "checking", 1)
                time.sleep(self.delay)
                is_spam = random.random() > 0.6
                pipel = self.r.pipeline(True)
                pipel.hincrby(f"user:{writer_id}", "checking", -1)
                if is_spam:
                    sender_username = self.r.hmget(f"user:{writer_id}", 'login')[0]
                    pipel.zincrby("spam:", 1, f"user:{sender_username}")
                    pipel.hmset(f"mess:{mess_id}", {
                        'status': 'blocked'
                    })
                    pipel.hincrby(f"user:{writer_id}", "blocked", 1)
                    pipel.publish('spam', f"User {sender_username} sent spam mess: \"%s\"" %
                                     self.r.hmget("mess:%s" % mess_id, ["text"])[0])
                    print(f"User {sender_username} sent spam mess: \"%s\"" % self.r.hmget("mess:%s" % mess_id, ["text"])[0])
                else:
                    pipel.hmset(f"mess:{mess_id}", {
                        'status': 'sent'
                    })
                    pipel.hincrby(f"user:{writer_id}", "sent", 1)
                    pipel.sadd(f"sent to:{receiver_id}", mess_id)
                pipel.execute()

    def stop(self):
        self.loop = False


if __name__ == '__main__':
    try:
        loop = True
        workers_count = 5
        workers = []
        for i in range(workers_count):
            workr = Worker(random.randint(0, 3))
            workr.setDaemon(True)
            workers.append(workr)
            workr.start()
        while True:
            pass
    except Exception as e:
        Menu.display_error(str(e))
