# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g, jsonify
from db.redis_init import GlobalRedisAccess, g_rds_access
from db.dbinit import DBSession
from base.comm_const import *
from base.https_base import *

'''
   获取access_token
'''
def update_access_token(client_id, client_secret):
    request_url = const.GET_ACCESS_TOKEN_URL+'grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
	
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    rst = https_post(request_url, headers=headers)
    print 'update_access_token:[%s]' % rst
    rst_dict = eval(rst)

    try: 
        if rst.find('error') == -1 :
            access_token = rst_dict["access_token"]

            rds = g_rds_access.get_session_rds()
            rds.set(const.REDIS_ACCESS_TOKEN, access_token)

            g.access_token = access_token

            return True

        else :
            error = rst_dict["error"]
            error_description = rst_dict["error_description"]

            g.errinfo = {'errcode':'', 'errmsg':error, 'errdes':error_description}

            return False

    except Exception as e:
        print e
        g.errinfo = {'errcode':'', 'errmsg':e, 'errdes':''}

        return False

'''
   修改用户的组信息
'''
def modify_user_group(user_lst, group_id):
    print 'g.access_token:[%s]' % g.access_token

    request_url = const.MODIFY_USER_GROUP_URL+g.access_token

    post_params = {
        "useridList" : user_lst,
        "to_groupid" : group_id
    }

    print 'post_params:[%s]' % post_params

    rst = https_post(request_url, post_params)
    print 'modify_user_group:[%s]' % rst

    rst_dict = eval(rst)

    try :
	    err_code = rst_dict["errcode"]
	    print 'err_code:[%s]' % err_code
    except Exception as e:
        g.errinfo = {'errcode':'', 'errmsg':e, 'errdes':''}
        return False


    if err_code == const.PUBLIC_PLAT_RET_ACCESS_TOKEN_ERROR or err_code == const.PUBLIC_PLAT_RET_ACCESS_TOKEN_INVALID:
        print 'access_token错误!'
        if update_access_token(const.PUBLIC_PLAT_CLIENT_ID, const.PUBLIC_PLAT_CLIENT_SECRET) is False :
            return False
        else :
            modify_user_group(user_lst, group_id)
    elif err_code == const.PUBLIC_PLAT_RET_SUCCESS :
        return True
    else :
        g.errinfo = {'errcode':rst_dict['errcode'], 'errmsg':rst_dict['errmsg'], 'errdes':''}
        return False

'''
    获取用户组信息
'''
def get_user_group_id(user_id):
    print 'g.access_token:[%s]' % g.access_token

    request_url = const.QUERY_GROUP_URL+g.access_token

    post_params = {
        "userid" : user_id
    }

    print 'post_params:[%s]' % post_params

    rst = https_post(request_url, post_params)
    print 'get_user_group_id:[%s]' % rst

    rst_dict = eval(rst)

    if rst.find('errcode') == -1 :
        try :
            groupid = rst_dict["groupid"]
            return groupid

        except Exception as e:
            g.errinfo = {'errcode':'', 'errmsg':e, 'errdes':''}
            return ''

    else :
        rst_dict = eval(rst)
        try :
            err_code = rst_dict["errcode"]
            print 'err_code:[%s]' % err_code
        except Exception as e:
            g.errinfo = {'errcode':'', 'errmsg':e, 'errdes':''}
            return ''


        if err_code == const.PUBLIC_PLAT_RET_ACCESS_TOKEN_ERROR or err_code == const.PUBLIC_PLAT_RET_ACCESS_TOKEN_INVALID:
            print 'access_token错误!'
            if update_access_token(const.PUBLIC_PLAT_CLIENT_ID, const.PUBLIC_PLAT_CLIENT_SECRET) is False :
                return ''
            else :
                return get_user_group_id(user_id)
        else :
            g.errinfo = {'errcode':rst_dict['errcode'], 'errmsg':rst_dict['errmsg'], 'errdes':''}
            return ''

def push_material_to_users(user_lst, latest_meterial_id, meterial_type):
    print 'g.access_token:[%s]' % g.access_token
    request_url = const.PUSH_MATERIAL_INFO_URL+g.access_token

    post_params = {
        "touser": user_lst,
        "mpnews":{
            "media_id":latest_meterial_id
        },
        "msgtype": meterial_type
    }        

    print 'post_params:[%s]' % post_params

    rst = https_post(request_url, post_params)
    print 'push_material_to_users:[%s]' % rst


#def create_menu():









