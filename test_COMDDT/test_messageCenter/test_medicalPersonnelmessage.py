#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: test_medicalPersonnelmessage.py
@time: 2019/9/29 11:52
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("医疗人员信息")
class Test_medicalPersonnelmessage:

    @allure.title("消息类型")
    @allure.story("消息类别")
    @allure.step("参数：login={0}")
    def test_getNOticeTypeList(self, login):
        response1, cook = login
        hint = ("医院通知", "项目消息", "招募信息", '平台通知', '综合新闻')
        url = host + portlogin + "/notice/getNOticeTypeList.json"
        data = dict(time=1569735394000, type=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        for i in hint:
            assert i in result.text
        print_json_multi_row(json.loads(result.text))

    # -------------------收到的消息---------------------------
    @allure.title("消息列表")
    @allure.story("收到的消息")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_findNoticeRecipientPage(self, dlogin, login, start, end):
        response1, cook = login
        url = host + portlogin + "/notice/findNoticeRecipientPage.json"
        header = {"cookie": dlogin}
        data = dict(
            page=1, size=15,
            startDate=start, endDate=end, modularType=1,
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, headers=header)

    def transfer_noticeList(self, dlogin, response1, cook):
        header = {"cookie": dlogin}
        url = host + portlogin + "/notice/findNoticeRecipientPage.json"
        data = dict(
            page=1, size=15,
            startDate="", endDate="", modularType=1,
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, headers=header)
        ids = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                recientid12 = i["recientId"]
                title12 = i["noticeTitle"]
                userName12 = i["sendUserName"]
                ids.append((recientid12, title12, userName12))
        return ids

    @allure.title("消息详情")
    @allure.story("收到的消息")
    def test_getNoticeDetailsByNoticeId(self,dlogin, login):
        response1, cook = login
        url = host + portlogin + "/notice/getNoticeDetailsByNoticeId.json"
        dicdata = self.transfer_noticeList(dlogin, response1, cook)
        allure.attach(f"内部参数：dicdata={dicdata}")
        if len(dicdata) > 0:
            data = dict(recientId=dicdata[0][0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, dicdata[0][1])

    @allure.title("医院的医生的列表-医生科室列表")
    @allure.story("我创建的")
    @allure.step("参数：login={0}")
    def test_getOrgInfoTreeList(self, login):
        response1, cook = login
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38", path=400, orgName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("医院的医生的列表-医生列表")
    @allure.story("我创建的")
    @allure.step("参数：login={0}")
    def test_findUserBasePage(self, login):
        response1, cook = login
        url = host + portlogin + "/users/users/findUserBasePage.json"
        data = dict(positionIds=2202,   # 这里是固定的
                    keyword="", path=f"400,{response1['itemOrgId']},", page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def addresseeId(self, response1, cook):
        url = host + portlogin + "/users/users/findUserBasePage.json"
        data = dict(positionIds=2202, keyword="", path=f"400,{response1['itemOrgId']},", page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["orgUserId"])
        return ids

    @allure.title("创建新的消息")
    @allure.story("我创建的")
    @allure.step("参数： login={0}")
    def test_createNotice(self, login):
        response1, cook = login
        url = host + portlogin + "/notice/createNotice.json"
        ids = self.addresseeId(response1, cook)
        allure.attach(f"内部参数：ids={ids}")
        data = {
                'addresseeId': ids[0],
                'title': '新增消息2',
                'noticeTypeId': 1,
                'content': '<p>新增消息2</p>',
                'autoSave': 'false',
                'recipientAll': 0,
                'attachmentURL': [],
                'operatorId': response1["authUserId"],
                'noticeStatus': 2,
                'modularType': 1,
                'operatorFunction': '51058-addMsg',
                'authUserId': response1["authUserId"],
                'authToken': response1["authToken"]}
        assert_post(url, data, cook)

    @allure.title("上传附件")
    @allure.story("我创建的")
    def test_saveFileattachment(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/common/fileattachment/saveFileattachment.json"
        ff = {"file": uploadpath1}
        header = {"cookie": dlogin}
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, files=ff, headers=header, data=data)

    @allure.title("审核记录列表")
    @allure.story("审核记录")
    @allure.step("参数： login={0}")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_findNoticeExaminetPage(self, login, start, end):
        response1, cook = login
        url = host + portlogin + "/notice/findNoticeExaminetPage.json"
        data = dict(
            page=1, size=15,
            startDate=start, endDate=end, modularType=1,
            operatorFuncttest_updateStatusion='51058-viewAuditingRecord', operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_noticelEcaminet(self, response1, cook):
        url = host + portlogin + "/notice/findNoticeExaminetPage.json"
        data = dict(
            page=1, size=15,
            startDate="", endDate="", modularType=1,
            operatorFunction='51058-viewAuditingRecord', operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]['content']
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append((i['noticeId'], i['noticeTitle'], i['createOrgUserId']))
        return ids

    @allure.title("审核")
    @allure.story("审核记录")
    @allure.step("参数：login={0}")
    def test_updateStatus(self, login):
        response1, cook = login
        url = host + portlogin + "/notice/updateStatus.json"
        noticedata = self.transfer_noticelEcaminet(response1, cook)
        allure.attach(f"内部参数：noticedata={noticedata}")
        data = dict(
            auditOrgUserId=noticedata[0][2], noticeId=noticedata[0][0], status=1, auditOpinion="",
            auditAndRepealFlag='auditFlag', repealOpinion="",
            operatorFunction='51058-lookThrough', operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("审核后的项目详情")
    @allure.story("审核记录")
    @allure.step("参数：login={0}")
    def test_getCreateAndExamineByNoticeId(self, login):
        response1, cook = login
        url = host + portlogin + "/notice/getCreateAndExamineByNoticeId.json"
        noticadata = self.transfer_noticelEcaminet(response1, cook)
        allure.attach(f"内部参数：noticadata={noticadata}")
        data = dict(noticeId=noticadata[0][0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)