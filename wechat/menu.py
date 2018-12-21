import requests
import json

def get_token():
    APPID = "wx3ceb9e7639c54c75"
    AppSecret = "58ca8dc9afd67aa4cd2b0fb054bbc46f"
    token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(APPID, AppSecret)
    json_token = requests.get(token_url).json()
    access_token = json_token['access_token']
    print(access_token)
    return access_token

def creat_menu(access_token):
    data = """{
     "button":[
     {
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
            
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"V1001_GOOD"
            }]
       }]
 }"""
    #data = json.dumps(data)
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + access_token
    resp = requests.post(url,json=data).json()
    print(resp)

access_token='15_gKO5TkNJnMeUZimsbFIBZf0IdgEbQ_onZ3qLDHNF--fV7h5qk7tR0hfZJiY04OhJrEFmB1WYRZDt36uzXRdJbwpE0VpGA91o8t-xKbvPeXXk9U4JRef8CqZ5nFHaVEoh1T1vAP0sgTsKaujMDMZbAGAJSF'
creat_menu(access_token)