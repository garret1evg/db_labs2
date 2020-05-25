from inspect import signature
from menu import Menu


class Controller(object):
    @staticmethod
    def mkchoice(menu_listing: list, name_menu: str):
        try:
            Menu.display_menu(menu_listing, name_menu)
            return Controller.get_men_val(" Your text :  ", len(menu_listing))

        except Exception as e:
            Menu.display_error(str(e))

    @staticmethod
    def consid_choice(controller, choi: int, listing_func: list):
        try:
            if choi > len(listing_func) - 1:
                raise Exception("func is not exist")

            desird_func = listing_func[choi]
            desird_func(controller)
        except Exception as e:
            Menu.display_error(str(e))

    @staticmethod
    def get_func_args(func, amount_miss_arguments=0) -> list:
        from data import special_params
        listing_params = signature(func).parameters
        listing_args = []
        length = len(listing_params)
        for i in range(length - amount_miss_arguments):
            listing_args.append(Controller.get_val(
                f" Please, enter {list(listing_params)[i]}{special_params[list(listing_params)[i]] if list(listing_params)[i] in special_params else ''}: ",
                str))
        return listing_args

    @staticmethod
    def get_men_val(msg: str, top_line: int = None):
        while True:
            num = input(msg)
            if num.isdigit():
                num = int(num)
                if top_line is None or 0 <= num < top_line:
                    return num

    @staticmethod
    def get_val(msg: str, variation_var):
        while True:
            try:
                usr_inpt = input(msg)
                if variation_var == str:
                    if len(usr_inpt) != 0:
                        return variation_var(usr_inpt)
                else:
                    return variation_var(usr_inpt)
            except Exception as e:
                Menu.display_error(str(e))

    @staticmethod
    def stp_loop(controller):
        controller.loop = False
