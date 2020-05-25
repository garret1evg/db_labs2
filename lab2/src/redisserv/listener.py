from threading import Thread
import datetime
import logging
import redis

class EventListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.r = redis.Redis(charset="utf-8", decode_responses=True)
        self.evts = []

    def start(self):
        pubsubs = self.r.pubsub()
        pubsubs.subscribe(['users', 'spam'])
        for it in pubsubs.listen():
            if it['type'] == 'mess':
                mess = " %s at '%s'" % (it['data'], datetime.datetime.now())
                self.evts.append(mess)
                logging.info(mess)

    def get_events(self):
        return self.evts
