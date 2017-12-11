# -*- coding: utf-8 -*-
import time
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
import importlib
from base.log import g_log

'''
功能：

输入：
输出:
'''

class RequestRouteHandler(MethodView):
    def base(self, route_root, route_name):
	print route_root
        print route_name

        module_name = 'apis.'+route_root+'.'+route_name

        '''
         <todo>判断模块是否存在
         如果不存在直接返回系统错误
        '''
        #动态加载
        module = importlib.import_module(module_name)
        print module.BasePostClass
        print type(module.BasePostClass)        

        '''
         <todo> 根据模块名module可以增加一些处理
        '''
        
	#初始化交易流程中的全局变量
        g.db_session = DBSession()
	g.log = g_log.get_sys_log()
	g.rds = g_rds_access.get_plat_rds()


        #使用静态调用
        ret_flag, ol_log_info, module_ret = module.BaseGetClass().get()

        if ret_flag is True:
            g.db_session.commit()
        else :
            g.db_session.rollback()

        #如果不为空，则登记流水表
        if ol_log_info:
            g.log.info("ol_log_info:%s", ol_log_info)


            user_id        = ol_log_info['user_id'] \
                            if ol_log_info.has_key('user_id') else '0'
            service        = ol_log_info['service'] \
                            if ol_log_info.has_key('service') else ' '
            ret_code       = module_ret['header']['code']
            remark         = module_ret['description']
            last_upd_dttm  = datetime.datetime.now()
            record_stat    = '1'

            user_id = int(user_id)
            print ol_log_info
            

        if g.db_session != None:
            g.db_session.close()
 
	return module_ret


    def get(self, route_root, route_name):
        return self.base(route_root, route_name)


    def post(self, route_root, route_name):
        return self.base(route_root, route_name)

    def put(self, route_root, route_name):
        return self.base(route_root, route_name)
