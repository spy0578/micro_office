# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DBAPIError
from redis.exceptions import RedisError
from base.log import g_log
import base64
from public_plat_api_comm import *

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session

        print 'request.get_data():[%s]' % request.get_data()
        print 'request.data:[%s]' % request.data
        print 'type request.data:[%s]' % type(request.data)

        parameters = request.data
        param_dict = eval(parameters)

        to_user_name = param_dict['ToUserName']
        from_user_name = param_dict['FromUserName']
        create_time = param_dict['CreateTime']
        msg_type = param_dict['MsgType']
        print 'msg_type:[%s]' % msg_type


        if msg_type == const.PUBLIC_PLAT_MSG_TYPE_TEXT :

            content = param_dict['Content']
            msg_id = param_dict['MsgId']


            print 'content decode:[%s]' % base64.b64decode(content)

            input_content = base64.b64decode(content)

           
            '''
            判断输入的是否是手机号
          	如果注册信息表有记录，则说明已注册过
            否则根据手机号查找notes信息表，查找到notes的userid，再和当前的from_user_name比较
            如果是则注册成功：登记注册信息表, 设置默认权限
            '''


            if input_content.isdigit():# and len(input_content) == 11 :


                #设置用户权限为const.OTHER_DEP_GROUP
                if modify_user_group([from_user_name], const.OTHER_DEP_GROUP) is False:
                    return False, {}, json.dumps({"msgtype":"text","touser":from_user_name,"text":{"content":"注册失败，请再次尝试"}})

                return True, {}, json.dumps({"msgtype":"text","touser":from_user_name,"text":{"content":"手机号注册成功"}})

            return True, {}, json.dumps({"msgtype":"text","touser":from_user_name,"text":{"content":"hi~请输入手机号注册~"}})

            '''
            return True, {}, json.dumps(
              {
              "touser":from_user_name,
              "msgtype":"news",
              "news":{
                  "articles": [
                   {
                       "title":"Happy Day",
                       "description":"Is Really A Happy Day",
                       "url":"http://168.40.5.23:8002/SenchaTouch/Demo/form/index.html"
                   },
                        ]
              }
               }) 
            '''

        elif msg_type == const.PUBLIC_PLAT_MSG_TYPE_EVENT:
            '''
            触发菜单点击事件，获取菜单名，根据用户notesuserid判断是否已注册，从公众号服务端获取用户组信息，
            菜单与用户组 权限关系表 用户组1-菜单1
                                用户组1-菜单2
                                用户组2-菜单2
            如果查询到权限关系，则可以访问
            推送图文信息
            '''
            event_key = param_dict['EventKey'] 
            print 'event_key:[%s]' % event_key

            group_id = get_user_group_id(from_user_name)
            if group_id == '' :
                return True, {}, json.dumps({"msgtype":"text","touser":from_user_name,"text":{"content":"获取用户组信息失败"}})


            else :
                print 'group_id:[%s]' % group_id
                '''
                菜单与用户组 权限关系表 用户组1-菜单1
                                用户组1-菜单2
                                用户组2-菜单2
                如果查询到权限关系，则可以访问               
                '''
                return True, {}, json.dumps({"msgtype":"text","touser":from_user_name,"text":{"content":"点击菜单"}})
        
  
class BaseGetClass(MethodView):    
    @staticmethod
    def get():
        log=g_log.get_sys_log()
        db_session = g.db_session


        print 'request.args:', request.args
        parameters = request.args

        '''
         分隔符为&，截取字符串
        '''
        param_dict = parameters.to_dict()

        print 'echostr:%s' % param_dict['echostr']



        #返回给request_route_handler的get方法
        return True, {}, param_dict['echostr']

