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
from public_verify_apis.public_verify_api_comm import *

'''
功能：

输入：
输出:
'''

class PublicVerifyRequestRouteHandler(MethodView):
    def base(self, route_root, route_name, class_func_name):
		rds = g_rds_access.get_session_rds()
		g.access_token = rds.get(const.REDIS_ACCESS_TOKEN)

		if g.access_token is None :
			update_access_token(const.PUBLIC_PLAT_CLIENT_ID, const.PUBLIC_PLAT_CLIENT_SECRET)

		return base_request_route_handler(route_root, route_name, class_func_name)

    def get(self):
		return self.base('public_verify_apis', 'public_verify', 'module.BaseGetClass.get')

    def post(self):
    	return self.base('public_verify_apis', 'public_verify', 'module.BasePostClass.post')

