from base.log import g_task_log
from datetime import datetime
import time
import os



def tick2():
    log=g_task_log.get_sys_log()
    log.debug('Tick2! The time is: %s' % datetime.now())
    #print('Tick1! The time is: %s' % datetime.now())
