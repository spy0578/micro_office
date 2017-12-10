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

tasks = [
    {
        'uri': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 2',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 3',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 4',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 5',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 6',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 7',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 8',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },

]


tasks1 = [
    {
        'uri': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 2',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 3',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 4',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
    {
        'uri': 2,
        'title': u'Learn 5',
        'description': u'Need to find a good Python tutorial on the web',
        'create_time': '20160912143421'
    },
]

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


        print 'request.args:', request.args
        parameters = request.args

        '''
         分隔符为&，截取字符串
        '''
        param_dict = parameters.to_dict()

        page = param_dict['page']
        search = param_dict['search']

       
        opr_info = db_session.query(TblOprInfo).filter(TblOprInfo.opr_id == username,
                                                       TblOprInfo.record_stat   == const.RECORD_AVA).first()

        if opr_info is None :
            print 'opr_info is None'
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        print 'opr_info.role_no:[%s]' % opr_info.role_no


        N = 5
        i_offset = (int(page) - 1) * N
        print 'i_offset:[%d]' % i_offset

        rst_lst = []


        role_info = db_session.query(TblRoleInfo).filter(TblRoleInfo.role_no == opr_info.role_no).first()
        if role_info is None :
            print 'role_info is None'
            return ret_func(const.RET_SESSION_EXPIRE, 'not login', '')

        
        if role_info.role_type == const.SUPER_ADMIN_ROLE_TYPE :
            print '超级管理员'

            total_count = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.record_stat   == const.RECORD_AVA).count()

            chrg_grp_info_list = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.record_stat == const.RECORD_AVA).offset((int(page)-1) * N).limit(N).all()

       

        else :
            #opr_info.charger_oper_id
            total_count = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.charger_oper_id == opr_info.charger_oper_id,
                                                                           TblChrgGrpInfo.record_stat   == const.RECORD_AVA).count()


            chrg_grp_info_list = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.charger_oper_id == opr_info.charger_oper_id,
                                                     TblChrgGrpInfo.record_stat     == const.RECORD_AVA).offset((int(page)-1) * N).limit(N).all()
            #for chrg_grp_info in chrg_grp_info_list :


        for chrg_grp_info in chrg_grp_info_list :
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

            rst_lst.append(rst)
 


        if total_count % N == 0 :
            flag = 0
        else:
            flag = 1

        page_count = total_count / N + flag


        previous = next = True
        if page == '1' :
            previous = False
        elif int(page) == page_count :
            next = False


        print 'next:[%s], previous:[%s]' % (next, previous)


        data = { 'total_count': total_count ,
                 'page_count' : page_count ,
                 'next'       : next, 
                 'previous'   : previous,
                 'results'    : rst_lst}
        print data

        
        '''
        data = {}
        if page == '1':
            data = { 'total_count': 8 ,
                     'page_count' : 2 ,
                     'next'       : True, 
                     'previous'   : False,
                     'results'    : tasks[0:5]}
        elif page == '2':
            data = { 'total_count': 8 ,
                     'page_count' : 2 ,
                     'next'       : False, 
                     'previous'   : True,
                     'results'    : tasks[5:8]}
            print data
        '''


        return ret_func(const.RET_SUCCESS, 'success', data)
    
