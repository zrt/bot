# cannot reload

import const,var
import random
from flask import Flask
from flask import request

app = Flask('httpcallback')
TOKEN = const.HTTPCALLBACK_TOKEN
BOT = None
@app.route('/<path:msg>',methods=['GET'])
def callback(msg):
    global TOKEN
    global BOT
    token = request.args.get('token')
    if token == None or len(token) != len(TOKEN) or token != TOKEN:
        return 'Unauthorized',403
    argmsg = request.args.get('msg')
    msg = msg[:const.HTTPCALLBACK_MAXLEN]
    if argmsg != None:
        msg = msg + '\n' + argmsg[:const.HTTPCALLBACK_MAXLEN]
    if BOT != None:
        BOT.send_message(
            chat_id=const.HTTPCALLBACK_BINDCHANNEL, 
            text=msg,
        )
    else:
        print(msg)
    return 'ok,'+str(len(msg))

def randstr():
    charset = []
    for i in range(10):
        charset.append(str(i))
    for i in range(26):
        charset.append(chr(ord('a')+i))
        charset.append(chr(ord('A')+i))
    return ''.join([random.choice(charset) for x in range(32)])

def startapp(bot):
    global TOKEN
    global BOT
    BOT = bot
    if TOKEN == 'random':
        TOKEN = randstr()
    var.set('httpcallback_token', TOKEN)
    var.set('httpcallback_port', const.HTTPCALLBACK_PORT)
    var.set('httpcallback_channel', const.HTTPCALLBACK_BINDCHANNEL)
    var.set('httpcallback_maxlen', const.HTTPCALLBACK_MAXLEN)
    app.run(debug=False,host='0.0.0.0',port=const.HTTPCALLBACK_PORT)

if __name__ == '__main__':
    startapp(None)
