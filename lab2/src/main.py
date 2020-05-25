from src.entity.controller import Controller
from src.entity.user import UserController
from  emulation import emulation

if __name__ == "__main__":
    choice = Controller.mkchoice(["Main mode", "Emulation mode"], "Program menu")
    if choice == 0:
        UserController()
    elif choice == 1:
        emulation()
