from flask import Flask
from flask import request,make_response
import hashlib

from dispatcher import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/weixin', methods=["GET","POST"])#处理微信请求的处理函数，get方法用于认证，post方法取得微信转发的数据
def index():
    if request.method == "GET":
        token = 'binlau'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s.encode('utf-8')).hexdigest() == signature):
            return make_response(echostr)
        else:
            return make_response('认证失败')
    else:
        rec = request.stream.read()#接收消息
        dispatcher = MsgDispatcher(rec)
        data = dispatcher.dispatch()
        with open("./debug.log", "a",encoding ='UTF-8') as file:
            file.write(data)
        response = make_response(data)
        response.content_type = 'application/xml'
        return response

if __name__ == '__main__':
    #默认的5000端口也能成功？
    app.run()
