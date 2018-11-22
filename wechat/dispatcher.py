import time
import xml.etree.ElementTree as ET
from robot import *

class MsgParser(object):

    def __init__(self,data):
        self.data = data

    def parser(self):
        #有self的这些，所以类方法都可以用，没有self的变量只能在本方法中用
        self.et = ET.fromstring(self.data)
        self.user = self.et.find('FromUserName').text
        self.master = self.et.find('ToUserName').text
        self.msgtype = self.et.find('MsgType').text
        #纯文字信息字段
        self.content = self.et.find('Content').text if self.et.find('Content') is not None else ""
        #图片
        self.picurl = self.et.find("PicUrl").text if self.et.find("PicUrl") is not None else ""
        self.mediaid = self.et.find("MediaId").text if self.et.find("MediaId") is not None else ""
        #事件
        self.event  = self.et.find("Event").text if self.et.find("Event") is not None else ""

        return self #返回实例

class MsgDispatcher(object):

    def __init__(self,data):
        parser = MsgParser(data).parser()
        self.msg = parser
        self.handler = MsgHandle(parser)

    def dispatch(self):
        self.result = ""
        if self.msg.msgtype == "text":
            self.result = self.handler.textHandle()
        elif self.msg.msgtype == "voice":
            self.result = self.handler.voiceHandle()
        elif self.msg.msgtype == 'image':
            self.result = self.handler.imageHandle()
        elif self.msg.msgtype == 'video':
            self.result = self.handler.videoHandle()
        elif self.msg.msgtype == 'shortvideo':
            self.result = self.handler.shortVideoHandle()
        elif self.msg.msgtype == 'location':
            self.result = self.handler.locationHandle()
        elif self.msg.msgtype == 'link':
            self.result = self.handler.linkHandle()
        elif self.msg.msgtype == 'event':
            self.result = self.handler.eventHandle()
        return self.result


class MsgHandle(object):
    "每个信息对应的处理函数"
    def __init__(self,msg):
        self.msg = msg
        self.time = int(time.time())

    def textHandle(self,user='', master='', time='',content=''):
        template ="""
        <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[{}]]></Content>
         </xml>
        """
        try:
            response = get_response_by_keyword(self.msg.content)
            if response['type'] == 'image':
                result = self.imageHandle(self.msg.user, self.msg.master, str(self.time), response['content'])
            elif response['type'] == "music":
                data = response['content']
                result = self.musicHandle(data['title'], data['description'], data['url'], data['hqurl'])
            elif response['type'] == "news":
                items = response['content']
                result = self.newsHandle(items)
            else:
                response = get_turing_response(self.msg.content)
                result = template.format(self.msg.user, self.msg.master, self.time, response)
            return result

        except Exception as e:
            with open('./debug.log','a') as f:
                f.write("text handler:"+str(e.message))



    def musicHandle(self, title='', description='', url='', hqurl=''):
        template = """
        <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[music]]></MsgType>
             <Music>
             <Title><![CDATA[{}]]></Title>
             <Description><![CDATA[{}]]></Description>
             <MusicUrl><![CDATA[{}]]></MusicUrl>
             <HQMusicUrl><![CDATA[{}]]></HQMusicUrl>
             </Music>
             <FuncFlag>0</FuncFlag>
        </xml>
        """
        response = template.format(self.msg.user, self.msg.master, self.time, title, description, url, hqurl)
        return response

    def voiceHandle(self):
        response = get_turing_response(self.msg.recognition)
        result = self.textHandle(self.msg.user, self.msg.master, str(self.time), response)
        return result

    def imageHandle(self, user='', master='', time='', mediaid=''):
        template = """
        <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>{}</CreateTime>
             <MsgType><![CDATA[image]]></MsgType>
             <Image>
             <MediaId><![CDATA[{}]]></MediaId>
             </Image>
         </xml>
        """
        if mediaid == '':
            response = self.msg.mediaid
        else:
            response = mediaid
        result = template.format(self.msg.user, self.msg.master, self.time, response)
        return result

    def videoHandle(self):
        return 'video'

    def shortVideoHandle(self):
        return 'shortvideo'

    def locationHandle(self):
        return 'location'

    def linkHandle(self):
        return 'link'

    def eventHandle(self):
        return 'event'

    def newsHandle(self, items):
        # 图文消息这块真的好多坑，尤其是<![CDATA[]]>中间不可以有空格，可怕极了
        articlestr = """
        <item>
            <Title><![CDATA[{}]]></Title>
            <Description><![CDATA[{}]]></Description>
            <PicUrl><![CDATA[{}]]></PicUrl>
            <Url><![CDATA[{}]]></Url>
        </item>
        """
        itemstr = ""
        for item in items:
            itemstr += str(articlestr.format(item['title'], item['description'], item['picurl'], item['url']))

        template = """
        <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>{}</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>{}</ArticleCount>
            <Articles>{}</Articles>
        </xml>
        """
        result = template.format(self.msg.user, self.msg.master, self.time, len(items), itemstr)
        return result
