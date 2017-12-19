# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g,render_template
import os
import commands
import traceback
from log import g_log



def exec_cmd(command):
    print 'command:[%s]' % command
    ret = commands.getstatusoutput(command)
    if ret[0] != 0:
        raise ValueError('exec:[%s] error:[%s]' % (command, ret[1]))
    return ret[1]


