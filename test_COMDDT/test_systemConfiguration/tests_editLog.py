#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: tests_editLog.py
@time: 2019/9/30 11:57
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("操作日志")
class Test_editLog:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response1["responseData"]["loginName"]

    def test_getOpLogBusinessPage(self):
        url = host + portlogin + "/log/opLogBusiness/getOpLogBusinessPage.json"
        data = dict(
            keyword="", opUserName="", ip="", opResult="", startDate="", endDate="",
            page=1, size=10, operatorFunction="51046-viewLog",
            operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        print("result =",result.text)
        resultdic = json.loads(result.text)['responseData']["content"]
        print(f"\nusername={self.userName},\nreslt = {resultdic[0]['opUserName']}")
        assert self.userName == resultdic[0]['opUserName'], "最后一个的用户名是他自己"