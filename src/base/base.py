# -*- coding:utf-8 -*-
from flask import Flask, request, make_response,redirect,ctx,g,render_template
import os
import commands
from apis.api_comm import *
import traceback
from log import g_log
from apis.request_route_handler import *


def exec_cmd(command):
    print 'command:[%s]' % command
    ret = commands.getstatusoutput(command)
    if ret[0] != 0:
        raise ValueError('exec:[%s] error:[%s]' % (command, ret[1]))
    return ret[1]


