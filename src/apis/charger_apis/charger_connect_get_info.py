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
功能：扫码充电查询
输入
user_id
session_id
'''

class BaseGetClass(MethodView):
    @staticmethod
    def get():
        log=g_log.get_sys_log()
        db_session = g.db_session

        print 'request.args:', request.args
        parameters = request.args

        if parameters is None:
            '''
             上送报文错误
            '''
            return ret_func(const.RET_ARG_ERROR, '', {})


        '''
         分隔符为&，截取字符串
        '''
        param_dict = parameters.to_dict()

        user_id = param_dict['user_id']
        session_id = param_dict['session_id']

        print user_id
        print session_id


        log_data = {
                    'user_id' : user_id,
                    'service' : 'charger_connect_get_info',
                   }



        now = datetime.datetime.now()

        check_ret = check_session_id(user_id, session_id)
        if check_ret is not const.REDIS_SESSION_ID_CORRECT :
            return ret_func_for_app(check_ret, '', {}, log_data)
        print '11111111111111'

        charging = db_session.query(TblCharging).filter(TblCharging.user_id == user_id,
                                                        TblCharging.record_stat  == const.RECORD_AVA).first()
            
        if charging is None:
            return ret_func_for_app(const.RET_APP_UNCONNECT, 'app还未进行过扫码充电', {}, log_data)


        charger_info = db_session.query(TblChargerInfo).filter(TblChargerInfo.charger_id == charging.charger_id,
                                                               TblChargerInfo.record_stat   == const.RECORD_AVA).first()
        if charger_info is None:
            return ret_func(const.RET_DB_ERROR, '充电桩表查询无数据', {})



        data = {
                'charger_stat'        : str(charger_info.charger_stat),
                'charger_auth'        : str(charger_info.charger_auth),
                'charger_id'          : str(charger_info.charger_id),
                }

        print data

        log_data = {
                    'user_id' : user_id,
                    'charger_id' : charging.charger_id,
                    'service' : 'charger_connect_get_info',
                   }


        return ret_func_for_app(const.RET_SUCCESS, '成功', data, log_data)

