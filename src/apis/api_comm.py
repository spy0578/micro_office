# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g, jsonify
from base.comm_const import *
import hashlib
import datetime
from db.redis_init import GlobalRedisAccess, g_rds_access
from db.dbinit import DBSession
from base.log import g_log
import json
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DBAPIError
from sqlalchemy import or_
from redis.exceptions import RedisError
import time
import uuid
import base64
import os
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired,BadSignature



#from Crypto.PublicKey import RSA
#from Crypto.Signature import PKCS1_v1_5
#from Crypto.Hash import SHA256
#import pingpp
import math
import hashlib



'''
为app提供的服务api函数返回函数

log_data: 登记流水表所需数据，AppActLog对象
'''
def ret_func_for_app(code, description, ret_data, log_data):
    db_session = g.db_session

    if code is not const.RET_SUCCESS:
        db_session.rollback()


    print log_data
    print 'description:[%s]' % description


    if log_data :
    
        '''
         登记AppActLog 用户行为流水表
        '''

        t_user_id = 0
        t_service = ' '
        t_charger_id = ' '

        if log_data.has_key('user_id') :
            t_user_id = int(log_data['user_id'])
        if log_data.has_key('service') :
            if log_data['service'] != '' :
                t_service = log_data['service']
        if log_data.has_key('charger_id') :
            if log_data['charger_id'] != '' :
                t_charger_id = log_data['charger_id']

        t_code = ' '
        t_remark = ' '

        if code != '':
            t_code = code

        if description != '':
            t_remark = description

            
        now = datetime.datetime.now()
        app_act_log = TblAppActLog(user_id = t_user_id,
                                   service = t_service,
                                   charger_id = t_charger_id,
                                   ret_code  = t_code,
                                   remark     = t_remark,
                                   last_upd_dttm   = now,
                                   record_stat   = const.RECORD_AVA)

        db_session.add(app_act_log)
        db_session.flush() 
        db_session.commit()


    return ret_func(code, description, ret_data)


def ifGetHtml():
    #根据request.url，判断客户端请求是html
    request_list = request.url.split('/')
    if request_list[len(request_list) - 2] == const.HTML_APIS :
        return True
    else :
        return False



def get_ret_code(ret_json_data):
    rsp_dict = json.loads(ret_json_data)
    print rsp_dict["header"]
    return rsp_dict["header"]["code"]


def ret_func(code, description, data):
    #arguments: data must be json
    #<todo> get message according to code
    #return jsonify({'header':{'code':code, 'message':'', 'description':description}, 'data':data})
    return json.dumps({'header':{'code':code, 'message':get_code_msg(code), 'description':description}, 'data':data})

def get_code_msg(code):
    rds = g.rds
    try :
        msg = rds.hgetall('RET_CODE')[code]
        return msg
    #捕获异常避免并成功处理
    except KeyError, e:
        print 'get_code_msg key not exist in redis'
        return ''

def get_txn_begin_log():
    #now = datetime.datetime.now()
    #mircro = getattr(now, 'microsecond')
    #now_hms = now.strftime('%H%M%S')

    g.request_start_time = time.time()
    now = datetime.datetime.fromtimestamp(g.request_start_time)
    mircro = getattr(now, 'microsecond')
    now_hms = now.strftime('%H%M%S')

    #g.txn_begin = now_hms + '.' + mircro

    return "交易唯一戳[%s]:类型[REQ]:时间[%s]:交易时长[0]毫秒:请求url[%s]:请求头[%s]:请求数据[%s]" %  \
                    (now_hms+get_next_sn('WEB_TXN_SN'), now_hms, request.url, request.headers, request.data)

def get_txn_end_log(response):
    end_time = time.time()
    diff = "%.5fs" % (end_time - g.request_start_time)
    print diff


    now = datetime.datetime.fromtimestamp(end_time)
    mircro = getattr(now, 'microsecond')
    now_hms = now.strftime('%H%M%S')


    return "交易唯一戳[%s]:类型[RSP]:时间[%s]:交易时长[%s]毫秒:响应头[%s]:响应数据[%s]" %  \
                    (now_hms+get_curr_sn(), now_hms, diff, response.headers, response.data)


def get_curr_microsecond():
    now = datetime.datetime.now()
    mircro = getattr(now, 'microsecond')
    print now
    print micro

    return micro


def get_next_sn(sn):
    rds = g_rds_access.get_plat_rds()

    rds.hincrby(sn, 'CURR_SN', 1)
    sn = rds.hgetall(sn)['CURR_SN']

    g.curr_sn = sn.zfill(8)

    #return sn.zfill(8)
    return g.curr_sn

def get_curr_sn():

    return g.curr_sn


'''
  如果使用以下一组函数，则
  在接口中可以不用传user_id

  expiration=600 10min
'''
def generate_auth_token(username, expiration = 3600 * 24 * 7):
    s = Serializer('SECRET_KEY', expires_in = expiration)
    return s.dumps({ 'username': username })


def verify_auth_token(token):
    s = Serializer('SECRET_KEY')
    try:
        data = s.loads(token)
    except SignatureExpired:
        print 'SignatureExpired!!!'
        return None # valid token, but expired
    except BadSignature:
        print 'BadSignature!!!'
        return None # invalid token

    return data['username']




def gen_session_id(phone_no, user_id):
    now = datetime.datetime.now()
    session_id = hashlib.md5('%s#%s#%s#%s' % (phone_no, user_id, const.SESSION_KEY, now)).hexdigest()
    print "session_id:[%s]" % session_id
    return session_id

def set_session(user_id, session_id):
    rds = g_rds_access.get_session_rds()
    now = datetime.datetime.now()

    rds.hset(user_id, 'session_id', session_id)
    rds.hset(user_id, 'login_dttm', now)
    rds.hset(user_id, 'last_session_sec', time.time()) #last_session_sec 距离1970年1月1日0点秒数


'''
功能：
1. 校验app请求中的session_id
输入：
phone_no
session_id
输出：
1. 匹配成功，返回REDIS_session_id_correct
2. 匹配不成功，返回const.RET_LOGIN_OTHER_TERM  表明在另外地点登录
3. redis中没有相应的记录，返回RET_MEMDB_KEY_ERROR  重新登录
4. redis出错，返回RET_MEMDB_ERROR
作者：郑哲渊
'''
def check_session_id(user_id, session_id):
    rds = g_rds_access.get_session_rds()
    log=g_log.get_sys_log()
    now = datetime.datetime.now()
    try:
        #redis_session_id = rds[user_id]
        redis_session_id = rds.hgetall(user_id)['session_id']
        print 'check_session_id, redis_session_id:[%s]' % redis_session_id
        if session_id == redis_session_id :
            print "session id correct : %s" % session_id
            last_session_sec = rds.hgetall(user_id)['last_session_sec']
            diff = time.time() - float(last_session_sec)
            print 'last_session_sec:[%s], diff:[%f]' % (last_session_sec, diff)
            
            rds.hset(user_id, 'last_session_sec', time.time()) #last_session_sec 距离1970年1月1日0点秒数

            if diff >= const.SESSION_EXPIRE_SEC:
                return const.RET_SESSION_EXPIRE
            return const.REDIS_SESSION_ID_CORRECT
        else :
            return const.RET_LOGIN_OTHER_TERM 

    #捕获异常避免并成功处理
    except KeyError, e:
        log.debug(e)
        print 'check_session_id key not exist in redis'
        #若redist中没有相应的号码，则让用户重新登录
        return const.RET_MEMDB_KEY_ERROR
    except RedisError, e:
        print type(e) 
        log.debug(e)
        return const.RET_MEMDB_ERROR
