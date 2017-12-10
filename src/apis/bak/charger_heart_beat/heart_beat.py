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
���ܣ����ճ��׮�����ı��ģ����ݳ��׮��״̬��֮ǰһ�ε�״̬������������״̬�ĶԱȣ����в�ͬ�Ĳ�����

���룺
charger_id
charger_stat:���׮״̬
charger_time�����׮ʱ��
elec_value��������
voltage_value����ѹֵ
current_value:����ֵ
kw_value:����ֵ
SOC�����ٷֱȣ�ֱ����
battery_capacity�����������ֱ����
�����
���ߣ�֣��Ԩ
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
            #datetimeת����string
            charger_info_time = charger_info.upd_dttm.strftime('%Y%m%d%H%M%S')
            print "time is %s" % charger_info_time
            if charger_time <= charger_info_time:
                print "11111111111"
                return ret_func(const.RET_SUCCESS, '', {})
            recent_stat = charger_info.charger_stat
            #��ǰ״̬��δ����
            if charger_stat == '01':
                #�Ƿ����͵����Ϊ
                ret = check_elec_value(charger_id, elec_value)
                if ret == const.RET_FALUT_IN_CHARGE:
                    '''
                    ��֪server����͵����Ϊ
                    '''
                    print "3333"
                    return ret_func(ret, '', {})
                #����״̬��δ����
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
                #����״̬��������
                if recent_stat == '02':
                    print "in 0102"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                        '''
                        ���͸�app���������ӳ��׮
                        '''
                    #�鿴�������Ƿ��м�¼
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
                        ���͸�app���������ӳ��׮
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #����״̬�ǳ��
                if recent_stat == '03':
                    print "in 0103"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                    #��û��ָ���ʾ��ֱ�Ӱε��ģ�����Ҫ���ظ�app
                    else:
                        '''
                        ���͸�app��ֹͣ��磬���γ��ĸ�����Ϣ
                        '''
                    #�鿴�������Ƿ��м�¼
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        charge_history = chargingInfoH(charger_id      = charger_info.charger_id,
                                                       user_id         = charger_info.user_id,
                                                       init_elec       = charger_info.init_elec,
                                                       curr_elec       = charger_info.curr_elec,
                                                       total_elec      = charger_info.curr_elec - charger_info.init_elec,
                                                       start_charge_dt = charger_info.start_charge_dt,
                                                       end_charge_dt   = now,     #�����ֱ�Ӱε�ǹ������ֹͣ���ʱ��Ϊ����
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
                        ���͸�app���������ӳ��׮
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #����״̬�ǹ��ϡ���ʼ����
                else:
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
            #��ǰ״̬��������
            if charger_stat == '02':
                #�Ƿ����͵����Ϊ
                ret = check_elec_value(charger_id, elec_value)
                if ret == const.RET_FALUT_IN_CHARGE:
                    '''
                    ��֪server����͵����Ϊ
                    '''
                #����״̬��δ���ӻ���ǹδ�������۹���
                if (recent_stat == '01') or (recent_stat == '30'):
                    print "in 0201"
                    #�鿴�������Ƿ��м�¼
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
                #����״̬��������
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
                #����״̬�ǳ��
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
                        ���ظ�app�ѳ��������ѳ����Ϣ��app
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
                        ���ظ�app�����쳣��������ɨ��
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #״̬Ϊ����
                else:
                    '''
                    ���ظ�app����ǰ���׮���ϣ���ѡ�񸽽����׮
                    '''
            #��ǰ״̬�ǳ��
            if charger_stat == '03':
                #����״̬��������
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
                        #�Ʒ�
                        ret = cost(charging_info.user_id, charger_id, degrees)
                        print "ret =====%s" % ret
                        if ret == const.RET_BAL_IS_NONE:
                            '''
                            ���ظ�app���Ϊ0���뾡���ֵ�����γ�����
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
                        #�Ʒѱ���������
                        else:
                            '''
                            ���ظ�app����쳣�����������ӳ��׮
                            '''
                    #û�г��ָ��
                    else:
                        charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                        degrees = float(elec_value) - charging_info.curr_elec
                        #�Ʒ�
                        ret = cost(charging_info.user_id, charger_id, degrees)
                        if ret == const.RET_ACCOUNT_ID_NOT_EXIST:
                            '''
                            ���ظ�app��δ���ֽ��ʻ�
                            '''
                            return ret_func(const.RET_ACCOUNT_ID_NOT_EXIST,'', {})
                        if ret == const.RET_BAL_IS_NONE:
                            '''
                            ���ظ�app���Ϊ0���뾡���ֵ�����γ�����
                            '''
                            return ret_func(const.RET_BAL_IS_NONE,'', {})
                        if ret == const.RET_AREA_INFO_NOT_EXIST:
                            return ret_func(const.RET_AREA_INFO_NOT_EXIST, '', {})
                        
                        #ֹͣ���
                        add_command(charger_id, '1', const.COMMAND_STOP_CHARGING)
                        '''
                        ���ظ�app�˳��׮�����쳣�������Ӹ������׮
                        '''
                        #���³�������ʱ��Ϊ����ʱ��
                        db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).update({   
                                                                                                     ChargingInfo.curr_elec     :elec_value,
                                                                                                     ChargingInfo.end_charge_dt :now,
                                                                                                     ChargingInfo.upd_dttm      :now
                                                                                                     })
                        db_session.flush()
                        #���׮״̬��Ϊ�����쳣
                        db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :'21',
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                        db_session.flush()
                        db_session.commit()
                        return ret_func(const.RET_SUCCESS, '', {})
                #����״̬�ǳ����
                if recent_stat == '03':
                    print "in 0303"
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })                       
                        db_session.flush()
                        charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                        #���ֹͣ���ָ��
                        add_command(charger_id, '1', const.COMMAND_STOP_CHARGING)
                    #�Ʒ�
                    charging_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    degrees = float(elec_value) - charging_info.curr_elec
                    ret = cost(charging_info.user_id, charger_id, degrees)
                    if ret == const.RET_BAL_IS_NONE:
                        '''
                        ���ظ�app���Ϊ0���뾡���ֵ�����γ�����
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
                #����״̬�ǹ��ϻ�δ����
                else:
                    '''
                    ���ظ�server�쳣��磬���������쳣����
                    '''
                    #ֹͣ���
                    add_command(charger_id, '1', const.COMMAND_STOP_CHARGING)
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :'21',
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_CHARGE_ERROR, '', {})
            #��ǰ״̬��ǹδ��������
            if charger_stat == '30':
                #�Ƿ����͵����Ϊ
                ret = check_elec_value(charger_id, elec_value)
                if ret == const.RET_FALUT_IN_CHARGE:
                    '''
                    ��֪server����͵����Ϊ
                    '''
                    return ret_func(const.RET_FALUT_IN_CHARGE, '', {})
                #����״̬��δ���ӻ�ǹδ�������۹���
                if (recent_stat == '30') or (recent_stat == '01'):
                    '''
                    ��������
                    '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #����״̬��������
                if recent_stat == '02':
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                        '''
                        ���͸�app���������ӳ��׮
                        '''
                    #�鿴�������Ƿ��м�¼
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
                        ���͸�app���������ӳ��׮
                        '''
                    db_session.query(ChargerInfo).filter(ChargerInfo.charger_id == charger_id).update({
                                                                                               ChargerInfo.charger_stat  :charger_stat,
                                                                                               ChargerInfo.elec_value    :elec_value,
                                                                                               ChargerInfo.upd_dttm      :charger_time 
                                                                                                })
                    db_session.flush()
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                #����״̬�ǳ��
                if recent_stat == '03':
                    command_info = db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id, ChargerCommand.command == const.COMMAND_STOP_CHARGING, ChargerCommand.stat == '1').first()
                    if command_info:
                        db_session.query(ChargerCommand).filter(ChargerCommand.charger_id == charger_id).update({
                                                                                                         ChargerCommand.stat   :'2'
                                                                                                         })
                    #��û��ָ���ʾ��ֱ�Ӱε��ģ�����Ҫ���ظ�app
                    else:
                        '''
                        ���͸�app��ֹͣ��磬���γ��ĸ�����Ϣ
                        '''
                    #�鿴�������Ƿ��м�¼
                    charger_info = db_session.query(ChargingInfo).filter(ChargingInfo.charger_id == charger_id).first()
                    if charger_info:
                        charge_history = chargingInfoH(charger_id      = charger_info.charger_id,
                                                       user_id         = charger_info.user_id,
                                                       init_elec       = charger_info.init_elec,
                                                       curr_elec       = charger_info.curr_elec,
                                                       total_elec      = charger_info.curr_elec - charger_info.init_elec,
                                                       start_charge_dt = charger_info.start_charge_dt,
                                                       end_charge_dt   = now,     #�����ֱ�Ӱε�ǹ������ֹͣ���ʱ��Ϊ����
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
                        �������͸�app���������ӳ��׮
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
            ���ָ���������δ���͵�ָ����У��򷵻ظ����׮����û�У��򷵻ظ����׮��ָ��
            '''
        except SQLAlchemyError, e :
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_DB_ERROR, '', {})
        finally:
            db_session.close()
