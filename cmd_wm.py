# write mode cmd

import const,var
import miniflux_client
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler,ConversationHandler, RegexHandler, MessageHandler, Filters)


WM, READY, SENT = range(3)

def check_admin(check_id):
    admin_list = var.get('admin_list', [])
    if check_id in admin_list:
        return True
    return False

def writemode(bot, update):
    if not check_admin(update.message.from_user.id):
        return ConversationHandler.END
    var.set('blogarticle', '')
    var.set('blogarticleimg', [])
    update.message.reply_text('进入写作模式\n请发给我文字或图片\n/preview 命令来预览发送\n/cancel 命令退出写作模式')
    return WM

def addtext(bot, update):
    text = update.message.text
    var.set('blogarticle', var.get('blogarticle','')+text+'\n')
    update.message.reply_text('(%d)\n%s'%(len(var.get('blogarticle','')), var.get('blogarticle','')[-500:] + '...\n/preview 命令来预览发送\n/cancel 命令退出写作模式'))
    return WM

def addimg(bot, update):
    update.message.reply_text('todo')
    
    return WM

def confirm(bot, update):
    var.set('blogarticlepos', 0)
    update.message.reply_text('(%d/%d)\n%s'%(1,(len(var.get('blogarticle',''))-1)//500+1, var.get('blogarticle','')[:500] + '...\n/yes [title] [ascii title]  确认发送\n/no 继续编辑\n/prevpage 上一页 \n/nextpage 下一页'))
    return READY

def prevpage(bot, update):
    pos = var.get('blogarticlepos', 0 )
    if pos == 0:
        update.message.reply_text('没有上一页qwq')
    else:
        pos = pos -1
        var.set('blogarticlepos', pos)
        update.message.reply_text('(%d/%d)\n%s'%(pos+1,(len(var.get('blogarticle',''))-1)//500+1, var.get('blogarticle','')[pos*500:(pos+1)*500] + '...\n/yes [title] [ascii title] 确认发送\n/no 继续编辑\n/prevpage 上一页 \n/nextpage 下一页\n/cancel 命令退出写作模式'))
    return READY

def nextpage(bot, update):
    pos = var.get('blogarticlepos', 0 )
    if pos == (len(var.get('blogarticle',''))-1)//500:
        update.message.reply_text('没有下一页qwq')
    else:
        pos = pos +1
        var.set('blogarticlepos', pos)
        update.message.reply_text('(%d/%d)\n%s'%(pos+1,(len(var.get('blogarticle',''))-1)//500+1, var.get('blogarticle','')[pos*500:(pos+1)*500] + '...\n/yes [title] [ascii title] 确认发送\n/no 继续编辑\n/prevpage 上一页 \n/nextpage 下一页\n/cancel 命令退出写作模式'))
    return READY


def confirm_yes(bot, update, args):
    if len(args) != 2:
        update.message.reply_text('usage: /yes [title] [ascii title]')
        return READY
    article = var.get('blogarticle','')
    article += '\n\n> via [msbot](https://github.com/zrt/bot)\n'
    thread = articlemanager.create(args[0],args[1],article)
    var.set('blogarticlethread', thread)
    update.message.reply_text('发送中...\n/check 检查发送进度\n/cancel 退出写作模式')
    return SENT

def confirm_no(bot, update):
    update.message.reply_text('(%d)\n%s'%(len(var.get('blogarticle','')), var.get('blogarticle','')[-500:] + '...\n/preview 命令来预览发送\n/cancel 命令退出写作模式'))
    return WM

def check(bot, update):
    thread = var.get('blogarticlethread', None)
    if thread == None or thread.isAlive() == False:
        var.set('blogarticlethread', None)
        update.message.reply_text('发送完成\n/wm 开启新的一篇文章')
        return ConversationHandler.END
    else:
        update.message.reply_text('发送中...\n/check 检查发送进度\n/cancel 退出写作模式')
        return SENT
    


def cancel(bot, update):
    update.message.reply_text('canceled', reply_markup=ReplyKeyboardRemove())
    # 清空下载的图片

    return ConversationHandler.END



conv = ConversationHandler(
    entry_points = [CommandHandler('wm',writemode)],
    states = {
        WM: [ MessageHandler(Filters.text, addtext), MessageHandler(Filters.photo, addimg), CommandHandler('preview',confirm)],
        READY: [CommandHandler('prevpage',prevpage),CommandHandler('nextpage',nextpage),CommandHandler('yes',confirm_yes, pass_args =True),CommandHandler('no',confirm_no)],
        SENT: [CommandHandler('check',check)]
    },
    fallbacks = [CommandHandler('cancel', cancel)]
)

_handler = conv
