# uptime cmd
import subprocess
from telegram.ext import CommandHandler

def uptime(bot, update):
    text = ''
    try:
        ret = subprocess.check_output(['uptime'])
        text = 'ok\n'+ret.decode('utf-8')
    except subprocess.CalledProcessError as err:
        text = 'failed'
    bot.send_message(chat_id=update.message.chat_id, text=text)

_handler = CommandHandler('uptime', uptime)
