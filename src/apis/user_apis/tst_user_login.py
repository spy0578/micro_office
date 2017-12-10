# -*- coding: utf-8 -*-
import time
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import MsgVerCode, UserPasswdInfo, UserLoginInfo, UserBasicInfo, NoteTmplInfo
from db.redis_init import GlobalRedisAccess, g_rds_access
from base.log import g_txn_log
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
功能：用户正常登录
1. 验证密码是否正确
2. 置为登录，更新至登录表
3. 生成session_id 并更新至redis
4. 返回登录成功报文
输入：
phone_no password
输出:
各种报文
作者：郭祖龙、郑哲渊
'''

class user_login(MethodView):

    def post(self):

        log=g_txn_log.get_sys_log()
        rds = g_rds_access.get_rds()
        db_session = g.db_session

        inJsonData = json.loads(request.get_data())
        phone_no = inJsonData['phone_no']
        password = inJsonData['password']


        log.debug('phone_no:[%s]' % phone_no)
        log.debug('password:[%s]' % password)

        now = datetime.datetime.now()


        user_passwd_info_query = db_session.query(UserPasswdInfo)
        user_passwd_info = user_passwd_info_query.filter_by(phone_no=phone_no).first()
        if user_passwd_info :
            if password == user_passwd_info.password :
                '''
                 set user login
                '''
                user_login_info_query = db_session.query(UserLoginInfo)
                user_passwd_info = user_login_info_query.filter_by(user_id=user_passwd_info.user_id).first()
                if user_passwd_info :
                    user_login_info_query.filter(UserLoginInfo.user_id==user_passwd_info.user_id).update({
                                                                            UserLoginInfo.login_opt   : const.LOGIN_OPT_LOGIN,
                                                                            UserLoginInfo.login_time  : now,
                                                                            UserLoginInfo.upd_dttm    : now
                                                                            })
                    '''
                     get session_id
                    '''
                    session_id = gen_session_id(phone_no, user_passwd_info.user_id)

                    '''
                     save user_id - session_id in redis
                    '''
                    ret = rds.set(user_passwd_info.user_id, session_id)
                    if ret == False : 
                        return ret_func(const.RET_MEMDB_ERROR, '', {})
                    

                    #when get redis use next exception handler
                    #except KeyError,e:
                    #    print e
                    #    print 'KeyError'


                    log.debug("user:[%s] login successfully" % phone_no)

                    return ret_func(const.RET_SUCCESS, '', {'user_id':user_passwd_info.user_id, 'session_id':session_id})
                else :
                    #那就是在注册方法中直接新增记录，注册完就登录
                    return ret_func(const.RET_SYS_ERROR, '', {})
            else :
                return ret_func(const.RET_PASSWD_ERROR, '', {})
        else :
            #还未注册
            return ret_func(const.RET_PHONE_NO_NOT_EXIST, '', {})

