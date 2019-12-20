#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: running.py
@time: 2019/10/18 13:50
@Author:Terence
"""
import os,sys
from readConfig import get_email
from public.configEmail import send_zip


path1 = os.path.dirname(__file__)
pathcase = os.path.join(path1,"test_COMDDT")
sender = get_email("sender")
passwd = get_email("passwd")
toget = get_email("toget")

#下面是执行终端命令的代码
def t1est_TestRun():
    # ------------------------------第二种方法----------------------------------
    # 重复执行 20次（后面可以跟class，一定要有参数 -x 与错误停止）
    # pytest -v -q --alluredir ./report/xml/ --reruns 5 --count=20 --repeat-scope=session
    os.system(f"pytest {pathcase}  -n 5 --alluredir ./report/test/ --reruns 5")
    os.system(r"allure generate ./report/test/ -c -o ./report/html/")
    # 发送邮件
    if 1 == 0:
        send_zip(sender, toget, passwd)


path = sys.path
print(f"path = {path}")