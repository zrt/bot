# httpcallback cmd
import subprocess
from telegram.ext import CommandHandler
import var

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def httpcallback(bot, update):
    if not check_admin(update.message.from_user.id):
        return
    text = 'PORT: {}\nTOKEN: {}\nCHANNEL: {}\nMAXLEN: {}\n'.format(
        var.get('httpcallback_port',None),
        var.get('httpcallback_token',None),
        var.get('httpcallback_channel',None),
        var.get('httpcallback_maxlen',None))
    bot.send_message(chat_id=update.message.chat_id, text=text)

_handler = CommandHandler('httpcallback', httpcallback)
