# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
import base64
import StringIO
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class BasePostClass(MethodView):
    @staticmethod
    def post():

        print 'request.headers:[%s]' % request.headers

        print request.get_data()
        if request.get_data() == '':
            #使用token 验证成功
            print 'request.get_data() is kongkongong'

            if request.headers.has_key('Authorization') is False :
                return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

            auth = request.headers['Authorization']
            username = verify_auth_token(auth)
            if username is None :
                return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

            return ret_func('00000', 'token login', '')


        inJsonData = json.loads(request.get_data())
        username   = inJsonData['username']
        md5_password   = inJsonData['password']

        #<todo>验证密码

        token = generate_auth_token(username)

        return ret_func('00000', 'passwd login', {'token':token})



