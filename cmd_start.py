# start cmd

from telegram.ext import CommandHandler

def start(bot, update, args):
    if args is None or len(args) == 0:
        text = '''Welcome!
This is @Ruotian's personal bot.
See /help for a list of commands.
'''
        bot.send_message(chat_id=update.message.chat_id, text=text)
        return
    # param

_handler = CommandHandler('start', start, pass_args = True)
