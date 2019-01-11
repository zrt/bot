# 总未读数量限制 0 or 20

import const,var
import miniflux_client
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re
# MINIFLUX_MAXUNREAD
var.get('rssunreadnum', 0)
htmltag = re.compile(r'</?\w+[^>]*>')
def escapehtml(s):
    return htmltag.sub('',s)

def get_info(entry):
    ret = ''
    ret += "%s\n"%entry['title']
    ret += '%s\n'%entry['author']
    ret += entry['url']+'\n'
    ret += '%s, .%d\n'%(entry['published_at'],entry['id'])
    s = escapehtml(entry['content'])
    if len(s) <1500:
        ret += escapehtml(s)
    else:
        ret += escapehtml(s) +'...'
    return ret

def send_entry(bot, entry):
    text = get_info(entry)
    motd_keyboard = [[
        InlineKeyboardButton(
            '📦',
            callback_data="rssmarkread,%d,0,0" % entry['id']
        )
    ,
        InlineKeyboardButton(
            '✨',
            callback_data="rssmarkstar,%d,0,0"  % entry['id']
        )
    ]]
    motd_markup = InlineKeyboardMarkup(motd_keyboard)

    bot.send_message(
        chat_id=const.MINIFLUX_CHANNEL_ID, 
        text=text,
        reply_markup=motd_markup
    )


def callback_rss(bot, job):
    unreadnum = var.get('rssunreadnum', 0)
    lastid = var.get('rsslatestid', 0)
    if unreadnum >= const.MINIFLUX_MAXUNREAD:
        return
    entries = miniflux_client.get_entries(lastid)
    for x in entries:
        send_entry(bot,x)
        lastid = max(lastid, x['id'])
    var.set('rsslatestid', lastid)
    var.set('rssunreadnum', unreadnum+len(entries))

_callback = callback_rss
_first = 0
_interval = 60*8 # 8 min