# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import MsgVerCode, UserPasswdInfo, UserLoginInfo, UserBasicInfo, NoteTmplInfo, chargingInfoH
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
功能：接收充电桩心跳的报文，根据充电桩的状态和之前一次的状态，根据这两个状态的对比，进行不同的操作。

输入：
charger_id
charger_stat:充电桩状态
charger_time：充电桩时间
elec_value：电表度数
voltage_value：电压值
current_value:电流值
kw_value:功率值
SOC：充电百分比（直流）
battery_capacity：电池容量（直流）
输出：
作者：郑哲渊
'''

class heart_beat(MethodView):
    def get(self, charger_id, charger_stat, charger_time, elec_value, voltage_value, current_value, kw_value, SOC, battery_capacity):
        log=g_log.get_sys_log()
        '''
        inJsonData = json.loads(request.get_data())
        charger_id = inJsonData['charger_id']
        charger_stat = inJsonData['charger_stat']
        charger_time = inJsonData['charger_time']
        elec_value = inJsonData['elec_value']
        vlotage_value = inJsonData['vlotage_value']
        current_value = inJsonData['current_value']
        kw_value = inJsonData['kw_value']
        SOC = inJsonData['SOC']
        battery_capacity = inJsonData['battery_capacity']
        '''
        now = datetime.datetime.now()
        try:
            db_session = DBSession()
            charger_info = db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).first()
            #datetime转换成string
            charger_info_time = charger_info.upd_dttm.strftime('%Y%m%d%H%M%S')
            print "time is %s" % charger_info_time
            if charger_time <= charger_info_time:
                print "11111111111"
                return ret_func(const.RET_SUCCESS, '', {})
            recent_stat = charger_info.charger_stat
            #当前状态是未连接
            if charger_stat == '01':
                #是否存在偷电行为
                ret = check_elec_value(charger_id, elec_value)
                if ret == const.RET_FALUT_IN_CHARGE:
                    '''
                    告知server存在偷电行为
                    '''
                    print "3333"
                    return ret_func(ret, '', {})
                #表中状态是未连接
                if recent_stat == '01':
                    print "in 0101"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_AUTHORIZATION, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })   
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是已连接
                if recent_stat == '02':
                    print "in 0102"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                        '''
                        推送给app请重新连接充电桩
                        '''
                    #查看充电表中是否有记录
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        charge_history = chargingInfoH(charger_id      = charger_info.charger_id,
                                                       user_id         = charger_info.user_id,
                                                       init_elec       = charger_info.init_elec,
                                                       curr_elec       = charger_info.curr_elec,
                                                       total_elec      = charger_info.curr_elec - charger_info.init_elec,
                                                       start_charge_dt = charger_info.start_charge_dt,
                                                       end_charge_dt   = charger_info.end_charge_dt,
                                                       crt_dttm        = charger_info.crt_dttm,
                                                       upd_dttm        = charger_info.upd_dttm,
                                                       remark          = charger_info.remark,
                                                       rec_stat        = charger_info.rec_stat)
                        db_session.add(charge_history)
                        db_session.flush()
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).delete()
                        db_session.flush()
                    else:
                        '''
                        推送给app请重新连接充电桩
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是充电
                if recent_stat == '03':
                    print "in 0103"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                    #若没有指令，表示是直接拔掉的，所以要返回给app
                    else:
                        '''
                        推送给app已停止充电，本次充电的各种信息
                        '''
                    #查看充电表中是否有记录
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        charge_history = chargingInfoH(charger_id      = charger_info.charger_id,
                                                       user_id         = charger_info.user_id,
                                                       init_elec       = charger_info.init_elec,
                                                       curr_elec       = charger_info.curr_elec,
                                                       total_elec      = charger_info.curr_elec - charger_info.init_elec,
                                                       start_charge_dt = charger_info.start_charge_dt,
                                                       end_charge_dt   = now,     #充电中直接拔掉枪，所以停止充电时间为现在
                                                       crt_dttm        = charger_info.crt_dttm,
                                                       upd_dttm        = charger_info.upd_dttm,
                                                       remark          = charger_info.remark,
                                                       rec_stat        = charger_info.rec_stat)
                        db_session.add(charge_history)
                        db_session.flush()
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).delete()
                        db_session.flush()
                    else:
                        '''
                        推送给app请重新连接充电桩
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是故障、初始化等
                else:
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
            #当前状态是已连接
            if charger_stat == '02':
                #是否存在偷电行为
                ret = check_elec_value(charger_id, elec_value)
                if ret == const.RET_FALUT_IN_CHARGE:
                    '''
                    告知server存在偷电行为
                    '''
                #表中状态是未连接或者枪未插入锁槽故障
                if (recent_stat == '01') or (recent_stat == '30'):
                    print "in 0201"
                    #查看充电表中是否有记录
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({
                                                                                                     ChargingInfo.init_elec  :elec_value,
                                                                                                     ChargingInfo.curr_elec  :elec_value,
                                                                                                     ChargingInfo.crt_dttm   :now,
                                                                                                     ChargingInfo.upd_dttm   :now
                                                                                                     })
                        db_session.flush()
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是已连接
                if recent_stat == '02':
                    print "in 0202"
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({
                                                                                                     ChargingInfo.curr_elec  :elec_value,
                                                                                                     ChargingInfo.upd_dttm   :now
                                                                                                     })
                        db_session.flush()
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是充电
                if recent_stat == '03':
                    print "in 0203"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })                       
                        db_session.flush()
                    else:
                        '''
                        返回给app已充满，并把充电信息给app
                        '''
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({
                                                                                                     ChargingInfo.curr_elec     :elec_value,
                                                                                                     ChargingInfo.end_charge_dt :now,
                                                                                                     ChargingInfo.upd_dttm      :now
                                                                                                     })
                        db_session.flush()
                    else:
                        '''
                        返回给app存在异常，请重新扫码
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #状态为故障
                else:
                    '''
                    返回给app：当前充电桩故障，请选择附近充电桩
                    '''
            #当前状态是充电
            if charger_stat == '03':
                #表中状态是已连接
                if recent_stat == '02':
                    print "in 0302"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })                       
                        db_session.flush()
                        charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                        degrees = elec_value - charging_info.curr_elec
                        #计费
                        ret = cost(charging_info.user_id, charger_id, degrees)
                        print "ret =====%s" % ret
                        if ret == const.RET_BAL_IS_NONE:
                            '''
                            返回给app余额为0，请尽快充值，本次充电结束
                            '''
                        if ret == const.RET_SUCCESS:
                            chargeing_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                            if charging_info:
                                db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({
                                                                                                     ChargingInfo.curr_elec  :elec_value,
                                                                                                     ChargingInfo.upd_dttm   :now
                                                                                                     })
                                db_session.flush()
                            db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                            db_session.flush()
                            db_session.commit()
                            return ret_func(const.RET_SUCCESS, '', {})
                        #计费报其他问题
                        else:
                            '''
                            返回给app充电异常，请重新连接充电桩
                            '''
                    #没有充电指令
                    else:
                        charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                        degrees = float(elec_value) - charging_info.curr_elec
                        #计费
                        ret = cost(charging_info.user_id, charger_id, degrees)
                        if ret == const.RET_ACCOUNT_ID_NOT_EXIST:
                            '''
                            返回给app还未绑定现金帐户
                            '''
                            return ret_func(const.RET_ACCOUNT_ID_NOT_EXIST,'', {})
                        if ret == const.RET_BAL_IS_NONE:
                            '''
                            返回给app余额为0，请尽快充值，本次充电结束
                            '''
                            return ret_func(const.RET_BAL_IS_NONE,'', {})
                        if ret == const.RET_AREA_INFO_NOT_EXIST:
                            return ret_func(const.RET_AREA_INFO_NOT_EXIST, '', {})
                        
                        #停止充电
                        add_command(charger_id, '1', const.COMMAND_STOP_CHARGING)
                        '''
                        返回给app此充电桩发生异常，请连接附近充电桩
                        '''
                        #更新充电表，结束时间为现在时间
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({   
                                                                                                     ChargingInfo.curr_elec     :elec_value,
                                                                                                     ChargingInfo.end_charge_dt :now,
                                                                                                     ChargingInfo.upd_dttm      :now
                                                                                                     })
                        db_session.flush()
                        #充电桩状态改为盗电异常
                        db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :'21',
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                        db_session.flush()
                        db_session.commit()
                        return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是充电中
                if recent_stat == '03':
                    print "in 0303"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })                       
                        db_session.flush()
                        charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                        #添加停止充电指令
                        add_command(charger_id, '1', const.COMMAND_STOP_CHARGING)
                    #计费
                    charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    degrees = float(elec_value) - charging_info.curr_elec
                    ret = cost(charging_info.user_id, charger_id, degrees)
                    if ret == const.RET_BAL_IS_NONE:
                        '''
                        返回给app余额为0，请尽快充值，本次充电结束
                        '''
                        return ret_func(const.RET_BAL_IS_NONE, '', {})
                    if ret == const.RET_SUCCESS:
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({   
                                                                                                     ChargingInfo.curr_elec     :elec_value,
                                                                                                     ChargingInfo.upd_dttm      :now
                                                                                                     })
                        db_session.flush()
                        db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                        db_session.flush()
                        db_session.commit()
                        return ret_func(const.RET_SUCCESS, '', {})
                    else:
                        return ret_func(ret, '', {})
                #表中状态是故障或未连接
                else:
                    '''
                    返回给server异常充电，建议有张异常充电表
                    '''
                    #停止充电
                    add_command(charger_id, '1', const.COMMAND_STOP_CHARGING)
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :'21',
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_CHARGE_ERROR, '', {})
            #当前状态是枪未插入锁槽
            if charger_stat == '30':
                #是否存在偷电行为
                ret = check_elec_value(charger_id, elec_value)
                if ret == const.RET_FALUT_IN_CHARGE:
                    '''
                    告知server存在偷电行为
                    '''
                    return ret_func(const.RET_FALUT_IN_CHARGE, '', {})
                #表中状态是未连接或枪未插入锁槽故障
                if (recent_stat == '30') or (recent_stat == '01'):
                    '''
                    不做处理
                    '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是已连接
                if recent_stat == '02':
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                        '''
                        推送给app请重新连接充电桩
                        '''
                    #查看充电表中是否有记录
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        charge_history = chargingInfoH(charger_id      = charger_info.charger_id,
                                                       user_id         = charger_info.user_id,
                                                       init_elec       = charger_info.init_elec,
                                                       curr_elec       = charger_info.curr_elec,
                                                       total_elec      = charger_info.curr_elec - charger_info.init_elec,
                                                       start_charge_dt = charger_info.start_charge_dt,
                                                       end_charge_dt   = charger_info.end_charge_dt,
                                                       crt_dttm        = charger_info.crt_dttm,
                                                       upd_dttm        = charger_info.upd_dttm,
                                                       remark          = charger_info.remark,
                                                       rec_stat        = charger_info.rec_stat)
                        db_session.add(charge_history)
                        db_session.flush()
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).delete()
                        db_session.flush()
                    else:
                        '''
                        推送给app请重新连接充电桩
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #表中状态是充电
                if recent_stat == '03':
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                    #若没有指令，表示是直接拔掉的，所以要返回给app
                    else:
                        '''
                        推送给app已停止充电，本次充电的各种信息
                        '''
                    #查看充电表中是否有记录
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        charge_history = chargingInfoH(charger_id      = charger_info.charger_id,
                                                       user_id         = charger_info.user_id,
                                                       init_elec       = charger_info.init_elec,
                                                       curr_elec       = charger_info.curr_elec,
                                                       total_elec      = charger_info.curr_elec - charger_info.init_elec,
                                                       start_charge_dt = charger_info.start_charge_dt,
                                                       end_charge_dt   = now,     #充电中直接拔掉枪，所以停止充电时间为现在
                                                       crt_dttm        = charger_info.crt_dttm,
                                                       upd_dttm        = charger_info.upd_dttm,
                                                       remark          = charger_info.remark,
                                                       rec_stat        = charger_info.rec_stat)
                        db_session.add(charge_history)
                        db_session.flush()
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).delete()
                        db_session.flush()
                    else:
                        '''
                        报错，推送给app请重新连接充电桩
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
            '''
            检查指令表中有无未发送的指令，若有，则返回给充电桩，若没有，则返回给充电桩控指令
            '''
        except SQLAlchemyError, e :
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_DB_ERROR, '', {})
        finally:
            db_session.close()
