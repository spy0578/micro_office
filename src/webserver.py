# -*- coding: utf-8 -*-
import traceback  
import sys
import urllib
import urllib2
import json
from flask import Flask, request, make_response,redirect,ctx,g,render_template
from datetime import *
from sqlalchemy.sql import and_,or_
import time
sys.path.append("..")
from etc.config import *
from base.flask_base import *
from base.log import g_log


reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.debug = True
app.template_folder = '/dvlp/ichrg_repos/templates'



'''
 初始化日志全局对象
'''
g_log.init_log(configs[config_type].WEB_SERVER_LOG_LEVEL, configs[config_type].WEB_SERVER_LOG_FILE_NAME, 
               configs[config_type].WEB_SERVER_LOG_FILE_DIR_PRE, configs[config_type].WEB_SERVER_LOG_FILE_DIR_POST)
log=g_log.get_sys_log()


flask_init(app)

if __name__ == '__main__':

    
    '''
    set use_reloader=False avoid starting monitor thread
    '''
    app.run(host='127.0.0.1', port=9999, debug=False, use_reloader=True, threaded=False)
    #app.run(host='0.0.0.0', port=9999, debug=True, use_reloader=False)


