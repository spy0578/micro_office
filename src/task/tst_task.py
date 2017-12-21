#-*- coding:utf-8 -*-
from datetime import datetime
import time
import os
from base.log import g_task_log
from base.ftp import *
from etc.config import  *
from task_main import g_task


def tick1():
    log=g_task_log.get_sys_log()

    log.info('Tick1! The time is: %s' % datetime.now())

    ftp = FTPSync(configs[config_type].POSITION_DATA_FTP_HOST)
    ftp.login(configs[config_type].POSITION_DATA_FTP_USERNAME, configs[config_type].POSITION_DATA_FTP_PASSWORD)
    #ftp判断目标文件是否存在（data.flg），如果存在则获取data文件
    if ftp._is_ftp_file(configs[config_type].POSITION_DATA_FILE_DIR+configs[config_type].POSITION_DATA_FLAG_FILE) is True:
        ftp.get_file(configs[config_type].POSITION_DATA_FILE_DIR+configs[config_type].POSITION_DATA_FILE, configs[config_type].POSITION_DATA_LOCAL_FILE_DIR) 

        scheduler = g_task.get_scheduler()
        scheduler.pause_job('tick1')



    #print('Tick1! The time is: %s' % datetime.now())
