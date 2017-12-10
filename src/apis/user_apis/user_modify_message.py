# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblChargerCommand, TblChargerCommandH, TblChargerInfo, TblCharging, TblChargingH,TblUserBasicInfo, TblUserLoginInfo, TblUserPasswdInfo, TblMsgVerCode
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
import types
'''
功能：更换手机号或者密码
1. 验证session_id
2. 验证短信验证码表，验证码未过期、已验证过且验证码类型相同(1)，表明本次注册请求有效(防止有人恶意绕过验证码，直接发注册的报文)
3. 修改用户密码表
输入：
user_id
session_id
code_type
msg_ver_code
message:根据type，是phone_no 或者 password
输出
返回message
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session
        now = datetime.datetime.now()
        inJsonData = json.loads(request.get_data())
        user_id = inJsonData['user_id']
        session_id = inJsonData['session_id']
        code_type = inJsonData['code_type']
        msg_ver_code = inJsonData['msg_ver_code']
        message = inJsonData['message']
        check_ret = check_session_id(user_id, session_id)
        if check_ret == const.REDIS_SESSION_ID_CORRECT:
            user_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id == user_id).first()
            if user_info:
                phone_no = user_info.phone_no
            ret = check_user_code(phone_no, code_type, msg_ver_code)
            if ret == const.RET_SUCCESS:
                if code_type == const.VER_CODE_TPYE_PHONE_NO:
                    db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id == user_id).update({
                                                                                                            TblUserPasswdInfo.phone_no : message,
                                                                                                            TblUserPasswdInfo.upd_dttm : now
                                                                                                            })
                if code_type == const.VER_CODE_TPYE_PASSWD:
                    salt = random.randint(100000, 999999)
                    passwd = message + str(salt)
                    passwd = getsha256(passwd)
                    db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id == user_id).update({
                                                                                                            TblUserPasswdInfo.password : passwd,
                                                                                                            TblUserPasswdInfo.salt     : salt,
                                                                                                            TblUserPasswdInfo.upd_dttm : now
                                                                                                            })
                db_session.flush()
                db_session.commit()
                data = dict(message=message)
                return ret_func(const.RET_SUCCESS, '', data)
            else:
                return ret_func(ret, '', {})
        else:
            return ret_nunc(check_ret, '', {})
















'''

class user_modify(MethodView) :
    #log=g_log.get_sys_log()
    #rds = g_rds_access.get_rds()
    def post(self) :
        log=g_log.get_sys_log()
        inJsonData = json.loads(request.get_data())
        user_id = inJsonData['user_id']
        phone_no = inJsonData['phone_no']
        session_id = inJsonData['session_id']
        password = inJsonData['password']
        
        print "type is %s" % type(phone_no)
        print "value is %s" % phone_no
        log.debug('user_id is [%s]' % user_id)
        log.debug('password is [%s]' % password)
        now = datetime.datetime.now()
        try :
            db_session = DBSession()
            check_ret = check_session_id(user_id, session_id)
            if check_ret == REDIS_session_id_correct :
                #print "33333333"
                user_passwd_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id==user_id).first()
                #print "444444444444444444444"
                #db_session.commit()
                #print "phone number is %s" % selected_phone_no
                #print "phone type %s" % type(selected_phone_no)
                info = db_session.query(TblMsgVerCode).filter(TblMsgVerCode.phone_no == user_passwd_info.phone_no, now < TblMsgVerCode.exp_date_time, MsgVerCode.ver_code_stat == '1', TblMsgVerCode.msg_ver_type == '1').first()
                #info = db_session.execute('select * from MsgVerCode where now < MsgVerCode.exp_date_time and MsgVerCode.ver_code_stat == '1' and MsgVerCode.msg_ver_type == '1' and MsgVerCode.phone_no == (select phone_no from UserPasswdInfo where UserPasswdInfo.user_id==user_id)')
                #print "5555555555"
                if info :
                    #修改密码
                    #print "666"
                    if not phone_no :
                        #print "1111111111111111111111"
                        print "user id is %s" % user_id
                        user_password_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id == user_id).update({
                                                                                                                     TblUserPasswdInfo.password : password,
                                                                                                                     TblUserPasswdInfo.upd_dttm : now  
                                                                                                                     })
                    #修改手机号                                                                                      
                    if not password :
                        print "2222222222"
                        user_password_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id == user_id).update({
                                                                                                                     TblUserPasswdInfo.phone_no : phone_no,
                                                                                                                     TblUserPasswdInfo.upd_dttm : now  
                                                                                                                     })
                    db_session.commit()
                    return ret_func(const.RET_SUCCESS, '', {})
                else :
                    #返回验证码超时报文
                    return ret_func(const.RET_MSG_VER_CODE_EXPIRE, '', {})                                                                        
            else :
                return ret_func(check_ret, '', {})
        except SQLAlchemyError, e :
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
'''            
