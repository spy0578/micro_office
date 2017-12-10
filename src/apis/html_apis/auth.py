# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BaseGetClass(MethodView):
    @staticmethod
    def get():

        print 'request.args:', request.args
        parameters = request.args


        token = request.headers.get('Authorization')
        if token == 'undefined':
            return ret_func(const.RET_USER_ID_NOT_LOGIN, '', {})



        return ret_func(const.RET_SUCCESS, '', {})



