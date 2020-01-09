# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_patientMessage.py
    Time:    2019/12/2 13:53
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *


@allure.feature("帮助中心管理")
class Test_patientListMessage:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]
        self.orgId = response["responseData"]["roleList"][0]["orgId"]
        self.itemOrgId = response["responseData"]["itemOrgId"]

    @allure.title("消息类别")
    @allure.story("我创建的")
    def test_getNOticeTypeList(self):
        url = host + portlogin + "/notice/getNOticeTypeList.json"
        data = {
            "time": time_up,
            "type": 2,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("数据列表展示")
    @allure.story("我创建的")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_findNoticeInfoPage(self, start, end):
        url = host + portlogin + "/notice/findNoticeInfoPage.json"
        data = {
            "page": 1,
            "size": 15,
            "noticeTypeId": "",
            "noticeStatus": "",
            "startDate": start,
            "endDate": end,
            "noticeTitle": "",
            "modularType": 2,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("创建消息-平台信息")
    @allure.story("我创建的-创建消息")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = {
            "listType": 2,
            "status": 1,
            "orgTypeIds": "33, 35, 38",
            "path": 400,
            "orgName": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "云平台")

    @allure.title("创建消息-查找可以发信息的对象")
    @allure.story("我创建的-创建消息")
    def test_patientSearch(self):
        url = host + port_dataindex + "/patient/search.json"
        data = {
            "searchWord": "",
            "orgPath": f"400, {self.itemOrgId},",
            "orgType": 38,
            "orgId": self.itemOrgId,
            "sourceType": 2,
            "sourceRecord": 1,
            "neSourceDataType": 3,
            "page": 1,
            "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    def addresseeId(self):
        url = host + port_dataindex + "/patient/search.json"
        data = {
            "searchWord": "",
            "orgPath": f"400, {self.itemOrgId},",
            "orgType": 38,
            "orgId": self.itemOrgId,
            "sourceType": 2,
            "sourceRecord": 1,
            "neSourceDataType": 3,
            "page": 1,
            "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        ids = []
        for i in result[1]["responseData"]["content"]:
            ids.append(i["orgUserId"])
        return ids

    @allure.title("创建消息")
    @allure.story("我创建的-创建消息")
    def test_createNotice(self):
        url = host + portlogin + "/notice/createNotice.json"
        addresseeId = self.addresseeId()
        allure.attach(f"内部参数：addresseeId={addresseeId}")
        data = {
            "addresseeId": addresseeId[0],
            "title": "发送邮件",
            "noticeTypeId": 2,
            "content": "<p> 没有</p>",
            "autoSave": "false",
            "recipientAll": 0,
            "attachmentURL": "[]",
            "operatorId": self.authUserId,
            "noticeStatus": 2,
            "modularType": 2,
            "operatorFunction": "51060-addMsg",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    def noticeId(self):
        url = host + portlogin + "/notice/findNoticeInfoPage.json"
        data = {
            "page": 1,
            "size": 15,
            "noticeTypeId": "",
            "noticeStatus": "",
            "startDate": "",
            "endDate": "",
            "noticeTitle": "",
            "modularType": 2,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result, resultdic = assert_get(url, data, self.cook)
        ids = []
        for i in resultdic["responseData"]["content"]:
            ids.append(i["noticeId"])
        return ids

    @allure.title("消息详情")
    @allure.story("我创建的")
    def test_getCreateAndExamineByNoticeId(self):
        url = host + portlogin + "/notice/getCreateAndExamineByNoticeId.json"
        noticeId = self.noticeId()
        allure.attach(f"传值参数：noticeId={noticeId}")
        if len(noticeId) > 0:
            data = dict(noticeId=noticeId[0],
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_get(url, data, self.cook)

    @allure.title("显示要审核的-数据的个数")
    @allure.story("审核记录")
    def test_getWaitTotal(self):
        url = host + portlogin + "/notice/getWaitTotal.json"
        data = {
            "modularType": 2,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("审核记录-列表展示")
    @allure.story("审核记录")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_findNoticeExaminetPage(self, start, end):
        url = host + portlogin + "/notice/findNoticeExaminetPage.json"
        data = {
            "page": 1,
            "size": 15,
            "noticeTypeId": "",
            "noticeStatus": "",
            "startDate": start,
            "endDate": end,
            "noticeTitle": "",
            "modularType": 2,
            "operatorFunction": "51060-viewAutidingRecord",
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("审核-不通过")
    @allure.story("审核记录")
    @pytest.mark.parametrize("status", (1, 3))
    def test_updateStatus(self, status):
        """
        :param status: 表示审核的状态 1：通过；3：不通过
        :return:
        """
        url = host + portlogin + "/notice/updateStatus.json"
        data = {
            "auditOrgUserId": self.authUserId,
            "noticeId": 13817,
            "status": status,
            "auditOpinion": "不同意",
            "auditAndRepealFlag": "auditFlag",
            "repealOpinion": "不同意",
            "operatorFunction": "51060-lookThrough",
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)
