#-*- coding:utf-8 -*-
from datetime import datetime
import time
import os
from base.log import g_task_log
from base.ftp import *
from etc.config import  *
from task_init import g_task

def resume_jobs():
    log=g_task_log.get_sys_log()
    scheduler = g_task.get_scheduler()

    scheduler.resume_job('get_position_data')
    print 'resume_job done'



