import const,var
import telegram

def callback_daily(bot, job):
    bot.send_message(
        chat_id=const.DAILY_CHANNEL_ID, 
        text=const.DAILY_MESSAGE,
    )

_callback = callback_daily
_first = const.DAILY_TIME
_interval = 24*60*60