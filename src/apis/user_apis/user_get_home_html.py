# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from flask.views import MethodView
import datetime
from base.comm_const import *
from apis.api_comm import *
from db.dborm.dborm import TblHomeHtmlInfo
from base.log import Log, g_log
from db.dbinit import DBSession
from db.redis_init import GlobalRedisAccess, g_rds_access

'''
功能：获取主页轮播图，并返回给app,当未登录时，调用此接口。
输入：无。
输出：轮播图的list.
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        db_session = g.db_session
        now = datetime.datetime.now()
        home_html_info = db_session.query(TblHomeHtmlInfo).all()
        data_list = []
        for instance in home_html_info:
            data = {
                    'image'   : const.IMAGE_PATH + str(instance.image),
                    'html'    : const.HTML_PATH + str(instance.html)
                    }
            data_list.append(data)
        return ret_func(const.RET_SUCCESS, '', data_list)
