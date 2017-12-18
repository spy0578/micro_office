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
url = "https://168.1.6.140:9016/mass/masspush.action?access_token=954b8ae3e51195c96c273d776162c3"
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
'''

post_params = {
   "touser":[
    "100099671"
   ],
   "mpnews":{
      "media_id":"82058"
   },
   "msgtype":"mpnews"     
}        


r = requests.post(url, verify=False, data=json.dumps(post_params))
print(r.text)

def https_post(url, post_params={}, headers={}):
    r = requests.post(url, verify=False, data=json.dumps(post_params), headers=headers)
    print(r.text)

    return r.text

