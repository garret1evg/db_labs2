import colorama
from colorama import Fore
import atexit
from entity.controller import Controller

from menu import Menu
from redisserv.redisservr import RedisServ


class UserController(object):
    def __init__(self):
        self.servr = RedisServ()
        self.menu = 'Main menu'
        self.curr_usr_id = -1
        self.loop = True
        atexit.register(self.sgn_out)
        self.start()

    def start(self):
        from data import menu_listing
        try:
            while self.loop:
                choice = Controller.mkchoice(menu_listing[self.menu].keys(), self.menu)
                Controller.consid_choice(self, choice, list(menu_listing[self.menu].values()))

        except Exception as e:
            Menu.display_error(str(e))

    def registr(self):
        usernm=self.servr.registr(*Controller.get_func_args(self.servr.registr))
        colorama.init()
        print(Fore.GREEN + "\n Congratulations!\n You have been successfully\n registered) " + Fore.RESET)

    def sgn_in(self):
        user_id = self.servr.sgn_in(*Controller.get_func_args(self.servr.sgn_in))
        self.curr_usr_id = user_id
        self.menu = 'User menu'
        print(Fore.GREEN + f"\n Good to see you again! " + Fore.RESET)
    def inbox_mess(self):
        messages = self.servr.get_mess(self.curr_usr_id)
        Menu.display_list("-" * 30 + "\n My messages: ", messages)

    def get_mess_statistics(self):
        statistics = self.servr.get_mess_statistics(self.curr_usr_id)
        Menu.display_item(statistics)

    def sgn_out(self):
        if self.curr_usr_id != -1:
            self.servr.sgn_out(self.curr_usr_id)
            self.menu = 'Main menu'
            self.curr_usr_id = -1

    def send_mess(self):
        self.servr.create_mess(*Controller.get_func_args(self.servr.create_mess, 1),
                               self.curr_usr_id)


