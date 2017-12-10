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
功能：停止充电
1 app将停止充电指令发给server
2 server收到指令，在指令表中添加指令
3 将本次充电的信息返回给app，本次充电结束
输入：
user_id
sesion_id
command
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        inJsonData = json.loads(request.get_data())
        user_id = inJsonData['user_id']
        session_id = inJsonData['session_id']
        log=g_log.get_sys_log()
        now = datetime.datetime.now()
        db_session = g.db_session

        log_data = {
                'user_id' : user_id,
                'service' : 'start_charging',
                   }

        check_ret = check_session_id(user_id, session_id)
        if check_ret is not const.REDIS_SESSION_ID_CORRECT :
            return ret_func_for_app(check_ret, '', {}, log_data)


        charging = db_session.query(TblCharging).filter(TblCharging.user_id == user_id,
                                                                TblCharging.record_stat  == const.RECORD_AVA).first()

        if charging is None:
            return ret_func_for_app(const.RET_DB_ERROR, '充电表查询无数据', {}, log_data)


        log_data = {
                'user_id' : user_id,
                'service' : 'start_charging',
                'charger_id' : charging.charger_id,
                   }



        charger_info = db_session.query(TblChargerInfo).filter(TblChargerInfo.charger_id == charging.charger_id,
                                                               TblChargerInfo.record_stat   == const.RECORD_AVA).first()

        if charger_info is None:
            return ret_func_for_app(const.RET_DB_ERROR, '充电桩表查询无数据', {}, log_data)


        '''
          无条件 停止充电
        '''
        ret = add_command(charger_info.charger_id, '0', const.COMMAND_STOP_CHARGING)
        return ret_func_for_app(ret, '', {}, log_data)

