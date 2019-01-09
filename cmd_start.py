# start cmd

import var
from telegram.ext import CommandHandler

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def start(bot, update, args):
    if args is None or len(args) == 0:
        text = '''Welcome!
This is @Ruotian's personal bot.
See /help for a list of commands.
'''
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return
    elif check_admin(update.message.from_user.id):
        # check admin
        pass

    # param

_handler = CommandHandler('start', start, pass_args = True)
