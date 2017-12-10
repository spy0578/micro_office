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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DBAPIError
from redis.exceptions import RedisError
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
功能：充电中信息查询
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
        print type(parameters)

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
                    'service' : 'charging_get_info',
                   }



        now = datetime.datetime.now()

        check_ret = check_session_id(user_id, session_id)
        if check_ret is not const.REDIS_SESSION_ID_CORRECT :
            return ret_func_for_app(check_ret, '', {}, log_data)
        print '11111111111111'

        charging = db_session.query(TblCharging).filter(TblCharging.user_id == user_id,
                                                        TblCharging.record_stat  == const.RECORD_AVA).first()
            
        if charging is None:
            return ret_func(const.RET_CHARGER_UNAUTH, '充电桩与汽车断开连接', {})


        charger_info = db_session.query(TblChargerInfo).filter(TblChargerInfo.charger_id == charging.charger_id,
                                                               TblChargerInfo.record_stat   == const.RECORD_AVA).first()
        if charger_info is None:
            return ret_func(const.RET_DB_ERROR, '充电桩表查询无数据', {})



        print '2222222222222'
        acct_info = db_session.query(TblAcctInfo).filter(TblAcctInfo.user_id  == user_id,
                                                         TblAcctInfo.record_stat == const.RECORD_AVA).first()
        print acct_info 
        if acct_info is None :
            return ret_func_for_app(const.RET_DB_ERROR, '', {}, log_data)

        
        print '3333333333333'
        charger_group = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.charger_group_id == charger_info.charger_group_id,
                                                                TblChrgGrpInfo.record_stat == const.RECORD_AVA).first()
        if charger_group is None :
            return ret_func_for_app(const.RET_DB_ERROR, '', {}, log_data)


        
        
        expect_charging_time = 0
        expect_finish_dttm = ''
        charging_tm = ''
        charging_elec = 0
        charging_fee = 0.0

        print 'TblChargerInfo.charger_stat:[%s]' % charger_info.charger_stat
        print 'TblChargerInfo.charger_auth:[%s]' % charger_info.charger_auth
        '''
          充电结束   查询充电历史表中最新的记录
        '''
        '''
        if charger_info.charger_stat != const.CHARGER_STAT_CHARGING :
            charging_h = db_session.query(TblChargingH).filter(TblChargingH.charger_id == charger_info.charger_id,
                                                              TblChargingH.record_stat == const.RECORD_AVA).order_by(TblChargingH.last_upd_dttm.desc()).first()
            print 'charging_h.serial_num[%d]' % charging_h.serial_num


            charging_tm = str(charging_h.end_dttm - charging_h.start_dttm)
            charging_elec = charging_h.curr_elec - charging_h.init_elec


            ret_code = const.RET_CHARGING_FINISH
        '''

        fault_flag = False
        ret_code='' 
        desc=''
        print 'const.CHARGER_STAT_CONNECT_CAR:[%s]' % const.CHARGER_STAT_CONNECT_CAR
        print 'const.AUTHORIZATION:[%s]' % const.AUTHORIZATION

        if charger_info.charger_stat == const.CHARGER_STAT_CHARGING and charger_info.charger_auth == const.AUTHORIZATION :
            '''
             充电中
            '''
            ret_code = const.RET_SUCCESS
            desc = '充电中'
        #elif charger_info.charger_stat == const.CHARGER_STAT_CONNECT_CAR and charger_info.charger_auth == const.AUTHORIZATION :
        elif charger_info.charger_stat == '02' and charger_info.charger_auth == '1' :
            '''
             开始充电准备中
            '''
            ret_code = const.RET_STARTING_CHARGING
            desc = '开始充电准备中'
        else :
            '''
             充电桩故障
            '''
            ret_code = const.RET_IN_FAULT
            fault_flag = True
            desc = '充电桩故障'

        print desc


        if fault_flag is False:

            if charger_info.soc != 0 and charger_info.battery_capacity != 0 and charger_info.kw_value != 0:
                #充电时间 = 电压 * 容量 * SOC / 功率
                expect_charging_time = charger_info.vlotage_value * 10 * charger_info.battery_capacity * charger_info.soc * 0.01 / charger_info.kw_value * 100

            print 'expect_charging_time:[%d]' % expect_charging_time
            expect_finish_dttm = now + timedelta(hours=expect_charging_time)  
            print expect_finish_dttm



            #已充电时长
            if charging.start_dttm is not const.DEFAULT_TIMEDATE_STR :
                charging_tm = str(now - charging.start_dttm)
            #已充电电量
            charging_elec = charger_info.elec_value - charging.init_elec



            print 'charging_tm:[%s]' % charging_tm
            print 'charging_elec:[%d]' % charging_elec
            print 'charging_fee:[%f]' % charging_fee
            print 'charger_group.elec_cost + charger_group.addt_cost:[%f]' % (charger_group.elec_cost + charger_group.addt_cost)

            charging_fee = float(charging_elec) / 100.0 * float(charger_group.elec_cost + charger_group.addt_cost)


        data = {
                'bal'                 : str(acct_info.bal), 
                'charger_id'          : charger_info.charger_id, 
                'charger_kw'          : str(charger_info.kw_value), 
                'elec_cost'           : str(charger_group.elec_cost),
                'addt_cost'           : str(charger_group.addt_cost),
                'expect_charging_time': str(expect_charging_time),
                'expect_finish_dttm'  : str(expect_finish_dttm),
                'charger_stat'        : str(charger_info.charger_stat),
                'charger_auth'        : str(charger_info.charger_auth),
                'charging_tm'         : str(charging_tm),
                'charging_elec'       : str(charging_elec),
                'charging_fee'        : str(charging_fee),
                
                }

        print data

        log_data = {
            'user_id' : user_id,
            'charger_id' : charger_info.charger_id,
            'service' : 'charging_get_info',
                }


        return ret_func_for_app(ret_code, desc, data, log_data)

