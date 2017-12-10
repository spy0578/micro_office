# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack, render_template
from db.dborm.dborm import MsgVerCode, UserPasswdInfo, UserLoginInfo, UserBasicInfo, NoteTmplInfo
from db.dbinit import DBSession
from db.redis_init import GlobalRedisAccess, g_rds_access
from base.log import g_txn_log
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DBAPIError
from redis.exceptions import RedisError

class BaseGetClass(MethodView):
    @staticmethod
    def get(parameters):
        log=g_txn_log.get_sys_log()
        rds = g_rds_access.get_rds()
        db_session = g.db_session

        print 'get here'
        print parameters
        print g.db_session



        '''
        <todo> У�����
        '''

        return render_template('index.html')
