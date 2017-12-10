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

'''
功能：作为一般登录的入口
输入：user_id
      session_id
输出：home_html
      find_html
      avatar
      province
      city
      district
      gender
      car_number
      car_informati
      name
      nickname
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g.log
        db_session = g.db_session

        log.info('request.get_data():[%s]' % request.get_data())
        log.info('user_get_info post')

        return True, ret_func(const.RET_SUCCESS, '', 'post')
    
class BaseGetClass(MethodView):    
    @staticmethod
    def get():
        log=g.log
        db_session = g.db_session

        log.info('request.get_data():[%s]' % request.get_data())
        log.info('user_get_info get')

        return True, ret_func(const.RET_SUCCESS, '', 'get')
