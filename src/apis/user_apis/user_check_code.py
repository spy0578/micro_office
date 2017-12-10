# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblMsgVerCode, TblUserPasswdInfo, TblUserLoginInfo, TblUserBasicInfo, TblNoteTmplInfo
from db.dbinit import DBSession
from base.log import Log, g_log
import json
import functools
from apis.api_comm import *
import datetime
from base.comm_const import *
import random
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DBAPIError

'''
���ܣ�У�������֤�����ȷ��
1. У���Ƿ������֤���¼
2. У���Ƿ�ʱ
3. У���Ƿ���ȷ
4. ������֤���
���룺phone_no code_type msg_ver_code
���
���ߣ�
��������֣��Ԩ
'''
class user_check_code(MethodView) :
    def post(self) :
        log=g_log.get_sys_log()
        
        inJsonData = json.loads(request.get_data())
        phone_no = inJsonData['phone_no']
        code_type = inJsonData['type']
        msg_ver_code = inJsonData['msg_ver_code']
        if phone_no is None :
            return ret_func(const.RET_ARG_ERROR, '', {})
        if msg_ver_code is None :
            return ret_func(const.RET_ARG_ERROR, '', {})
        if code_type is None :
            return ret_func(const.RET_ARG_ERROR, '', {})        
        
        print "phone_no:[%s]" % phone_no 
        print "msg_ver_code:[%s]" % msg_ver_code
        now = datetime.datetime.now()
        try :
            db_session = DBSession()
            query = db_session.query(TblMsgVerCode)
            MsgVerCode_info = query.filter(TblMsgVerCode.phone_no == phone_no, TblMsgVerCode.msg_ver_type == code_type, TblMsgVerCode.ver_code_stat == const.VER_CODE_UNCHECKED).first()
            if MsgVerCode_info :
                if now < MsgVerCode_info.exp_date_time :
                    if ( msg_ver_code == MsgVerCode_info.msg_ver_code ) :
                        query.filter(MsgVerCode_info.phone_no == phone_no).update({TblMsgVerCode.ver_code_stat   : const.VER_CODE_CHECKED,
                                                                              TblMsgVerCode.upd_dttm        : now})
                        db_session.commit()
                        return ret_func(const.RET_SUCCESS, 'msg_ver_code is correct', {})
                    else :
                        #��֤�벻��ȷ
                        return ret_func(const.RET_MSG_VER_CODE_ERROR, '', {})
                else :
                    #��֤�볬ʱ
                    return ret_func(const.RET_MSG_VER_CODE_EXPIRE, '', {})
            else :
                #��������֤��
                return ret_func(const.RET_MSG_VER_CODE_UNAPPLY, '', {})
        except SQLAlchemyError, e :
            print type(e)
            log.debug(e)
            db_session.rollback()
            return ret_func(const.RET_DB_ERROR, '', {})
        finally :
            db_session.close()
