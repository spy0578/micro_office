# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g,render_template
import os
import commands
from apis.api_comm import *
import traceback
from log import g_log
from apis.request_route_handler import *
from apis.static_request_route_handler import *
from apis.public_verify_request_route_handler import *

def flask_init(app):
    log=g_log.get_sys_log()
    
    log.info('flask_init')
    


    '''
     动态路由配置，根据客户端请求的url路由至指定交易文件
    '''
    request_route_handler_view = RequestRouteHandler.as_view('request_route_handler')
    app.add_url_rule('/apis/request_route_handler/<route_root>/<route_name>'
                             , view_func=request_route_handler_view, methods=['GET', 'POST', 'PUT'])

    public_verify_request_route_handler_view = PublicVerifyRequestRouteHandler.as_view('public_verify_request_route_handler')
    app.add_url_rule('/'
                             , view_func=public_verify_request_route_handler_view, methods=['GET', 'POST'])

    static_request_route_handler_view = StaticRequestRouteHandler.as_view('static_request_route_handler')
    app.add_url_rule('/<path:filename>'
                             , view_func=static_request_route_handler_view, methods=['GET'])



    '''
    设置 before after teardown
    '''
    app.before_request(before_request)
    app.after_request(after_request)
    app.teardown_request(teardown_request)
    app.errorhandler(404)(exception_handler_404)
    app.errorhandler(500)(exception_handler_500)


def before_request():
    print 'before_request'
    log=g_log.get_sys_log()

    g.db_session = None


    s = get_txn_begin_log()
    print s
    log.info(s)

    #print 'request:[%s]' % request
    #print 'request header :[%s]' % request.headers
    #print 'request data :[%s]' % request.data

    #print 'request user_agent:[%s]' % request.user_agent
    #print 'request url:[%s]' % request.url
    #log.info('request url:[%s]' % request.url)
    
    


def after_request(response):
    log=g_log.get_sys_log()

    print 'after_request'



    #print 'response:[%s]' % response
    #print 'response type:[%s]' % type(response)

    #print 'response header :[%s]' % response.headers
    #log.info( 'response header :[%s]' % response.headers)

    #print 'response data:[%s]' % response.data
    #log.info( 'response data:[%s]' % response.data)
    #print 'response data type:[%s]' % type(response.data)

    #rsp_code = get_ret_code(response.data)
    #print 'rsp_code:[%s]' % rsp_code


    '''
     对于一般情况，只有返回码正常的才进行事务提交，对于返回码错误的进行事务回滚
     如果有特殊情况，需要交易代码中手动进行事务的操作
    '''
    '''
    #if rsp_code == const.RET_SUCCESS :
    if rsp_code[0] == '0' :
        g.db_session.commit()
    else :
        if g.db_session != None :
            g.db_session.rollback()

    if g.db_session != None :
        g.db_session.close()
    '''

    s = get_txn_end_log(response)
    print s
    log.info(s)
    



    return response

'''
 无论是否出现异常都会进入该函数中
 - 出现异常时，捕获异常，输出异常信息
 - 未出现异常时，response对象为None
'''
def teardown_request(response):
    log=g_log.get_sys_log()

    print "teardown_request"
    print response

    if response == None:
        return
    print 'here i am'

    if g.db_session != None :
        g.db_session.rollback()
        g.db_session.close()

    s=traceback.format_exc()
    print s
    log.error(s)


    return


'''
  warning!!!
  如果是flask底层报错(未进入交易处理框架)，则flask会设置默认的返回内容。
  例如测试命令 curl "http://139.196.169.237:9997/apis/err_request_route_handler/charger_heart_beat/heart_beat_tmp?charger_id=1"

  以下函数是设置自定义的错误返回内容，目的是尽量返回200，错误为系统错误，不能捕捉到报错信息
  以下函数处理完会进入after_request和teardown_request
'''
def exception_handler_500(exception):
    log=g_log.get_sys_log()

    if g.db_session != None :
        g.db_session.rollback()
        g.db_session.close()

    log.error('500发生异常')
    return ret_func(const.RET_SYS_ERROR, '', {})


def exception_handler_404(exception):
    log=g_log.get_sys_log()

    if g.db_session != None :
        g.db_session.rollback()
        g.db_session.close()

    log.error('404发生异常')
    return ret_func(const.RET_SYS_ERROR, '', {})
