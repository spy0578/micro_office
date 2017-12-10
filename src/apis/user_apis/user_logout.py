# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblChargerCommand, TblChargerCommandH, TblChargerInfo, TblCharging, TblChargingH,TblUserBasicInfo, TblUserLoginInfo, TblUserPasswdInfo
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
功能：用户正常退出
1. 校验session_id
2. 校验用户登录表，是否有记录，如没有，表明不存在该用户
3. 校验是否登录
4. 若登录，置为退出登录
5. 返回操作成功报文
输入：user_id session_id
输出
作者：郑哲渊
'''
class user_logout(MethodView) :
    def post(self) :
        log=g_log.get_sys_log()
        #rds = g_rds_access.get_rds()
        
        inJsonData = json.loads(request.get_data())
        user_id = inJsonData['user_id']
        session_id = inJsonData['session_id']
        log.debug('user_id:[%s]' % user_id)
        log.debug('session_id:[%s]' % session_id)
        print "userid is %s" % user_id
        now = datetime.datetime.now()
        try :
            db_session = DBSession()
            check_ret = check_session_id(user_id, session_id)
            if check_ret == REDIS_session_id_correct :
                login_info = db_session.query(TblUserLoginInfo).query.filter(TblUserLoginInfo.user_id == user_id).first()
                if login_info :
                    #表明是登录状态
                    #login_opt = db_session.query(UserLoginInfo.login_opt).filter(UserLoginInfo.user_id == user_id).first()
                    if login_info.login_opt == "const.LOGIN_OPT_LOGIN" :
                    #print "login_opt is %s" % login_info.login_opt
                    #if login_info.login_opt == "1" :
                        #print "111111111"
                        db_session.query(TblUserLoginInfo).filter(TblUserLoginInfo.user_id == user_id).update({  
                                                                                                               TblUserLoginInfo.login_opt : const.LOGIN_OPT_LOGOUT ,
                                                                                                               TblUserLoginInfo.logout_time : now
                                                                                                               })
                        db_session.commit()
                        return ret_func(const.RET_SUCCESS, '', {})
                    else :
                        return ret_func(const.RET_USER_ID_NOT_LOGIN, 'has not login', {})
                else :
                    #表明该用户不存在，因为注册完立即添加到登录表
                    return ret_func(const.RET_USER_ID_NOT_EXIST, 'has not login', {})
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
