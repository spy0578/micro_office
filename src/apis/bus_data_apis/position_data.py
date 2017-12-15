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
genre_dict = [
    {
        "id":"1",
        "genre":"喜剧"
    },
    {
        "id":"2",
        "genre":"文艺"
    },   
    {
        "id":"3",
        "genre":"动作"
    },   
    {
        "id":"4",
        "genre":"爱情"
    },      
]

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session

        log.info('request.get_data():[%s]' % request.get_data())
        log.info('user_get_info post')

        return True, {}, ret_func(const.RET_SUCCESS, '', 'post')
    
class BaseGetClass(MethodView):    
    @staticmethod
    def get():
        log=g_log.get_sys_log()
        db_session = g.db_session

        log.info('request.get_data():[%s]' % request.get_data())
        log.info('user_get_info get')

        ol_log_info = {"user_id":"111", "service":"user_get_info"}

        #返回给request_route_handler的get方法
        return True, {}, ret_func(const.RET_SUCCESS, '', genre_dict)
