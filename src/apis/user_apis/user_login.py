# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblChargerCommand, TblChargerCommandH, TblChargerInfo, TblCharging, TblChargingH,TblUserBasicInfo, TblUserLoginInfo, TblUserPasswdInfo, TblHomeHtmlInfo
from db.dbinit import DBSession
from db.redis_init import GlobalRedisAccess, g_rds_access
from base.log import g_log
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
from passlib.hash import bcrypt

# Calculating a hash
hash = bcrypt.encrypt(usersPassword, rounds=12)

# Validating a hash
if bcrypt.verify(usersPassword, hash):
        # Login successful
'''

class BasePostClass(MethodView):
    @staticmethod
    def post():
        log=g_log.get_sys_log()
        db_session = g.db_session

        print 'get here'
        print g.db_session


        inJsonData = json.loads(request.get_data())
        phone_no = inJsonData['phone_no']
        password = inJsonData['password']


        '''
        <todo> 校验参数
        '''


        log.debug('phone_no:[%s]' % phone_no)
        print 'phone_no:[%s]' % phone_no
        log.debug('password:[%s]' % password)
        print 'password:[%s]' % password


        now = datetime.datetime.now()
 
        log_data = {
            'service' : 'user_login',
           }


        user_passwd_info_query = db_session.query(TblUserPasswdInfo)
        user_passwd_info = user_passwd_info_query.filter_by(phone_no=phone_no).first()
        if user_passwd_info :
            if user_passwd_info.user_stat == const.USER_LOCK_STAT:
                return ret_func(const.RET_USER_LOCK_ERROR, '', {})
            else:
                passwd = password + str(user_passwd_info.salt)
                passwd = getsha256(passwd)
                if passwd == user_passwd_info.password :
                    '''
                     set user login
                    '''
                    user_login_info = db_session.query(TblUserLoginInfo).filter(TblUserLoginInfo.user_id == user_passwd_info.user_id).first()
                    #user_passwd_info = user_login_info_query.filter_by(user_id=user_passwd_info.user_id).first()
                    if user_login_info :
                        db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.phone_no == phone_no).update({
                                                                                                                    TblUserPasswdInfo.err_time :0,
                                                                                                                    TblUserPasswdInfo.upd_dttm :now
                                                                                                                    })
                        db_session.query(TblUserLoginInfo).filter(TblUserLoginInfo.user_id==user_passwd_info.user_id).update({
                                                                                TblUserLoginInfo.login_opt   : const.LOGIN_OPT_LOGIN,
                                                                                TblUserLoginInfo.login_time  : now,
                                                                                TblUserLoginInfo.total_login_count : TblUserLoginInfo.total_login_count+1,
                                                                                TblUserLoginInfo.last_upd_dttm    : now
                                                                                })
                        #session_id = gen_session_id(phone_no, user_passwd_info.user_id)

                        '''
                         save user_id - session_id in redis
                        '''
                        #set_session(user_passwd_info.user_id, session_id)
                        

                        #when get redis use next exception handler
                        #except KeyError,e:
                        #    print e
                        #    print 'KeyError'


                        #return ret_func_for_app(const.RET_SUCCESS, '', {'user_id':user_passwd_info.user_id, 'session_id':session_id}, log_data)
                    else :
                        #首次登录
                        login_info = TblUserLoginInfo(
                                                      user_id = user_passwd_info.user_id,
                                                      login_opt = const.LOGIN_OPT_LOGIN,
                                                      crt_time = now,
                                                      login_time = now,
                                                      logout_time = now,
                                                      upd_dttm = now,
                                                      total_login_second = 0,
                                                      ret_stat = '1'
                                                       )
                        db_session.add(login_info)
                    session_id = gen_session_id(phone_no, user_passwd_info.user_id)
                    '''
                    save user_id - session_id in redis
                    '''
                    set_session(user_passwd_info.user_id, session_id)
                    data = dict()
                    user_info = db_session.query(TblUserBasicInfo).filter(TblUserBasicInfo.user_id == user_passwd_info.user_id).first()
                    if user_info:
                        data['gender'] = user_info.gender
                        data['name'] = user_info.name
                        data['nickname'] = user_info.nickname
                        data['province'] = user_info.province
                        data['city'] = user_info.city
                        data['district'] = user_info.district
                        data['car_number'] = user_info.car_number
                        data['car_information'] = user_info.car_information
                        data['user_id'] = user_passwd_info.user_id
                        data['session_id'] = session_id
                        home_html_info = db_session.query(TblHomeHtmlInfo).all()
                        data_list = []
                        for instance in home_html_info:
                            ele = {
                                    'image'   : const.IMAGE_PATH + str(instance.image),
                                    'html'    : const.HTML_PATH + str(instance.html)
                                   }
                            data_list.append(ele)
                        data['home_html'] = data_list
                        log_data = {
                                'user_id' : user_passwd_info.user_id,
                                'service' : 'user_login',
                                }
                        db_session.flush()
                        db_session.commit()
                        log.debug("user:[%s] login successfully" % phone_no)
                        print "user:[%s] login successfully" % phone_no
                        return ret_func_for_app(const.RET_SUCCESS, '', data, log_data)

                else :
                    if user_passwd_info.err_time >= const.PASSWD_MAX_TIME:
                        db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.phone_no == phone_no).update({
                                                                                                                    TblUserPasswdInfo.user_stat  : const.USER_LOCK_STAT,
                                                                                                                    TblUserPasswdInfo.upd_dttm : now
                                                                                                                    })
                        db_session.flush()
                        db_session.commit()
                        #在改为锁定状态的同时，改掉session_id，使跳转到登录页面
                        session_id = gen_session_id(phone_no, user_passwd_info.user_id)
                        '''
                        save user_id - session_id in redis
                        '''
                        set_session(user_passwd_info.user_id, session_id)

                        return ret_func(const.RET_USER_LOCK_ERROR, '', {})
                    else:
                        count = const.PASSWD_MAX_TIME - user_passwd_info.err_time
                        db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.phone_no == phone_no).update({
                                                                                                                    TblUserPasswdInfo.err_time : TblUserPasswdInfo.err_time+1,
                                                                                                                    TblUserPasswdInfo.upd_dttm : now
                                                                                                                    })
                        data = dict(time=count)
                        db_session.flush()
                        db_session.commit()
                        return ret_func(const.RET_PASSWD_ERROR, '', data)
        else :
            #还未注册
            return ret_func(const.RET_PHONE_NO_NOT_EXIST, '', {})

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
'''
class user_login(MethodView):

    def post(self):
        log=g_log.get_sys_log()
        rds = g_rds_access.get_rds()
        db_session = DBSession()
        inJsonData = json.loads(request.get_data())
        phone_no = inJsonData['phone_no']
        password = inJsonData['password']


        log.debug('phone_no:[%s]' % phone_no)
        log.debug('password:[%s]' % password)

        now = datetime.datetime.now()

        try :
            user_passwd_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.phone_no == phone_no).first()
            if user_passwd_info :
                if password == user_passwd_info.password :
                     #set user login
                    user_passwd_info = db_session.query(TblUserLoginInfo).filter(TblUserLoginInfo.user_id == user_passwd_info.user_id).first()
                    if user_passwd_info :
                        user_login_info_query.filter(TblUserLoginInfo.user_id==user_passwd_info.user_id).update({
                                                                                TblUserLoginInfo.login_opt   : const.LOGIN_OPT_LOGIN,
                                                                                TblUserLoginInfo.login_time  : now,
                                                                                TblUserLoginInfo.upd_dttm    : now
                                                                                })
                         #get session_id
                        session_id = gen_session_id(phone_no, user_passwd_info.user_id)

                         #save user_id - session_id in redis
                        # 将内层的try..except改为外层，多一个对抛出异常的处理就行
         #所有的else 都加上rollback（）          
                       
                        ret = rds.set(user_passwd_info.user_id, session_id)
                        if ret == False : 
                            db_session.rollback()
                            return ret_func(const.RET_MEMDB_ERROR, '', {})
                        

                        #when get redis use next exception handler
                        #except KeyError,e:
                        #    print e
                        #    print 'KeyError'

                        db_session.commit()

                        log.debug("user:[%s] login successfully" % phone_no)

                        return ret_func(const.RET_SUCCESS, '', {'user_id':user_passwd_info.user_id, 'session_id':session_id})
                    else :
                        #那就是在注册方法中直接新增记录，注册完就登录
                        db_session.rollback()
                        return ret_func(const.RET_SYS_ERROR, '', {})
                else :
                    db_session.rollback()
                    return ret_func(const.RET_PASSWD_ERROR, '', {})
            else :
                db_session.rollback()
                #还未注册
                return ret_func(const.RET_PHONE_NO_NOT_EXIST, '', {})

        except SQLAlchemyError, e :
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_DB_ERROR, '', {})
        except RedisError,e:
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_MEMDB_ERROR, '', {})

        finally :
            db_session.close()

'''
