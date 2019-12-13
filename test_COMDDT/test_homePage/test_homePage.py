#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: test_homePage.py
@time: 2019/9/29 9:16

@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("首页")
class Test_homePage:

    @allure.title("登录")
    @allure.step("参数：login={0}")
    def test_login(self, login):
        response1, cook = login
        url = host + portlogin + "/ext/shop/login.json"
        overWrite_assert_post_xls_hint(url, logindata, cook, systemPath, "登录")

    @allure.title("获取病种下拉列表")
    @allure.story("首页显示")
    @allure.step("参数：login={0}")
    def test_getTreeListByUser(self, login):
        response1, cook = login
        url = host + port_resource + "/disease/getTreeListByUser.json"
        data = dict(operatorId=response1["authUserId"])
        assert_get(url, data, cook, "慢阻肺")

    @allure.title("菜单配置列表")
    @allure.story("首页显示")
    def test_getMenu(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/ext/system/getMenu.json"
        header = {"cookie": dlogin}
        data = dict(id=response1["ids"],
                    idToken=response1["idToken"],
                    userAllMenu="true",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, headers=header)

    @allure.title("系统消息")
    @allure.story("首页显示")
    @allure.step("参数：login={0}")
    def test_getNoticeByNoticeType(self, login):
        response1, cook = login
        url = host + portlogin + "/home/getNoticeByNoticeType.json"
        data = dict(modularType=1, noticeTypeIds=4,
                    page=1, size=8,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("公告")
    @allure.story("首页显示")
    @allure.step("参数：login={0}")
    def test_getNoticeByNoticeType2(self, login):
        response1, cook = login
        url = host + portlogin + "/home/getNoticeByNoticeType.json"
        data = dict(modularType=1,
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("人次数据-有数据展示")
    @allure.story("首页显示")
    @allure.step("参数：login={0}")
    def test_findCount(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/home/findCount.json"
        data = dict(medCode="COPD-001", operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = assert_get(url, data, cook)
        assert len(result[1]["responseData"]) > 6, "人数数据-至少有六条数据"
        assert "totalCount" in result[0], "有人数这个字段"

    @allure.title("日历上的数据")
    @allure.story("首页显示")
    @allure.step("参数：login={0}")
    def test_calendarCount(self, login):
        response1, cook = login
        url = host + portlogin + "/userhome/calendar/count.json"
        data = dict(orgUserId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("显示上次登录的时间")
    @allure.story("首页显示")
    def test_getLastUserInfo(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/home/getLastUserInfo.json"
        header = {"cookie": dlogin}
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, headers=header)

    @allure.title("预警提示")
    @allure.story("首页显示")
    @allure.step("参数：login={0}")
    def test_findRecord(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/findRecord.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    medCode="COPD-001",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("审核情况")
    @allure.story("首页显示")
    def test_getAudit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/home/getAudit.json"
        header = {"cookie": dlogin}
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, headers=header)

    @allure.title("跳转质控界面，这里是指控的菜单列表")
    @allure.story("首页操作")
    @allure.step("参数：login={0}")
    def test_getGroupInfoList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getGroupInfoList.json"
        data = dict(multiCenter=0,
                    groupType="质量控制",
                    medCode="COPD-001",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("跳转病例讨论-带有个人的接口")
    @allure.story("首页操作")
    @allure.step("参数：login={0}")
    def test_tipsInfo(self, login):
        response1, cook = login
        url = host + port_bbs + "/bbs/tips/info.json"
        data = dict(dataType=1, dataId=665544, operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, str(response1["authUserId"]))


if __name__ == '__main__':
    pytest.main()
