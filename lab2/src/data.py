from src.entity.user import UserController
from src.entity.admin import AdminController
from src.entity.controller import Controller

menu_listing = {
    'Main menu': {
        'Login to account': UserController.sgn_in,
        'Create an account': UserController.registr,
        'Exit': Controller.stp_loop,
    },
    'User menu': {
        'Send a message': UserController.send_mess,
        'Inbox messages': UserController.inbox_mess,
        'My messages statistics': UserController.get_mess_statistics,
        'Sign out': UserController.sgn_out
    },
    'Admin menu': {
        'Online users': AdminController.get_active_users,
        'Events': AdminController.get_events,
        'Most senders': AdminController.get_most_senders,
        'Most spamers': AdminController.get_most_spamers,
        'Sign out': Controller.stp_loop,
    }
}

roles = {
    'utilizr': 'Utilizr menu',
    'admin': 'Admin menu'
}

special_params = {
    'role': '(admin or utilizr)'
}
