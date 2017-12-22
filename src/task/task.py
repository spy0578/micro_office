# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')


def aps_test(x):
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x


def aps_pause(x):
    scheduler.pause_job('interval_task')
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x


def aps_resume(x):
    scheduler.resume_job('interval_task')
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x

scheduler = BlockingScheduler()
trigger1 = CronTrigger(hour='*', minute='*', second='*/10')
trigger2 = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(seconds=12))
trigger3 = DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(seconds=24))
trigger4 = IntervalTrigger(seconds=3)
scheduler.add_job(func=aps_test, args=('定时任务',), trigger=trigger1, id='cron_task')
scheduler.add_job(func=aps_pause, args=('一次性任务,停止循环任务',), trigger=trigger2, id='pause_task')
scheduler.add_job(func=aps_resume, args=('一次性任务,恢复循环任务',), trigger=trigger3, id='resume_task')
scheduler.add_job(func=aps_test, args=('循环任务',), trigger=trigger4, id='interval_task')
scheduler._logger = logging

scheduler.start()
