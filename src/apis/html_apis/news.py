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

        print 'request.args:', request.args
        parameters = request.args

        '''
         分隔符为&，截取字符串
        '''
        param_dict = parameters.to_dict()

        page = param_dict['page']
        search = param_dict['search']

        
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


        return ret_func(const.RET_SUCCESS, 'success', data)
    
        return jsonify({'tasks': tasks})



