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
from db.dborm.dborm import TblOprInfo,TblRoleInfo,TblChargerInfo,TblChrgGrpInfo
from db.dbinit import DBSession
from base.log import Log, g_log
from sqlalchemy import and_



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


        print 'request.args:', request.args
        parameters = request.args

        '''
         分隔符为&，截取字符串
        '''
        param_dict = parameters.to_dict()

        page                 = param_dict['page']
        charger_stat         = param_dict['charger_stat']
        charger_group_id     = param_dict['charger_group_id']


        print 'charger_stat:[%s], charger_group_id:[%s]' % (charger_stat, charger_group_id)


               
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



        charger_info_filters_list = []
        other_stat_list = [str(x + 20) for x in range(20) ]
        print other_stat_list
        if charger_stat != '':

            #xx 其它状态
            if charger_stat == 'xx':
                print '其它状态'
                charger_info_filters_list.append(TblChargerInfo.charger_stat.in_(other_stat_list))
            else:
                charger_info_filters_list.append(TblChargerInfo.charger_stat == charger_stat)

        if charger_group_id != '':
            print 'charger_group_id is not None'
            charger_info_filters_list.append(TblChargerInfo.charger_group_id == charger_group_id)

        charger_info_filters_list.append(TblChargerInfo.record_stat == const.RECORD_AVA)


        if role_info.role_type == const.SUPER_ADMIN_ROLE_TYPE :
            print '超级管理员'
        
        
            condition = and_(*charger_info_filters_list)

            total_count = db_session.query(TblChargerInfo).filter(condition).count()

            charger_info_list = db_session.query(TblChargerInfo).filter(condition).offset((int(page)-1) * N).limit(N).all()

       

        else :
            grp_id_tmp_list = db_session.query(TblChrgGrpInfo.charger_group_id).filter(TblChrgGrpInfo.charger_oper_id == opr_info.charger_oper_id,
                                                                                          TblChrgGrpInfo.record_stat   == const.RECORD_AVA).all()

            grp_id_list = []
            for grp_id_tmp in grp_id_tmp_list:
                grp_id_list.append(grp_id_tmp.charger_group_id)

            print grp_id_list

            charger_info_filters_list.append(TblChargerInfo.charger_group_id.in_(grp_id_list))

            condition = and_(*charger_info_filters_list)

            total_count = db_session.query(TblChargerInfo).filter(condition).count()

            charger_info_list = db_session.query(TblChargerInfo).filter(condition).offset((int(page)-1) * N).limit(N).all()





        for charger_info in charger_info_list :
            print charger_info.charger_id

            chrg_grp_info = db_session.query(TblChrgGrpInfo).filter(TblChrgGrpInfo.charger_group_id   == charger_info.charger_group_id,
                                                                    TblChrgGrpInfo.record_stat   == const.RECORD_AVA).first()



            if charger_info.charger_stat in other_stat_list :
                charger_info.charger_stat = 'xx'


            rst = {
                    'charger_id'           : charger_info.charger_id,
                    'charger_group_id'     : str(charger_info.charger_group_id),
                    'charger_group_address': chrg_grp_info.address,
                    'charger_prod_id'      : str(charger_info.charger_prod_id),
                    'park_pos'             : charger_info.park_pos,
                    'charger_stat'         : charger_info.charger_stat,
                    'charger_auth'         : charger_info.charger_auth,
                    'elec_value'           : str(charger_info.elec_value),
                    'remark': charger_info.remark
                    }

            rst_lst.append(rst)
 


        if total_count % N == 0 :
            flag = 0
        else:
            flag = 1

        print 'total_count:[%d]' % total_count

        page_count = total_count / N + flag
        print 'page_count:[%d]' % page_count


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

        


        return ret_func(const.RET_SUCCESS, 'success', data)
    
