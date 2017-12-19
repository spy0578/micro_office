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


        event_key = param_dict['EventKey'] 
        print 'event_key:[%s]' % event_key

        group_id = get_user_group_id(from_user_name)
        if group_id == '' :
            print g.errinfo
            return True, {}, json.dumps({"msgtype":"text","touser":from_user_name,"text":{"content":"获取用户组信息失败"}})

        else :
            print 'group_id:[%s]' % group_id
            '''
            菜单与用户组 权限关系表 用户组1-菜单1
                            用户组1-菜单2
                            用户组2-菜单2
            如果查询到权限关系，则可以访问               
            '''
            push_material_to_users([from_user_name], '82350', const.PUBLIC_PLAT_METERIAL_TYPE_NEWS)
            return True, {}, json.dumps({})
