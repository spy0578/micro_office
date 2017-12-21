#-*- coding:utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
import time

import sys
sys.path.append("..")
sys.path.append("../..")

from etc.config import *
from base.design_pattern.singleton import Singleton
from base.log import g_task_log
#from task.day_end_task import *
#from tst_task  import *
#from tst_task2 import *


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(1),
}
job_defaults = {
    'coalesce': True,
    'max_instances': 1
}

class Task(Singleton) :
    scheduler = None

    def get_scheduler(self):
        return self.scheduler


    def init_task(self):
        print 'task init'
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

        '''
         start add jobs
         check if jobstores has these jobs
        #if self.scheduler.get_job('day_end_task') is None :
        #    self.scheduler.add_job(day_end_task, trigger='cron', args=None, id='day_end_task', hour='0') # using unix cron
        '''
        '''
        if self.scheduler.get_job('tick6') is None :
            trigger1 = CronTrigger(hour='*', minute='*', second='*/10')
            self.scheduler.add_job(tick1, trigger=trigger1, id='tick1')
            #self.scheduler.add_job(tick2, trigger='cron', id='tick2', second='*/5', hour='*')  # tst job

        self.scheduler.start()
        try:
            while True:
                time.sleep(2)
                print 'sleep'
        except(KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
            print 'exit the job'
        '''

g_task_log.init_log(configs[config_type].TASK_LOG_LEVEL, configs[config_type].TASK_LOG_FILE_NAME, 
               configs[config_type].TASK_LOG_FILE_DIR_PRE, configs[config_type].TASK_LOG_FILE_DIR_POST, True)

print 'task_main g_task_log:[%s]' % g_task_log
log=g_task_log.get_sys_log()
print 'task_main log:[%s]' % log

#init task
g_task=Task()
g_task.init_task()
