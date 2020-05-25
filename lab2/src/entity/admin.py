from src.entity.controller import Controller
from redisserv.listener import EventListener
from redisserv.redisservr import RedisServ
from menu import Menu


class AdminController(object):
    def __init__(self):
        self.servr = RedisServ()
        self.loop = True
        self.listenr = EventListener()
        self.listenr.start()
        self.start()

    def start(self):
        from data import menu_listing
        try:
            menu = "Admin menu"
            while self.loop:
                choice = Controller.mkchoice(menu_listing[menu].keys(), menu)
                Controller.consid_choice(self, choice, list(menu_listing[menu].values()))
        except Exception as e:
            Menu.display_error(str(e))


    def get_events(self):
        events = self.listenr.get_events()
        Menu.display_list("Events: ", events)

    def get_active_users(self):
        active_users = self.servr.get_active_users()
        Menu.display_list("Online users: ", active_users)

    def get_most_senders(self):
        most_senders = self.servr.get_most_senders(
            *Controller.get_func_args(self.servr.get_most_senders))
        Menu.display_list("Most senders: ", most_senders)

    def get_most_spamers(self):
        most_spamers = self.servr.get_most_spamers(
            *Controller.get_func_args(self.servr.get_most_spamers))
        Menu.display_list("Most spamrs: ", most_spamers)