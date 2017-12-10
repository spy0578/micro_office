# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import Flask, request, make_response,redirect,ctx,g, jsonify, _request_ctx_stack
from db.dborm.dborm import TblMsgVerCode, TblUserPasswdInfo, TblUserLoginInfo, TblMsgTmpl
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
import StringIO
import pycurl

'''
功能：创建短信验证码，并发送
1. 分为0:注册;1:修改手机号码;2:修改密码
2. 当0时，为注册。查看是否已经注册过;当1时，修改密码，要校验session_id的值。
3.验证短信验证码表中当前用户的该类型的验证码是否过期，若未过期，则返回之前验证码还在有效期内；
4. 若过期，则创建新的验证码，并更新至表中
5. 将验证码通过短信的方式返回给用户。
输入：
phone_no(type=0)
user_id(type=1/2)
session_id(type=1/2)
code_type:0:注册时候的验证码;1:修改密码或手机号的验证码
输出：
cpmid  验证码流水号
作者：郭祖龙、郑哲渊
edit 2016-10-12
'''



class BasePostClass(MethodView) :
    @staticmethod
    def post() :
        log=g_log.get_sys_log()
        db_session = g.db_session
        inJsonData = json.loads(request.get_data())
        now = datetime.datetime.now()
        type = inJsonData['type']
        if type == const.VER_CODE_TPYE_REGISTER:
            phone_no = inJsonData['phone_no']
        else:
            user_id = inJsonData['user_id']
            session_id = inJsonData['session_id']
            '''
            校验session_id
            '''
            check_ret = check_session_id(user_id, session_id)
            if check_ret == const.REDIS_SESSION_ID_CORRECT:
                user_info = db_session.query(TblUserPasswdInfo).filter(TblUserPasswdInfo.user_id == user_id).first()
                if user_info:
                    phone_no = user_info.phone_no
            else:
                return ret_func(const.RET_SESSION_EXPIRE, '', {})
        template_info = db_session.query(TblMsgTmpl).filter(TblMsgTmpl.tmpl_type == type).first()
        if template_info:
            text = template_info.tmpl_text
            msg_ver_code = random.randint(100000, 999999)
            delta = datetime.timedelta(minutes=const.CODE_EXPIRE_TIME)
            timeout_period = now + delta
            '''
            #生成验证码流水号
            now_date = datetime.datetime.now().strftime('%y%m%d')
            code_info = db_session.query(TblMsgVerCode).first()
            if code_info:
                max_info = db_session.execute('SELECT MAX(ver_code_id) FROM tbl_msg_ver_code')
                max_date = max_info[0:6]
                max_id = max_info[6:11]
                #表明已到另一天,id重置
                if now_date > max_date:
                    max_date = now_date
                    max_id = '00000'
                else:
                    max_id = int(max_id)+1
            else:
                print "table is none"
                max_date = now_date
                max_id = '00000'

            cpmid = max_date + str(max_id)
            '''
            '''
            新增验证码
            '''
            code_info = db_session.query(TblMsgVerCode).filter(TblMsgVerCode.phone_no == phone_no).first()
            if code_info:
                db_session.query(TblMsgVerCode).filter(TblMsgVerCode.phone_no == phone_no).update({
                                                                                                    TblMsgVerCode.apply_dttm    : now,
                                                                                                    TblMsgVerCode.exp_dttm      : timeout_period,
                                                                                                    TblMsgVerCode.ver_code_type : type,
                                                                                                    TblMsgVerCode.ver_code_stat : const.VER_CODE_UNCHECKED,
                                                                                                    TblMsgVerCode.msg_ver_code  : str(msg_ver_code),
                                                                                                    TblMsgVerCode.last_upd_dttm : now,
                                                                                                    TblMsgVerCode.remark        : 1,
                                                                                                    TblMsgVerCode.record_stat   : 1
                                                                                                    })
            else:
                ver_code_info = TblMsgVerCode(
                                            phone_no      = phone_no,
                                            apply_dttm    = now,
                                            exp_dttm      = timeout_period,
                                            ver_code_type = type,
                                            ver_code_stat = const.VER_CODE_UNCHECKED,
                                            msg_ver_code  = str(msg_ver_code),
                                            last_upd_dttm =now,
                                            remark        = 1,
                                            record_stat   = 1
                                             )
                db_session.add(ver_code_info)
            '''
            向短信平台发送
            '''
            storage = StringIO.StringIO()
            URL = const.MESSAGE_URL
            c = pycurl.Curl()
            head = ['Content-Type:text/xml;charset=utf-8']
            values = dict()
            values['cpid'] = const.CPID
            values['userpass'] = const.USERPASS
            values['port'] = const.PORT
            values['cpmid'] = const.CPMID
            values['flag'] = 0
            values['mobile'] = phone_no
            values['message'] = text + str(msg_ver_code) + const.ALERT + const.LOGO
            print "我是帅哥"
            values['respDataType'] = 'JSON'
            data = trans_dict_to_xml(values)
            print data
            c.setopt(c.URL, URL)
            c.setopt(c.WRITEFUNCTION, storage.write)
            c.setopt(pycurl.POSTFIELDS, data)
            c.setopt(pycurl.CUSTOMREQUEST, "POST")
            c.setopt(pycurl.HTTPHEADER, head)
            c.perform()
            c.close()
            content = json.loads(storage.getvalue())
            if content['respCode'] == "0":
                db_session.flush()
                db_session.commit()
                #data1 = dict(cpmid=cpmid)
                return ret_func(const.RET_SUCCESS, '', {})
            else:
                print content['respCode']
                return ret_func(const.RET_MESSAGE_ERROR, '',{})
        else:
            return ret_func(const.RET_SYS_ERROR, '',{})




