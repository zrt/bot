# gitpull cmd
import subprocess, var
from telegram.ext import CommandHandler

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False


def gitpull(bot, update):
    if not check_admin(update.message.from_user.id):
    	return
    text = ''
    try:
        ret = subprocess.check_output(['git', 'pull'])
        text = 'ok\n'+ret.decode('utf-8')
    except subprocess.CalledProcessError as err:
        text = 'failed'
    bot.send_message(chat_id=update.message.chat_id, text=text)

_handler = CommandHandler('gitpull', gitpull)
