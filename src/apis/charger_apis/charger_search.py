# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblChargerCommand, TblChargerCommandH, TblChargerInfo, TblCharging, TblChargingH
from db.dbinit import DBSession
from db.redis_init import GlobalRedisAccess, g_rds_access
from base.log import Log, g_log
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
功能：将某一城市的充电点按离用户的当前位置从近到远返回给app。
输入：城市名
      lat
      lon
输出：
'''
class BasePostClass(MethodView):
    @staticmethod
    def post():
        inJsonData = json.loads(request.get_data())
        city = inJsonData['city']
        lat = inJsonData['lat']
        lon = inJsonData['lon']
        log=g_log.get_sys_log()
        now = datetime.datetime.now()
        db_session = g.db_session
        data = []
        group_info = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.city == city).all()
        for instance in group_info:
            ele = dict()
            ele['id'] = instance.charger_group_id
            ele['name'] = instance.address
            location = str(instance.city) + str(instance.district)
            ele['location'] = location
            ele['lat'] = float(instance.latitude)
            ele['lon'] = float(instance.longtitude)
            distance = getDistance(lon, lat, instance.longtitude, instance.latitude)
            ele['distance'] = distance
            data.append(ele)
        print data
        new_data = sorted(data,key = lambda e:e.__getitem__('distance'))
        print new_data
        return ret_func(const.RET_SUCCESS, '', new_data)

