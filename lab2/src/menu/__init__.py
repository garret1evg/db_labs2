from colorama import Fore, Style


class Menu(object):
    @staticmethod
    def display_menu(menu_listing, name_menu: str):
        print("\n" + "-" * 30)
        print(Fore.CYAN + f"     ~~ {name_menu} ~~ ")
        print(Fore.BLACK + "-" * 30)
        number = 0
        for menu_item in menu_listing:
            print(Fore.BLACK + f" [{number}] - {menu_item}")
            number += 1
        print(Fore.BLACK + "-" * 30)

    @staticmethod
    def display_item(item):
        print(f"\n{item}")

    @staticmethod
    def display_items(items: list):
        count = 1
        for item in items:
            print(f"  [{count}] - {item}")
            count += 1

    @staticmethod
    def display_error(err: str):
        print(Fore.RED + f" Error: {err}")
        print(Style.RESET_ALL)

    @staticmethod
    def display_text(text: str):
        print(text)

    @staticmethod
    def display_line():
        print(' ~' * 30)

    @staticmethod
    def display_list(name_of_list, list):
        print(name_of_list)
        count = 1
        for item in list:
            print(f" №{count}.  {item}")
            count += 1
        print('-' * 30)
