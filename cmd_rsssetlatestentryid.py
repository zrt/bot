# rss cmd

import const,var
import miniflux_client
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler,ConversationHandler, RegexHandler, MessageHandler, Filters)

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def rsssetlatestentryid(bot, update , args):
    if not check_admin(update.message.from_user.id):
        return
    # show info and help
    result = ''
    entryid = -1
    try:
        entryid = int(args[0])
        var.set('rsslatestid', entryid)
        result = 'ok '+str(entryid)
    except Exception as e:
        result = 'error '+str(e)
    update.message.reply_text(result)


var.get('rsslatestid', miniflux_client.get_latest_entry_id())
_handler = CommandHandler('rsssetlatestentryid',rsssetlatestentryid,  pass_args = True)
