# coding:utf-8
import requests
import json
# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


html_content='   \
<!DOCTYPE html>   \
<html>   \
<head>   \
    <title>密码输入组件的使用示例</title>   \
    <link rel="stylesheet" href="sencha-touch.css"   \
    type="text/css">   \
    <script type="text/javascript" src="sencha-touch-all-debug.js">   \
    </script>   \
    <script type="text/javascript" src="echarts.js">   \
    </script>   \
    <script type="text/javascript" src="app.js"></script>   \
</head>   \
<body>   \
    <div id="echart" style="width:100%;height:250px;"></div>     \
</body>   \
</html>   \
'

#url = "https://168.1.6.140:9016/mass/material.action?access_token=954b8ae3e51195c96c273d776162c3"
#url = "https://168.1.6.140:9016/mass/masspush.action?access_token=954b8ae3e51195c96c273d776162c3"
url = "https://168.1.6.140:9016/group/move.action?access_token=11a3da47a743e8e760201343a0c0eb3f"
#url = "https://168.1.6.140:9016/group/new.action?access_token=11a3da47a743e8e760201343a0c0eb3f"
headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"
          }
'''
post_params = {"touser":"100099671","msgtype":"text","text":{"content":"Hello World"}}
'''
'''
post_params = {
    "articles": [
    {
    "thumb_media_id":"23290",
    "author":"xxx",
    "title":"Happy Day",
    "content_source_url":"www.google.com",
    "content":html_content,
    "digest":"digest",
    "show_cover_pic":"1"
    }]
 }


post_params = {
   "touser":[
    "100099671"
   ],
   "mpnews":{
      "media_id":"82058"
   },
   "msgtype":"mpnews"     
}        
'''

'''
post_params = {
"group":{"name":"it_dep"}
}
'''

def https_post(url, post_params={}, headers={}):
    r = requests.post(url, verify=False, data=json.dumps(post_params), headers=headers)
    print(r.text)

    return r.text

def get_user_group_id():
    QUERY_GROUP_URL       = 'https://168.1.6.140:9016/group/query.action?access_token=11a3da47a743e8e760201343a0c0eb3f'
    post_params = {"userid":"100099671"}

    r = requests.post(QUERY_GROUP_URL, verify=False, data=json.dumps(post_params))
    print(r.text)

def create_position_data_info():
    CREATE_MATERIAL_INFO_URL = 'https://168.1.6.140:9016/mass/material.action?access_token=' + 'd48dd93ab17ab9e0da767f9d813a0cc'

    post_params = {
        "articles": [
        {
        "thumb_media_id":"23348",
        "author":"xxx",
        "title":"Happy Day",
        "content_source_url":"www.google.com",
        "content":html_content,
        "digest":"digest",
        "show_cover_pic":"1"
        }]
    }

    r = requests.post(CREATE_MATERIAL_INFO_URL, verify=False, data=json.dumps(post_params))
    print(r.text)


def create_menu():
    CREATE_MENU_URL       = 'https://168.1.6.140:9016/menu/new.action?access_token=d48dd93ab17ab9e0da767f9d813a0cc'

    post_params = {
     "button":[
     {  
          "name":"营销考核",
          "sub_button":[
          {
              "type":"click",
              "name":"头寸",
              "key":"1701"         
          }
          ]
      },
      {
           "name":"系统运维",
           "sub_button":[
            {    
               "type":"view",
               "name":"搜索",
               "url":"http://168.40.5.23:8002/SenchaTouch/Demo/form/index.html"
            },
            {
               "type":"view",
               "name":"测试",
               "url":"http://v.qq.com/"
            },
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"1702"
            },
            {
               "type":"click",
               "name":"双击666",
               "key":"1703"
            }           
            ]
       }]
    }
 
    r = requests.post(CREATE_MENU_URL, verify=False, data=json.dumps(post_params))
    print(r.text)


if __name__ == '__main__':
    create_position_data_info()



