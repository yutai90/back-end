import requests
import json

def get_turing_response(req=""):
    url = "http://openapi.tuling123.com/openapi/api/v2"
    content = {
    "perception": {"inputText": {"text": req},},
    "userInfo": {"apiKey": "db65a29d197f4f0f944d64d94c9c8462","userId": ""}
}
    content = json.dumps(content)
    response = requests.post(url=url,json=content).json()
    return response['results'] if response['intent'] == 200 else "出现异常"

def get_response_by_keyword(keyword):
    if "团建" in keyword:
        result ={'type':'image','content':'3s9Dh5rYdP9QruoJ_M6tIYDnxLLdsQNCMxkY0L2FMi6HhMlNPlkA1-50xaE_imL7'}
    elif 'music' in keyword or '音乐' in keyword:
        musicurl = 'http://204.11.1.34:9999/dl.stream.qqmusic.qq.com/C400001oO7TM2DE1OE.m4a?vkey=3DFC73D67AF14C36FD1128A7ABB7247D421A482EBEDA17DE43FF0F68420032B5A2D6818E364CB0BD4EAAD44E3E6DA00F5632859BEB687344&guid=5024663952&uin=1064319632&fromtag=66'
        result = {'type': 'music', 'content': {'title':'222', 'description':"有个男歌手姓liu，于是这首歌叫222", "url": musicurl, "hqurl": musicurl}}
    elif '关于' in keyword:
        items = [{"title": "关于我", "description":"喜欢瞎搞一些脚本", "picurl":"http://www.etian365.com/resources/web/images/about_img.jpg", "url":"https://github.com/yutai90"},
                 {"title": "我的博客", "description":"收集到的，瞎写的一些博客", "picurl":"http://avatar.csdn.net/0/8/F/1_marksinoberg.jpg", "url":"http://blog.csdn.net/marksinoberg"},
                 {"title": "薛定谔的��", "description": "副标题有点奇怪，不知道要怎么设置比较好","picurl": "https://www.baidu.com/img/bd_logo1.png","url": "http://www.baidu.com"}
                 ]
        result = {'type':'news','content':items}
    else:
        result = {"type": "text", "content": "可以自由进行拓展"}
    return result


def get_qingyunke_response(req=""):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(req)
    response = requests.get(url)
    return json.loads(response.text)['content'] if response.status_code == 200 else ""