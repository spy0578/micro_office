# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from flask.views import MethodView
import datetime
from base.comm_const import *
from apis.api_comm import *
from db.dborm.dborm import TblFindHtmlInfo
from base.log import Log, g_log
from db.dbinit import DBSession
from db.redis_init import GlobalRedisAccess, g_rds_access

'''
功能：获取发现里面的图片和文档url，并返回给app,当点击发现时，调用此接口。
输入：无。
输出：发现的list.二维数组
'''
class BasePostClass(MethodView):
    @staticmethod
    def post():
        db_session = g.db_session
        now = datetime.datetime.now()
        data_list = []
        find_info = db_session.query(TblFindHtmlInfo).order_by(TblFindHtmlInfo.group_id).all()
        count = 1
        data_inn_list = []
        for instance in find_info:
            #print instance.group_id
            if instance.group_id == count:
                #print instance.group_id
                #print instance.id
                data = {
                        'id'  : instance.inner_id,
                        'image' : const.IMAGE_PATH + str(instance.image),
                        'html'  : const.HTML_PATH + str(instance.html)
                        }
                data_inn_list.append(data)
            else:
                #print "2222222"
                #print instance.group_id
                #print instance.id
                data_list.append(data_inn_list)
                #print data_inn_list
                data_inn_list = []
                print "reset"
                #print data_inn_list
                count = instance.group_id
                #print count
                data = {
                        'id'  : instance.inner_id,
                        'image' : const.IMAGE_PATH + str(instance.image),
                        'html'  : const.HTML_PATH + str(instance.html)
                        }
                data_inn_list.append(data)
        print data_inn_list
        data_list.append(data_inn_list)
        return ret_func(const.RET_SUCCESS, '', data_list)

