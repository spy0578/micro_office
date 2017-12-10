from flask import Flask, request, make_response,redirect,ctx,g, jsonify
from base.comm_const import *
import hashlib
import datetime
from db.redis_init import GlobalRedisAccess, g_rds_access
from redis.exceptions import RedisError


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
    rds = g_rds_access.get_rds()
    try:
        redis_session_id = rds['user_id']
        if session_id == redis_session_id :
            return REDIS_session_id_correct
        else :
            reutrn const.RET_LOGIN_OTHER_TERM
    except KeyError, e:
        log.debug(e)
        print 'key not exist in redis'
        #若redist中没有相应的号码，则让用户重新登录
        return const.RET_MEMDB_KEY_ERROR
    except RedisError, e:
        print type(e)
        log.debug(e)
        return const.RET_MEMDB_ERROR
        


        
