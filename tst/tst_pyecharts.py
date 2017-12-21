#!/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from pyecharts import Line, Pie, Grid
from pyecharts_snapshot.main import make_a_snapshot

attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [5, 20, 36, 10, 10, 100]
v2 = [55, 60, 16, 20, 15, 80]
line = Line("折线图示例")
line.add("商家A", attr, v1, mark_point=["average"])
line.add("商家B", attr, v2, is_smooth=True, mark_line=["max", "average"])
line.render('test.html')

make_a_snapshot('test.html', 'test.jpeg')
