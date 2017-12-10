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
���ܣ����
1 app���ͳ�������server
2 ���session_id
3 server�鿴���׮��Ϣ��������Ȩ����ת��4����û�У��򷵻ظ�app�������������ͳ��׮
4 �鿴���׮״̬�����������ӣ�����ָ����м�����ָ���������״̬���򷵻���Ӧ������Ϣ
���룺
user_id
session_id
ָ��
'''

class charging(MethodView):
    def post(slef):
        inJsonData = json.loads(request.get_data())
        user_id = inJsonData['user_id']
        session_id = inJsonData['session_id']
        command = inJsonData['command']
        log=g_log.get_sys_log()
        now = datetime.datetime.now()
        try:
            db_session = DBSession()
            check_ret = check_session_id(user_id, session_id)
            if check_ret == const.REDIS_SESSION_ID_CORRECT :
                charging_info = db_session.query(TblCharging).filter(TblCharging.user_id == user_id).first()
                if charging_info:
                    charger_info = db_session.query(TblChargerInfo).filter(TblChargerInfo.charger_id == charging_info.charger_id).first()
                    if charger_info.charger_auth == '1':              
                        #���׮״̬��������
                        if charger_info.charger_stat == '02':
                            print "11111111111"
                            ret = add_command(charger_info.charger_id, '0', const.COMMAND_CHARGING)
                            if ret == const.RET_SUCCESS:
                            	db_session.commit()
                            	return ret_func(const.RET_SUCCESS, '', {})
                            else:
                            	return ret_func(ret, '', {})
                        #���׮״̬��δ����
                        if charger_info.charger_stat == '01':
                            '''
                            ����app�뽫ǹ��������
                            '''
                    else:
                    	'''
                    	����app������Ȩ
                    	'''    

                else:
                    '''
                    ����app������Ȩ
                    '''  
            else:
                return ret_func(check_ret, '', {})
        except SQLAlchemyError, e:
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_DB_ERROR, '', {})
        except RedisError, e:
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_MEMDB_ERROR, '', {})
        finally :
            db_session.close()
        
        
