#-*- coding:utf-8 -*-
import redis
from base.design_pattern.singleton import Singleton
from etc.config import *
from dborm.dborm import TblRetCodeInfo
from dbinit import DBSession

#print redis.__file__

class GlobalRedisAccess(Singleton):
    rds = None

    session_rds = None
    plat_rds    = None

    def init_redis_access(self):
        print 'init redis'

        self.session_rds = redis.Redis(host=configs[config_type].REDIS_URI, port=int(configs[config_type].REDIS_PORT), 
                                       db=int(configs[config_type].SESSION_REDIS_NUM))

        self.plat_rds = redis.Redis(host=configs[config_type].REDIS_URI, port=int(configs[config_type].REDIS_PORT), 
                                       db=int(configs[config_type].PLAT_REDIS_NUM))
        self.init_plat_rds()
        
    def get_session_rds(self):
        return self.session_rds

    def get_plat_rds(self):
        return self.plat_rds


    def init_plat_rds(self):
        session = DBSession()
        print '初始化返回码'
        query = session.query(TblRetCodeInfo).all()

        for i in range(len(query)):
            print 'ret_code:[%s], ret_code_msg:[%s]' % (query[i].ret_code, query[i].ret_code_msg)
            self.plat_rds.hset('RET_CODE', query[i].ret_code, query[i].ret_code_msg)


        #如果不存在
        if self.plat_rds.exists('WEB_TXN_SN') == 0:
            self.plat_rds.hincrby('WEB_TXN_SN', 'CURR_SN', 0)


        session.close()


'''
 init redis
'''
g_rds_access = GlobalRedisAccess()
g_rds_access.init_redis_access()

