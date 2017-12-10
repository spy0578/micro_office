# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblUserBasicInfo, TblUserLoginInfo, TblUserPasswdInfo, TblMsgVerCode
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
���ܣ��û�ע�Ტ��¼
1. У�������֤�����֤��δ���ڡ�����֤������֤��������ͬ(0)����������ע��������Ч(��ֹ���˶����ƹ���֤�룬ֱ�ӷ�ע��ı���)
2. �����û�����Ϣ�������û�������û�������Ϣ��
3. ����session_id
4. ��Ϣ��������¼��(��֤�Ƿ���ע����autenticate_api.py�����)
5. ����
���룺phone_no  password msg_ver_code code_type
�������ʶ��  user_id session_id
���ߣ���������֣��Ԩ
modify:2016-10-13  zzy
'''


class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session
        now = datetime.datetime.now()
        inJsonData = json.loads(request.get_data())
        phone_no = inJsonData['phone_no']
        password = inJsonData['password']
        msg_ver_code = inJsonData['msg_ver_code']
        code_type = inJsonData['code_type']
        ret = check_user_code(phone_no, code_type, msg_ver_code)
        if ret == const.RET_SUCCESS:
            #У����ֻ����Ƿ�ע���
            print "11111111"
            phone_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.phone_no == phone_no).first()
            if phone_info:
                return ret_func(const.RET_PHONE_NO_EXIST, '', {})
            else:
                '''
                password�ӹ�
                '''
                salt = random.randint(100000, 999999)
                passwd = password+str(salt)
                passwd = getsha256(passwd)
                user_passwd_info = TblUserPasswdInfo(
                                                        phone_no  = phone_no,
                                                        password  = passwd,
                                                        salt      = salt,
                                                        crt_dttm  = now,
                                                        upd_dttm  = now,
                                                        rec_stat  = '1',
                                                        user_stat = 0,
                                                        err_time  = 0
                                                        )
                db_session.add(user_passwd_info)
                db_session.flush()
                #db_session.commit()
                #��ȡ������user_id,����basic_info
                passwd_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.phone_no == phone_no).first()
                user_id = passwd_info.user_id
                user_basic_info = TblUserBasicInfo(
                                                    user_id = user_id,
                                                    gender = ' ',
                                                    name = ' ',
                                                    nickname = ' ',
                                                    avatar = 'default.jpg',
                                                    province = ' ',
                                                    city = ' ',
                                                    district = ' ',
                                                    crt_dttm = now,
                                                    upd_dttm =now,
                                                    record_stat = '1',
                                                    remark = ' '
                                                    )
                db_session.add(user_basic_info)
                db_session.flush()
                user_login_info = TblUserLoginInfo(
                                                    user_id = user_id,
                                                    login_opt = const.LOGIN_OPT_LOGIN,
                                                    login_time = now,
                                                    logout_time = now,
                                                    total_login_count = 1,
                                                    crt_dttm = now,
                                                    last_upd_dttm = now,
                                                    rec_stat = '1',
                                                    remark = ' '
                                                    )
                db_session.add(user_login_info)
                db_session.flush()
                '''
                ��ȡsession_id
                '''
                session_id = gen_session_id(phone_no, user_passwd_info.user_id)
                print session_id
                ret = set_session(user_passwd_info.user_id, session_id)
                #log.debug('value is :[%s]', rds[user_passwd_info.user_id])
                if ret == False :
                    db_session.rollback()
                    return ret_func(const.RET_MEMDB_ERROR, '', {})
                db_session.commit()
                data = dict()
                data['user_id'] = user_id
                data['session_id'] = session_id
                return ret_func(const.RET_SUCCESS, '', data)
        else:
            print "22222222222"
            print ret
            return ret_func(ret, '', {})




















'''

rds = g_rds_access.get_rds()
log=g_log.get_sys_log()

class user_register(MethodView):
    def post(self):
        db_session = DBSession()
        print "11111"
        print request.get_data()
        inJsonData = json.loads(request.get_data())
        phone_no = inJsonData['phone_no']
        password = inJsonData['password']
        
        log.debug('phone_no:[%s]' % phone_no)
        log.debug('password:[%s]' % password)
        now = datetime.datetime.now()
        try:
            db_session = DBSession()
            info = db_session.query(TblMsgVerCode).filter(TblMsgVerCode.phone_no == phone_no, now < TblMsgVerCode.exp_date_time, MsgVerCode.ver_code_stat == '1', TblMsgVerCode.msg_ver_type == '0').first()
            if info :
                user_passwd_info = TblUserPasswdInfo(phone_no    = phone_no,
                                                     password    = password,
                                                     crt_dttm    = now,
                                                     upd_dttm    = now,
                                                     rec_stat    = '1')

                db_session.add(user_passwd_info)
                db_session.flush()
                user_basic_info = TblUserBasicInfo(user_id       = user_passwd_info.user_id,
                                                   phone_no      = phone_no,
                                                   nickname      = '',
                                                   name          = '',
                                                   avatar        = '',
                                                   gender        = '',
                                                   crt_dttm    = now,
                                                   upd_dttm    = now,
                                                   rec_stat    = '1')
                db_session.add(user_basic_info)
                db_session.flush()
                #db_session.commit()
               
                 #get session_id
                session_id = gen_session_id(phone_no, user_passwd_info.user_id)
                #print "sessom_id is 1111 %s" % session_id
                #print "user_id is 222 %s" % user_passwd_info.user_id
                ret = rds.set(user_passwd_info.user_id, session_id)
                #print "session_id is %s" % rds['user_passwd_info.user_id']
                log.debug('value is :[%s]', rds[user_passwd_info.user_id])
                if ret == False :
                    #print "11111111111111111111111111111111111"
                    db_session.rollback()
                    return ret_func(const.RET_MEMDB_ERROR, '', {})
                user_login_info = TblUserLoginInfo(user_id            = user_passwd_info.user_id,
                                                   login_opt          = const.LOGIN_OPT_LOGOUT,
                                                   login_time         = now,
                                                   logout_time        = const.DEFALUT_TIMEDATE,
                                                   total_login_second = 0,
                                                   crt_dttm           = now,
                                                   upd_dttm           = now,
                                                   rec_stat           = '1')
                db_session.add(user_login_info)
                db_session.flush()
                db_session.commit()
                return ret_func(const.RET_SUCCESS, '', {'user_id':user_passwd_info.user_id, 'session_id':session_id})
            else :
                #������֤�볬ʱ����
                return ret_func(const.RET_MSG_VER_CODE_EXPIRE, '', {})
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
