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

'''
功能：

输入：
输出:
'''

class StaticRequestRouteHandler(MethodView):
    def get(self, filename):
        #filename = htmlfile + '.html'
        return send_from_directory(configs[config_type].STATIC_TEMPLATE_FOLDER
                                   , filename)

