#-*- coding:utf-8 -*-
from datetime import datetime
import time
import os
from base.log import g_task_log
from base.ftp import *
from etc.config import  *
from task_init import g_task
from db.dbinit import DBSession
from db.dborm.dborm import TblParaStatInfo
import shutil  


def get_position_data():
    log=g_task_log.get_sys_log()

    log.info('get_position_data! The time is: %s' % datetime.now())

    ftp = FTPSync(configs[config_type].POSITION_DATA_FTP_HOST)
    ftp.login(configs[config_type].POSITION_DATA_FTP_USERNAME, configs[config_type].POSITION_DATA_FTP_PASSWORD)
    #ftp判断目标文件是否存在（data.flg），如果存在则获取data文件
    if ftp._is_ftp_file(configs[config_type].POSITION_DATA_FILE_DIR+configs[config_type].POSITION_DATA_FLAG_FILE) is True:
        shutil.rmtree(configs[config_type].POSITION_DATA_LOCAL_FILE_DIR)
        os.mkdir(configs[config_type].POSITION_DATA_LOCAL_FILE_DIR)
        ftp.get_file(configs[config_type].POSITION_DATA_FILE_DIR+configs[config_type].POSITION_DATA_FILE, configs[config_type].POSITION_DATA_LOCAL_FILE_DIR) 

        #读取文件内容并保存到表中，然后设置标志文件
        try:
            db_session = DBSession()
            query = db_session.query(TblParaStatInfo).all()

            for i in range(len(query)):
                print 'para_stat_id:[%d], para_type_id:[%d]' % (query[i].para_stat_id, query[i].para_type_id)
        except Exception, e:
            print 'get_position_data except:[%s]' % e
            return
        finally:
            db_session.close()

        os.mknod(configs[config_type].POSITION_DATA_LOCAL_FILE_DIR + configs[config_type].POSITION_DATA_DONE_FILE)


        print 'finish this time:get_position_data!!!!'

        scheduler = g_task.get_scheduler()
        scheduler.pause_job('get_position_data')




