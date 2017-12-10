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
from db.dborm.dborm import TblOprInfo,TblRoleInfo
from db.dbinit import DBSession
from base.log import Log, g_log
reload(sys)
sys.setdefaultencoding('utf8')


def auth_verrify(func):
    def inner(obj):

        print 'inner'
        if request.headers.has_key('Authorization') is False :
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')
            
        auth = request.headers['Authorization']
        username = verify_auth_token(auth)
        if username is None :
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        return func()
    return inner



class BaseGetClass(MethodView):
    #@auth_verrify
    def get(self):
        log=g_log.get_sys_log()
        db_session = g.db_session


        if request.headers.has_key('Authorization') is False :
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        auth = request.headers['Authorization']
        username = verify_auth_token(auth)
        if username is None :
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')


        print 'request.args:', request.args
        parameters = request.args

        '''
         分隔符为&，截取字符串
        '''
        param_dict = parameters.to_dict()

        charger_group_id = param_dict['charger_group_id']

       
        opr_info = db_session.query(TblOprInfo).filter(TblOprInfo.opr_id == username,
                                                       TblOprInfo.record_stat   == const.RECORD_AVA).first()

        if opr_info is None :
            print 'opr_info is None'
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        print 'opr_info.role_no:[%s]' % opr_info.role_no


        chrg_grp_info = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.charger_group_id   == charger_group_id, 
                                                                TblChrgGrpInfo.record_stat   == const.RECORD_AVA).first()
        role_info = db_session.query(TblRoleInfo).filter(TblRoleInfo.role_no == opr_info.role_no).first()
        if role_info is None :
            print 'role_info is None'
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')


        if role_info.role_type != const.SUPER_ADMIN_ROLE_TYPE :
            if opr_info.charger_open_id != chrg_grp_info.charger_oper_id :
                print '管理员无权限查看其它公司信息'
                return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')


        print chrg_grp_info.charger_group_id
        rst = {
                'charger_group_id' : chrg_grp_info.charger_group_id,
                'province': chrg_grp_info.province,
                'city': chrg_grp_info.city,
                'district': chrg_grp_info.district,
                'location': chrg_grp_info.location,
                'address': chrg_grp_info.address,
                'open_tm': chrg_grp_info.open_tm,
                'close_tm': chrg_grp_info.close_tm,
                'longtitude': str(chrg_grp_info.longtitude),
                'latitude': str(chrg_grp_info.latitude),
                'elec_cost': str(chrg_grp_info.elec_cost),
                'addt_cost': str(chrg_grp_info.addt_cost),
                'charger_oper_id': str(chrg_grp_info.charger_oper_id),
                'remark': chrg_grp_info.remark
                }


        return ret_func(const.RET_SUCCESS, 'success', rst)


class BasePutClass(MethodView):
    @staticmethod
    def put():
        log=g_log.get_sys_log()
        db_session = g.db_session

        #db_session.query(

        print 'ppppppppppppppuuuuuuuuuuuuuuuuuuuuuuuutttttttttttt'
        print 'request.args:', request.args
        print request.get_data()


        return ret_func(const.RET_SUCCESS, 'success', {})
    
