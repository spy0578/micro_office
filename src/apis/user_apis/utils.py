from flask import Flask, request, make_response,redirect,ctx,g, jsonify
from base.comm_const import *
import hashlib
import datetime
from db.redis_init import GlobalRedisAccess, g_rds_access
from redis.exceptions import RedisError


'''
���ܣ�
1. У��app�����е�session_id
���룺
phone_no
session_id
�����
1. ƥ��ɹ�������REDIS_session_id_correct
2. ƥ�䲻�ɹ�������const.RET_LOGIN_OTHER_TERM  ����������ص��¼
3. redis��û����Ӧ�ļ�¼������RET_MEMDB_KEY_ERROR  ���µ�¼
4. redis��������RET_MEMDB_ERROR
���ߣ�֣��Ԩ
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
        #��redist��û����Ӧ�ĺ��룬�����û����µ�¼
        return const.RET_MEMDB_KEY_ERROR
    except RedisError, e:
        print type(e)
        log.debug(e)
        return const.RET_MEMDB_ERROR
        


        
