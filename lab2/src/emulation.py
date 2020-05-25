import random
from threading import Thread
from redisserv.redisservr import RedisServ
from faker import Faker
from entity.admin import AdminController
from menu import Menu


fake = Faker()

def emulation():
    fake = Faker()
    users_num = 5
    users = [fake.profile(fields=['user_name'], sex=None)['user_name'] for u in range(users_num)]
    thrds = []
    try:
        for i in range(users_num):
            thrds.append(EmulationController(users[i], users, users_num, random.randint(100, 5000)))
        for thrd in thrds:
            thrd.start()
        AdminController()
        for thrd in thrds:
            if thrd.is_alive():
                thrd.stop()
    except Exception as e:
        Menu.display_error(str(e))


class EmulationController(Thread):
    def __init__(self, user_name, listing_users, users_num, loop_num):
        Thread.__init__(self)
        self.quant_lp = loop_num
        self.servr = RedisServ()
        self.usrs_listing = listing_users
        self.users_qnt = users_num
        self.servr.registr(user_name)
        self.usr_id = self.servr.sgn_in(user_name)

    def run(self):
        while self.quant_lp > 0:
            mess_text = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
            receiver = self.usrs_listing[random.randint(0, self.users_qnt - 1)]
            self.servr.create_mess(mess_text, receiver, self.usr_id)
            self.quant_lp -= 1

        self.stop()

    def stop(self):
        self.servr.sgn_out(self.usr_id)
        self.quant_lp = 0
