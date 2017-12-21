from task_main import g_task
from apscheduler.triggers.cron import CronTrigger
from tst_task  import *

scheduler = g_task.get_scheduler()
trigger1 = CronTrigger(hour='*', minute='*', second='*/5')
scheduler.add_job(tick1, trigger=trigger1, id='tick1')


scheduler.start()
try:
    while True:
        time.sleep(2)
        print 'sleep'
except(KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print 'exit the job'
