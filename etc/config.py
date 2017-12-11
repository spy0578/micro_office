#-*- coding:utf-8 -*-
import logging
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>' 
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    
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

    SQLALCHEMY_URI              = os.environ.get('DEV_SQLALCHEMY_URL') or \
                                                 'sqlite:///./sqlalchemy.db'

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
    WEB_SERVER_LOG_FILE_DIR_PRE   = os.environ.get('WEB_SERVER_LOG_FILE_DIR_PRE') or \
                                     '/Users/spy0578/lab/micro_office/log'
    WEB_SERVER_LOG_FILE_DIR_POST  = os.environ.get('WEB_SERVER_LOG_FILE_DIR_POST') or \
                                     'web_txn'


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

