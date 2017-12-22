#-*- coding:utf-8 -*-
from task_init import g_task
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from get_position_data  import *
from resume_jobs import *
from draw_line_chart import *
import datetime

scheduler = g_task.get_scheduler()

'''
    resume_jobs  设置在凌晨2点运行，确保所有任务可以正常执行
    
    get_position_data
        从ftp服务器获取头寸数据，并保存在表中

    draw_line_chart
'''

#scheduler.add_job(get_position_data, trigger=CronTrigger(hour='*', minute='*', second='*/5'), id='get_position_data')
scheduler.add_job(draw_line_chart, trigger=CronTrigger(hour='*', minute='*', second='*/5'), id='draw_line_chart')
scheduler.add_job(resume_jobs, trigger=DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(seconds=20)), id='resume_jobs')

scheduler.start()
try:
    while True:
        time.sleep(2)
        print 'sleep'
except(KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print 'exit the job'
