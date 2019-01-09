import const,var
import miniflux_client
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
import re,threading

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def callback_query(bot, update):
    if not check_admin(update.callback_query.from_user.id):
        return
    callback_data = update.callback_query.data
    origin_message_id = update.callback_query.message.message_id
    text = update.callback_query.message.text
    chat_id = update.callback_query.message.chat_id
    args = callback_data.split(',')
    entryid = int(args[1])
    isread = int(args[2])
    isstar = int(args[3])
    motd_keyboard = None
    callbackanswer = ''
    if args[0] == 'rssmarkread':
        var.set('rssunreadnum',var.get('rssunreadnum', 1)-1)
        threading.Thread(target = miniflux_client.markread, args = (entryid,)).start()
        motd_keyboard = [[
            InlineKeyboardButton(
                '📦✔️',
                callback_data="rssmarkunread,%d,%d,%d" % (entryid,1,isstar)
            )
        ,
            InlineKeyboardButton(
                '✨'+['', '✔️'][isstar],
                callback_data="%s,%d,%d,%d" % (("rssmarkstar","rssmarkunstar")[isstar], entryid, 1, isstar)
            )
        ]]
        callbackanswer = '已标记为已读'
    elif args[0] == 'rssmarkstar':
        threading.Thread(target = miniflux_client.markstar, args = (entryid,)).start()
        motd_keyboard = [[
            InlineKeyboardButton(
                '📦'+['', '✔️'][isread],
                callback_data="%s,%d,%d,%d" % (("rssmarkread","rssmarkunread")[isread],entryid,isread,1)
            )
        ,
            InlineKeyboardButton(
                '✨✔️',
                callback_data="rssmarkstar,%d,%d,%d" % (entryid, isread, 1)
            )
        ]]
        callbackanswer = '已星标'
    elif args[0] == 'rssmarkunread':
        var.set('rssunreadnum',var.get('rssunreadnum', 0)+1)
        miniflux_client.markunread(entryid)
        motd_keyboard = [[
            InlineKeyboardButton(
                '📦',
                callback_data="rssmarkread,%d,%d,%d" % (entryid,0,isstar)
            )
        ,
            InlineKeyboardButton(
                '✨'+['', '✔️'][isstar],
                callback_data="%s,%d,%d,%d" % (("rssmarkstar","rssmarkunstar")[isstar], entryid, 0, isstar)
            )
        ]]
        callbackanswer = '已标记为未读'
    elif args[0] == 'rssmarkunstar':
        miniflux_client.markunstar(entryid)
        motd_keyboard = [[
            InlineKeyboardButton(
                '📦'+['', '✔️'][isread],
                callback_data="%s,%d,%d,%d" % (("rssmarkread","rssmarkunread")[isread],entryid,isread,0)
            )
        ,
            InlineKeyboardButton(
                '✨',
                callback_data="rssmarkstar,%d,%d,%d" % (entryid, isread, 0)
            )
        ]]
        callbackanswer = '已去掉星标'
    else:
        return
    motd_markup = InlineKeyboardMarkup(motd_keyboard)
    bot.edit_message_text(
        chat_id = chat_id, 
        message_id = origin_message_id,
        text = text,
        reply_markup = motd_markup
    )
    bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=callbackanswer
    )


# _handler = CallbackQueryHandler(callback_query, pattern = r'$(rssmarkread|rssmarkstar|rssmarkunread|rssmarkunstar),')

_handler = CallbackQueryHandler(callback_query)
