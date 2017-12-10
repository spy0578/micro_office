# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblChargerCommand, TblChargerCommandH, TblChargerInfo, TblCharging, TblChargingH,TblAcctInfo, TblChrgGrpInfo, TblChrgCommand 
from db.dbinit import DBSession
from db.redis_init import GlobalRedisAccess, g_rds_access
from base.log import Log, g_log
import json
import functools
from apis.api_comm import *
from datetime import datetime,timedelta  
from base.comm_const import *
import random
import sys

'''
功能：充电中信息查询
输入
user_id
session_id
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session


        inJsonData = json.loads(request.get_data())
        session_id = inJsonData['session_id']
        user_id = inJsonData['user_id']


        log_data = {
            'user_id' : user_id,
            'service' : 'start_charging',
           }


        now = datetime.datetime.now()

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




        if charger_info.charger_auth == '1': #已授权
            if charger_info.charger_stat == '02':
                ret = add_command(charger_info.charger_id, '0', const.COMMAND_CHARGING)
                return ret_func_for_app(ret, '', {}, log_data)
            elif charger_info.charger_stat == '01':
                return ret_func_for_app(const.RET_NOT_CONNECT, '请将充电枪连接汽车', {}, log_data)
            else :
                return ret_func_for_app(const.RET_STST_ERROR, '充电桩状态异常', {}, log_data)
        else : #未授权
            return ret_func_for_app(const.RET_CHARGER_UNAUTH, '请进行扫码充电', {}, log_data)

