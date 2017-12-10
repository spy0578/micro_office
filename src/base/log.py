#-*- coding:utf-8 -*-
import logging
import logging.handlers
import datetime
from design_pattern.singleton import Singleton
import os
from etc.config import *

# without this setting, apsheduler wont use
# according to http://stackoverflow.com/questions/28724459/no-handlers-could-be-found-for-logger-apscheduler-executors-default
#logging.basicConfig()


####log file base dir####
LOG_NAME = 'MyLogger1'
#Bytes
MAX_LOG_FILE_SIZE = 100000
DEFAULT_LOG_LEVEL = logging.DEBUG
###NOT SURE, MAX FILE NUM??###
MAX_LOG_FILE_NUM = 15

class LogBase():
    filename = ''
    #log object
    sysLog = None
    level = None

    handler = None
    formatter = None

    #current date
    currDate = None

    dir_pre  = None
    dir_post = None
    log_file_name = None
    log_level = None

    def __init__(self):
        print "__init__"


    def init_log(self, log_level, log_file_name, dir_pre, dir_post):

        self.log_level = log_level
        self.log_file_name = log_file_name
        self.dir_pre  = dir_pre
        self.dir_post = dir_post

        now = datetime.datetime.now()
        self.currDate = now.strftime('%Y%m%d')


        self.sysLog = logging.getLogger(self.log_file_name)
        self.sysLog.setLevel(self.log_level)


        tmpPath = self.dir_pre + "/" + self.currDate + "/" + self.dir_post
        # check dir if exist, otherwise mkdir
        if os.path.exists(tmpPath) is False :
            os.makedirs(tmpPath)


        self.handler = logging.handlers.RotatingFileHandler(
                       tmpPath+"/"+log_file_name, maxBytes=MAX_LOG_FILE_SIZE, backupCount=MAX_LOG_FILE_NUM)

        self.formatter = logging.Formatter('%(threadName)s %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%H:%M:%S')

        self.handler.setFormatter(self.formatter)

        self.sysLog.addHandler(self.handler)
        

    def setLogLevel(self,level):
        self.level = level
        self.sysLog.setLevel(self.level)



    def get_sys_log(self):
        return self.sysLog



    ####this function used by BATCH_TASK###
    ####date switch###
    def changeLogPath(self):
        now = datetime.datetime.now()
        tmpCurrDate = now.strftime('%Y%m%d')
        if tmpCurrDate > self.currDate :
            self.currDate = tmpCurrDate
            tmpPath = self.dir_pre + "/" + self.currDate + "/" + self.dir_post


            if os.path.exists(tmpPath) is False :
                    os.makedirs(tmpPath)

            self.handler = logging.handlers.RotatingFileHandler(
                           tmpPath+"/"+LOG_NAME, maxBytes=MAX_LOG_FILE_SIZE, backupCount=MAX_LOG_FILE_NUM)
            self.handler.setFormatter(self.formatter)
            self.sysLog.addHandler(self.handler)






'''
init log
'''
g_log=LogBase()


