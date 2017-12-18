# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g, jsonify
from db.redis_init import GlobalRedisAccess, g_rds_access
from db.dbinit import DBSession
from base.comm_const import *
from base.https_base import *


def update_access_token(client_id, client_secret):
	request_url = const.GET_ACCESS_TOKEN_URL+'grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
	
	headers = {
     "Content-Type": "application/x-www-form-urlencoded"
          }

	rst = https_post(request_url, headers=headers)
	print 'update_access_token:[%s]' % rst

	rst_dict = eval(rst)

	try:
		access_token = rst_dict["access_token"]
		print 'access_token:[%s]' % access_token
	except Exception as e:
		print e
		return False

	#<todo>存储在redis中
	rds = g_rds_access.get_session_rds()
	rds.set(const.REDIS_ACCESS_TOKEN, access_token)

	g.access_token = access_token

	return True


def modify_user_group(user_id, group_id):
	print 'g.access_token:[%s]' % g.access_token

	request_url = const.MODIFY_USER_GROUP_URL+g.access_token

	post_params = {
		"openid" : user_id,
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
		print e
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
		return False











