#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by zrt

import logging, importlib, traceback
import telegram
import telegram.bot
from telegram.ext import messagequeue as mq
from telegram.ext import Updater, CommandHandler
from telegram.utils.request import Request

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

const = importlib.import_module('const')
var  = importlib.import_module('var')
# database = importlib.import_module('database')
# db

var.set('admin_list', [])

def reload_admin_list():
    admin_list = const.BOT_ADMIN
    var.set('admin_list', admin_list)

reload_admin_list()


# config bot
class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()
  
    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)

    @mq.queuedmessage
    def edit_message_text(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).edit_message_text(*args, **kwargs)
 
q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
request = Request(con_pool_size=8)
bot = MQBot(token=const.BOT_TOKEN, request=request, mqueue=q)

bot_username = bot.get_me().username
var.get('bot', bot)
var.get('bot_username', bot_username)
updater = Updater(bot=bot)
dispatcher = updater.dispatcher
job_queue = updater.job_queue


def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def bot_reload(bot, update):
    global const
    global command_module
    global current_job
    # global database
    # db

    if not check_admin(update.message.from_user.id):
        bot.send_message(chat_id=update.message.chat_id, text="permission_denied")
        return

    ## update constant
    const = importlib.reload(const)
    # database = importlib.reload(database)
    # db
    reload_admin_list()

    ## stop the jobs
    for job in current_job:
        job.schedule_removal()
    current_job = []
    ## remove old handlers
    for current_module in command_module:
        dispatcher.remove_handler(current_module._handler)

    ## reload modules and update handlers
    try:
        command_module = []
        for module_name in const.MODULE_NAME:
            current_module = importlib.import_module(module_name)
            current_module = importlib.reload(current_module)
            command_module.append(current_module)
            dispatcher.add_handler(current_module._handler)
        for job_name in const.JOB_NAME:
            job_module = importlib.import_module(job_name)
            job_module = importlib.reload(job_module)
            job = job_queue.run_repeating(job_module._callback,interval= job_module._interval, first=job_module._first)
            current_job.append(job)

        bot.send_message(chat_id=update.message.chat_id, text="reload_cmd_success")
    except Exception as e:
        failed_text = "reload_cmd_failed"
        bot.send_message(chat_id=update.message.chat_id, text=failed_text)
        bot.send_message(chat_id=update.message.chat_id, text=traceback.print_exc())

reload_handler = CommandHandler('reload', bot_reload)
dispatcher.add_handler(reload_handler)




# initial other commands
command_module = []
current_job = []

for module_name in const.MODULE_NAME:
    current_module = importlib.import_module(module_name)
    command_module.append(current_module)
    dispatcher.add_handler(current_module._handler)
for job_name in const.JOB_NAME:
    job_module = importlib.import_module(job_name)
    job = job_queue.run_repeating(job_module._callback,interval= job_module._interval, first=job_module._first)
    current_job.append(job)
if const.ENABLE_HTTPCALLBACK:
    import threading
    httpcallbacklib = importlib.import_module('httpcallback')
    threading.Thread(target=httpcallbacklib.startapp,args=(bot,)).start()

updater.start_polling()
updater.idle()





