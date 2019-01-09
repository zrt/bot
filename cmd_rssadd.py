# rss cmd

import const,var
import miniflux_client
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler,ConversationHandler, RegexHandler, MessageHandler, Filters)

START, DISCOVER, ADD = range(3)

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def add(bot,update):
    if not check_admin(update.message.from_user.id):
        return ConversationHandler.END
    update.message.reply_text('Please send me the url. \nSend /cancel to stop talking to me.')
    return DISCOVER

def discover(bot, update):
    url = update.message.text
    feeds = miniflux_client.discover(url)
    reply_keyboard = [[x['url']] for x in feeds]

    update.message.reply_text('url :'+ url +'\n'
        '%d feeds found.'%len(reply_keyboard),reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ADD

def finish(bot,update):
    feed = update.message.text
    feedid, ret = miniflux_client.create_feed(feed)
    update.message.reply_text('%s \nfeed id: %d'%(ret,feedid), reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
def cancel(bot, update):
    update.message.reply_text('canceled', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conv = ConversationHandler(
    entry_points = [CommandHandler('rssadd',add)],
    states = {
        DISCOVER: [ MessageHandler(Filters.text, discover)],
        ADD: [MessageHandler(Filters.text, finish)]
    },
    fallbacks = [CommandHandler('cancel', cancel)]
)

_handler = conv
