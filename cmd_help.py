# help cmd

from telegram.ext import CommandHandler

def help(bot, update):
    text = '''/help show this
/reload reload this bot
/uptime show uptime
/rss miniflux rss
/gitpull run git pull
/httpcallback show http callback config
/wm enter writing mode
'''
    bot.send_message(chat_id=update.message.chat_id, text=text)

_handler = CommandHandler('help', help)

'''
/setcommands

help - show help
reload - reload this bot
uptime - show uptime
rss -  miniflux rss
gitpull - run git pull
httpcallback - show http callback config
wm enter writing mode
'''
