#-*- coding:utf-8 -*-
import logging
import os
import platform

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>' 
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    sysstr = platform.system()
    
    @staticmethod
    def init_app(app): 
        pass

class DevelopmentConfig(Config): 
    DEBUG = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 

    REDIS_URI       = os.environ.get('DEV_REDIS_URI') or \
                                     '127.0.0.1'
    REDIS_PORT      = os.environ.get('DEV_REDIS_PORT') or \
                                     '6379'
    SESSION_REDIS_NUM   = os.environ.get('SESSION_REDIS_NUM') or \
                                     '1'
    PLAT_REDIS_NUM   = os.environ.get('PLAT_REDIS_NUM') or \
                                     '2'


    '''
     webserver.py 日志参数配置
     LOG_FILE_DIR=LOG_FILE_DIR_PRE+DATE+LOG_FILE_DIR_POST
    '''
    WEB_SERVER_LOG_LEVEL       = logging.DEBUG
    WEB_SERVER_LOG_FILE_NAME   = os.environ.get('WEB_SERVER_LOG_FILE_NAME') or \
                                     'log'

    TASK_LOG_LEVEL       = logging.DEBUG
    TASK_LOG_FILE_NAME   = os.environ.get('TASK_LOG_FILE_NAME') or \
                                     'log.txt'

    print 'sysstr:%s' % Config.sysstr
    if(Config.sysstr =="Windows"):
        print ("Windows")
        WEB_SERVER_LOG_FILE_DIR_PRE = os.environ.get('WEB_SERVER_LOG_FILE_DIR_PRE') or \
                               'E:\work_project\micro_office\log'

        STATIC_TEMPLATE_FOLDER = os.environ.get('STATIC_TEMPLATE_FOLDER') or \
                               'E:\work_project\micro_office\web'

        TASK_LOG_FILE_DIR_PRE = os.environ.get('TASK_LOG_FILE_DIR_PRE') or \
                                'E:\work_project\micro_office\log'

        SERVER_IP = os.environ.get('SERVER_IP') or \
                    '168.40.5.23'
        SQLALCHEMY_URI              = os.environ.get('DEV_SQLALCHEMY_URL') or \
                                                 'sqlite:///../db/sqlalchemy.db'

       
    elif(Config.sysstr =="Linux"):
        print ("Linux")
        WEB_SERVER_LOG_FILE_DIR_PRE = os.environ.get('WEB_SERVER_LOG_FILE_DIR_PRE') or \
                                         '/home/guozl/lab/micro_office/log'

        STATIC_TEMPLATE_FOLDER = os.environ.get('STATIC_TEMPLATE_FOLDER') or \
                                         '/home/guozl/lab/micro_office/web'

        TASK_LOG_FILE_DIR_PRE = os.environ.get('TASK_LOG_FILE_DIR_PRE') or \
                                '/home/guozl/lab/micro_office/log'

        SERVER_IP = os.environ.get('SERVER_IP') or \
                    '168.40.63.132'

        SQLALCHEMY_URI              = os.environ.get('DEV_SQLALCHEMY_URL') or \
                                                 'sqlite:////home/guozl/lab/micro_office/db/sqlalchemy.db'
    else:
        print ("others")
        WEB_SERVER_LOG_FILE_DIR_PRE = os.environ.get('WEB_SERVER_LOG_FILE_DIR_PRE') or \
                                         '/Users/spy0578/lab/micro_office/log'

        STATIC_TEMPLATE_FOLDER = os.environ.get('STATIC_TEMPLATE_FOLDER') or \
                                         '/Users/spy0578/lab/micro_office/web'

        TASK_LOG_FILE_DIR_PRE = os.environ.get('TASK_LOG_FILE_DIR_PRE') or \
                                'E:\work_project\micro_office\log'

        SERVER_IP = os.environ.get('SERVER_IP') or \
                    '168.40.5.23'

        SQLALCHEMY_URI              = os.environ.get('DEV_SQLALCHEMY_URL') or \
                                                 'sqlite:///../db/sqlalchemy.db'


    WEB_SERVER_LOG_FILE_DIR_POST  = os.environ.get('WEB_SERVER_LOG_FILE_DIR_POST') or \
                                     'web_txn'

    TASK_LOG_FILE_DIR_POST  =   os.environ.get('TASK_LOG_FILE_DIR_POST') or \
                                    'task'

    POSITION_DATA_FTP_HOST = os.environ.get('POSITION_DATA_FTP') or \
                                    '168.40.63.132'
    POSITION_DATA_FTP_PORT = os.environ.get('POSITION_DATA_PORT') or \
                                    '21'
    POSITION_DATA_FTP_USERNAME = os.environ.get('POSITION_DATA_USERNAME') or \
                                    'guozl'
    POSITION_DATA_FTP_PASSWORD = os.environ.get('POSITION_DATA_PASSWORD') or \
                                    'guozl'

    POSITION_DATA_FLAG_FILE = os.environ.get('POSITION_DATA_FLAG_FILE') or \
                                    'tst_file.flg'
    POSITION_DATA_FILE = os.environ.get('POSITION_DATA_FILE') or \
                                    'tst_file'
    POSITION_DATA_FILE_DIR = os.environ.get('POSITION_DATA_FILE_DIR') or \
                                    '/home/guozl/lab/ftp_dir/'
    POSITION_DATA_LOCAL_FILE_DIR = os.environ.get('POSITION_DATA_LOCAL_FILE_DIR') or \
                                    '/home/guozl/lab/local/'
    POSITION_DATA_DONE_FILE = os.environ.get('POSITION_DATA_DONE_FILE') or \
                                    'tst_file.done'

    #折线图展示几天内的数据，包括当日
    POSITION_DATA_LINE_CHARTS_DAYS = os.environ.get('POSITION_DATA_LINE_CHARTS_DAYS') or \
                                    3



class TestingConfig(Config): 
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') 
        #'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
        #'sqlite:///' + os.path.join(basedir, 'data.sqlite')

configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


'''
 配置启动 开发模式、测试模式 or 产品部署模式
'''
config_type = 'development'

