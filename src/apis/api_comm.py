# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g, jsonify
from base.comm_const import *
import hashlib
import datetime
from db.redis_init import GlobalRedisAccess, g_rds_access
from db.dbinit import DBSession
from db.dborm.dborm import TblOlLogInfo
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
import importlib



#from Crypto.PublicKey import RSA
#from Crypto.Signature import PKCS1_v1_5
#from Crypto.Hash import SHA256
#import pingpp
import math
import hashlib

def base_request_route_handler(route_root, route_name, class_func_name):
    print route_root
    print route_name

    module_name = 'apis.'+route_root+'.'+route_name

    '''
     <todo>判断模块是否存在
     如果不存在直接返回系统错误
    '''
    #动态加载
    module = importlib.import_module(module_name)    

    '''
     <todo> 根据模块名module可以增加一些处理
    '''
    
    g.db_session = DBSession()

    log = g_log.get_sys_log()

    #使用静态调用
    ret_flag, ol_log_info, module_ret = eval(class_func_name)()

    if ret_flag is True:
        g.db_session.commit()
    else :
        g.db_session.rollback()

    #如果不为空，则登记流水表
    if ol_log_info:
        log.info("ol_log_info:%s", ol_log_info)


        user_id        = ol_log_info['user_id'] \
                        if ol_log_info.has_key('user_id') else '0'
        service        = ol_log_info['service'] \
                        if ol_log_info.has_key('service') else ' '

        json_dict = json.loads(module_ret)
        print json_dict['header']['code']
        ret_code       = json_dict['header']['code']
        remark         = json_dict['header']['description']
        last_upd_dttm  = datetime.datetime.now()
        record_stat    = '1'

        user_id = int(user_id)
        print ol_log_info

        tbl_ol_log_info = TblOlLogInfo(user_id = user_id,
                               service = service,
                               ret_code  = ret_code,
                               remark     = remark,
                               last_upd_dttm   = last_upd_dttm,
                               record_stat   = const.RECORD_AVA)

        g.db_session.add(tbl_ol_log_info)
        g.db_session.flush() 
        g.db_session.commit()
        

    if g.db_session != None:
        g.db_session.close()

    return module_ret







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
    #return jsonify({'header':{'code':code, 'message':'', 'description':description}, 'data':data})
 
    return json.dumps({'header':{'code':code, 'message':get_code_msg(code), 'description':description}, 'data':data})

def get_code_msg(code):
    rds = g_rds_access.get_plat_rds()
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


    g_log.get_sys_log().info(response)
    g_log.get_sys_log().info(type(response))
    g_log.get_sys_log().info(response.headers)
    
    try :
        g_log.get_sys_log().info(response.data)
    except Exception, e:
        g_log.get_sys_log().info(e)
        return "交易唯一戳[%s]:类型[RSP]:时间[%s]:交易时长[%s]毫秒:响应头[%s]" %  \
                    (now_hms+get_curr_sn(), now_hms, diff, response.headers)        
    else:
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
