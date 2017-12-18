# -*- coding: utf-8 -*-
import time
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random

from base.log import g_log


'''
功能：

输入：
输出:
'''

class RequestRouteHandler(MethodView):


    def get(self, route_root, route_name):
        return base_request_route_handler(route_root, route_name, 'module.BaseGetClass.get')


    def post(self, route_root, route_name):
        return base_request_route_handler(route_root, route_name, 'module.BasePostClass.post')

    def put(self, route_root, route_name):
        return base_request_route_handler(route_root, route_name, 'module.BasePutClass.put')
