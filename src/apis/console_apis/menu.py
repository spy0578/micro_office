# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
import sys
from db.dborm.dborm import TblOprInfo,TblRoleFuncInfo,TblFuncInfo
from db.dbinit import DBSession
from base.log import Log, g_log
reload(sys)
sys.setdefaultencoding('utf8')


class BaseGetClass(MethodView):
    @staticmethod
    def get():
        log=g_log.get_sys_log()
        db_session = g.db_session


        if request.headers.has_key('Authorization') is False :
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        auth = request.headers['Authorization']
        username = verify_auth_token(auth)
        if username is None :
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        
        opr_info = db_session.query(TblOprInfo).filter(TblOprInfo.opr_id == username,
                                                       TblOprInfo.record_stat   == const.RECORD_AVA).first()

        if opr_info is None :
            print 'opr_info is None'
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        print 'role_no:[%s]' % opr_info.role_no



        role_func_info_tuple = db_session.query(TblRoleFuncInfo).filter(TblRoleFuncInfo.role_no == opr_info.role_no,
                                                                        TblRoleFuncInfo.record_stat   == const.RECORD_AVA).all()



        data_list = []

        for role_func_info in role_func_info_tuple:
            print role_func_info.func_no
            func_info = db_session.query(TblFuncInfo).filter(TblFuncInfo.func_no == role_func_info.func_no,
                                                                   TblFuncInfo.record_stat   == const.RECORD_AVA).first()

            data = {
                    'func_name':func_info.func_name, 
                    'show_name':func_info.show_name
                    }

            data_list.append(data)




        return ret_func(const.RET_SUCCESS, 'success', data_list) 

