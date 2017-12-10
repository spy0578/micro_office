# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblChargerCommand, TblChargerCommandH, TblChargerInfo, TblCharging, TblChargingH,TblAcctInfo, TblChrgGrpInfo
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
功能：用户-充电桩匹配
1 app将user_id和二维码中得到的charger_id发送至server
2 检查session_id
3 server校验charger_id 对应的状态，若是未连接或轻级别故障，则添加到充电表中
4 若是其他状态，则返回相应的错误信息
输入
user_id
session_id
charger_id
作者：郑哲渊
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session

        inJsonData = json.loads(request.get_data())
        charger_id = inJsonData['charger_id']
        session_id = inJsonData['session_id']
        user_id    = inJsonData['user_id']
        print "charger_id = %s" % charger_id


        log_data = {
            'user_id' : user_id,
            'charger_id' : charger_id,
            'service' : 'charger_connect',
           }
                

        now = datetime.datetime.now()

        check_ret = check_session_id(user_id, session_id)
        if check_ret == const.REDIS_SESSION_ID_CORRECT :
            charger_info = db_session.query(TblChargerInfo).filter(TblChargerInfo.charger_id == charger_id,
                                                                   TblChargerInfo.record_stat   == const.RECORD_AVA).first()
            if charger_info:
                charger_stat = charger_info.charger_stat
                print "stat = %s" % charger_stat

                if (charger_stat == const.CHARGER_STAT_READY) or (charger_stat == const.CHARGER_STAT_CONNECT_CAR):
                    charging_info = db_session.query(TblCharging).filter(TblCharging.charger_id == charger_id, 
                                                                         TblCharging.record_stat   == const.RECORD_AVA).first()
                    if charging_info:
                        #充电桩已授权
                        return ret_func_for_app(const.RET_CHARGER_AUTH, '充电桩已授权',{}, log_data)
                    else:
                        #充电表中加记录
                        charging = TblCharging(charger_id       = charger_id,
                                                user_id         = user_id,
                                                init_elec       = 0,
                                                curr_elec       = 0,
                                                start_dttm      = const.DEFAULT_TIMEDATE_STR,
                                                end_dttm        = const.DEFAULT_TIMEDATE_STR,
                                                remark          = ' ',
                                                last_upd_dttm   = now,
                                                record_stat     = const.RECORD_AVA)
                        db_session.add(charging)
                        db_session.flush()

                        #添加枪授权指令
                        #授权动作是server端发起的
                        ret = add_command(charger_id, '1', const.COMMAND_AUTHORIZATION)

                        print '1111111111111111'
                        print ret

                        if ret != const.RET_SUCCESS :
                            return ret_func_for_app(ret, '', {}, '')


                        return ret_func_for_app(const.RET_SUCCESS, '', {}, '')

                        


                elif charger_stat == '03':
                    #返回给app此充电桩正在使用，请链接其他充电桩
                    return ret_func_for_app(const.RET_CONNECT, '', {}, '')
                else:
                    #返回给app充电桩故障，请连接其他充电桩
                    return ret_func_for_app(const.RET_IN_FAULT, '', {}, '')
            return ret_func_for_app(const.RET_SYS_ERROR, '', {}, '')
        else :
            return ret_func_for_app(check_ret, '', {}, '')       
 





class charger_connect(MethodView):
    def post(self):
        log=g_log.get_sys_log()
        inJsonData = json.loads(request.get_data())
        charger_id = inJsonData['charger_id']
        session_id = inJsonData['session_id']
        user_id = inJsonData['user_id']
        print "charger_id = %s" % charger_id
        now = datetime.datetime.now()
        try:
            db_session = DBSession()
            check_ret = check_session_id(user_id, session_id)
            if check_ret == const.REDIS_SESSION_ID_CORRECT :
                charger_info = db_session.query(TblChargerInfo).filter(TblChargerInfo.charger_id == charger_id).first()
                if not charger_info:
                    '''
                    返回给app该用户没有注册
                    '''
                #桩为已授权状态
                if charger_info.charger_auth == '1':
                    '''
                    返回给app该充电桩已授权状态
                    '''
                charger_stat = charger_info.charger_stat
                print "stat = %s" % charger_stat
                if charger_stat == '01':
                    print "22222222"
                    charging_info = db_session.query(TblCharging).filter(TblCharging.charger_id == charger_id).first()
                    print "in 11111"
                    #已存在记录
                    if charging_info:
                        #返回给app此充电桩正在使用，请链接其他充电桩
                        return ret_func(const.RET_CONNECT, '',{})
                    else:
                        #充电表中加记录
                        charging = TblCharging( charger_id  = charger_id,
                                                user_id     = user_id,
                                                init_elec   = 0,
                                                curr_elec   = 0,
                                                crt_dttm    = now,
                                                upd_dttm    = now,
                                                rec_stat    = '1')
                        db_session.add(charging)
                        db_session.flush()
                        print "333"
                        #添加授权指令
                        ret = add_command(charger_id, '1', const.COMMAND_AUTHORIZATION)
                        if ret == const.RET_SUCCESS:
                            #返回给app连接成功
                            db_session.commit()
                            return ret_func(const.RET_SUCCESS, '', {})
                        else:
                            #返回给app此充电桩有故障，请链接其他充电桩
                            return ret_func(const.RET_COMMAND_ERROR, '', {})
                else:
                    #返回给app充电桩故障，请连接其他充电桩
                    return ret_func(const.RET_STST_ERROR, '', {})
            else :
                return ret_func(check_ret, '', {})       
        except SQLAlchemyError, e :
            print type(e)
            log.debug(e)
            db_session.rollback()
            '''
            返回给app出现故障，请重新连接
            '''
        except RedisError, e:
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_MEMDB_ERROR, '', {})
        finally :
            db_session.close()
                
                    
