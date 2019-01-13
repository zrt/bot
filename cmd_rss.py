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

def rss(bot, update):
    if not check_admin(update.message.from_user.id):
        return
    # show info and help
    text = '''Miniflux url: {}
user: {}
feeds num: {}
bind channel: {}
lastest entry id: {}
unread num: {}
max unread num: {}
---
/rssadd add a new rss feed
/rsssetlatestentryid <id> set latest entry id
'''.format(const.MINIFLUX_URL, const.MINIFLUX_USER, miniflux_client.get_feeds_num(), const.MINIFLUX_CHANNEL_ID
    , var.get('rsslatestid', None), var.get('rssunreadnum', None), const.MINIFLUX_MAXUNREAD)
    update.message.reply_text(text)


_handler = CommandHandler('rss',rss)
