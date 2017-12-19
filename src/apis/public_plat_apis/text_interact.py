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

        parameters = request.data
        param_dict = eval(parameters)

        to_user_name = param_dict['ToUserName']
        from_user_name = param_dict['FromUserName']
        create_time = param_dict['CreateTime']
        msg_type = param_dict['MsgType']
        print 'msg_type:[%s]' % msg_type


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
