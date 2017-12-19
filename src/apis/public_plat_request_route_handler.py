# -*- coding: utf-8 -*-
import time
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, send_from_directory
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
import importlib
from base.log import g_log
from db.dborm.dborm import TblOlLogInfo
from etc.config import *
from public_plat_apis.public_plat_api_comm import *
from public_plat_apis.text_interact import *
from public_plat_apis.event_handler import *

'''
功能：

输入：
输出:
'''

class PublicPlatRequestRouteHandler(MethodView):
    def init_access_token(self):
		rds = g_rds_access.get_session_rds()
		g.access_token = rds.get(const.REDIS_ACCESS_TOKEN)

		if g.access_token is None :
			print 'PublicVerifyRequestRouteHandler base'
			update_access_token(const.PUBLIC_PLAT_CLIENT_ID, const.PUBLIC_PLAT_CLIENT_SECRET)


    def get(self):
        self.init_access_token()
        return base_request_route_handler('public_plat_apis', 'public_verify', 'module.BaseGetClass.get')

    def post(self):
        self.init_access_token()

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


        #<todo>可以修改为根据配置表中 msg_type <-> 与api名对应关系
        if msg_type == const.PUBLIC_PLAT_MSG_TYPE_TEXT :
        	return base_request_route_handler('public_plat_apis', 'text_interact', 'module.BasePostClass.post')
        elif msg_type == const.PUBLIC_PLAT_MSG_TYPE_EVENT:
            return base_request_route_handler('public_plat_apis', 'event_handler', 'module.BasePostClass.post')

