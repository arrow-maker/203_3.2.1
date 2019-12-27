# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_discussionOfClinical.py
    Time:    2019/11/28 14:25
    Author:  Arrow
"""
from public.overWrite_Assert import *
replyId = []       # 讨论的Id
"""
这个模块要使用两个账号登录：记得你要有两个账号
    一个用于审核，一个是创建者
"""
@allure.feature("病例讨论")
class Test_dicussion():

    @allure.title("添加讨论列表数据")
    @allure.story("病例讨论-列表")
    def test_sectionsave(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/section/save.json"
        data = dict(serviceName="discussGroupService", sectionName="新增3.0版本",
                    sectionContent="个个都是", sectionTemplate=20, createdUserId=response["authUserId"],
                    updatedUserId=response["authUserId"], remark="",
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result, resultdic = assert_post(url, data, cook)
        assert "新增3.0版本" in result
        global sectionId
        sectionId = resultdic["responseData"]["sectionId"]
        global dataId
        dataId = resultdic["responseData"]["sectionId"]

    @allure.title("讨论列表数据")
    @allure.story("病例讨论-列表")
    @allure.step("参数：login={0}")
    def test_sectionList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/section/list.json"
        data = dict(serviceName="discussGroupService", timeStamp=time_up,
                    sectionName="", updatedUserId=response["authUserId"], page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook)

    def patientSearch(self, response, cook):
        url = host + port_bbs + "/bbs/patient/search.json"
        data = dict(searchWord="", sectionId=sectionId, page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result, resultdic = assert_get(url, data, cook)
        ids = []
        for i in resultdic["responseData"]["content"]:
            ids.append(i["patiId"])
        return ids

    @allure.title("添加患者")
    @allure.story("病例讨论-患者")
    @allure.step("参数：login={0}")
    def test_topicSave(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        patiId = self.patientSearch(response, cook)
        patiIds = ""
        for i in patiId:
            patiIds += f"{i},"
        allure.attach(f"内部参数：patiId={patiId}")
        data = dict(submitType=1, topicId="", serviceName="discussCaseService",
                    sectionId=sectionId, patiIds=patiIds, createdUserId=response["authUserId"],
                    updatedUserId=response["authUserId"],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook, patiIds)

    @allure.title("添加病例")
    @allure.story("病例讨论-患者")
    def test_topicSave2(self, login, resultList):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        patiId = resultList["patiId"]
        patiIds = ""
        for i in patiId:
            patiIds += f"{i},"
        allure.attach(f"内部参数：patiId={patiId}")
        data = dict(submitType=1, topicId="", serviceName="discussCaseService",
                    sectionId=sectionId, patiIds=patiIds, createdUserId=response["authUserId"],
                    updatedUserId=response["authUserId"],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook, patiIds)

    @allure.title("病例讨论中的患者列表")
    @allure.story("病例讨论-患者")
    @allure.step("参数：login={0}")
    def test_topicList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up, auditType=1, keyword="",
                    sectionId=sectionId, updatedUserId=response["authUserId"], page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook)

    def topicList(self, response, cook):
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up, auditType=1, keyword="",
                    sectionId=sectionId, updatedUserId=response["authUserId"], page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["bbsTopic"]["content"]
        ids = []
        for i in resultdic:
            ids.append(i["TOPIC_ID"])
        return ids

    @allure.title("添加用于审核组员-组员信息列表")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login={0}")
    def test_getUserList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/user/getUserList.json"
        data = dict(keyword="arrow3", size=10, sectionId=sectionId,
                    operatorId=response["authUserId"], page=1,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook, "arrow3")

    def userList(self, response, cook):
        url = host + port_bbs + "/bbs/user/getUserList.json"
        data = dict(keyword="arrow3", size=10, sectionId=sectionId,
                    operatorId=response["authUserId"], page=1,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        for i in resultdic:
            ids.append(i["ORG_USER_ID"])
        return ids

    @allure.title("添加用于审核组员-保存组员信息列表")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login={0}")
    def test_sectionMemberSave(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/section/member/save.json"
        userList = self.userList(response, cook)
        data = dict(serviceName="discussGroupService", sectionId=sectionId,
                    memberInfos='[{"memberOrgUserId":"%s","memberRoleType":3}]' % userList[0],
                    updatedUserId=response["authUserId"], authUserId=response["authUserId"],
                    authToken=response["authToken"])
        assert_post(url, data, cook, str(sectionId))

    @allure.title("添加用于审核组员-组员信息列表")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login={0}")
    def test_sectionMemberList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/section/member/list.json"
        data = dict(serviceName="discussGroupService", timeStamp=time_up, sectionId=sectionId,
                    updatedUserId=response["authUserId"], page=1, size=999999,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook, str(sectionId))

    def memberList(self, response, cook):
        url = host + port_bbs + "/bbs/section/member/list.json"
        data = dict(serviceName="discussGroupService", timeStamp=time_up, sectionId=sectionId,
                    updatedUserId=response["authUserId"], page=1, size=999999,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        for i in resultdic:
            if i["USER_NAME"] == "arrow3":
                ids.append(i["MEMBER_ID"])
        return ids

    @allure.title("添加用于审核组员-修改组员的职能为审核人")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login={0}")
    def test_sectionMemberupdate(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/section/member/update.json"
        memberId = self.memberList(response, cook)
        allure.attach(f"内部参数：memberId={memberId}")
        data = dict(serviceName="discussGroupService", sectionId=sectionId, memberId=memberId[0],
                    memberRoleType=2,updatedUserId=response["authUserId"],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook, str(sectionId))

    @allure.title("开始审核-查看患者详情(用于开始审核)")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login={0}")
    def test_topicInfo(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/info.json"
        topicId = self.topicList(response, cook)
        allure.attach(f"内部参数：topicId={topicId}")
        data = dict(serviceName="discussCaseService", topicId=topicId[0],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook, str(topicId[0]))

    @allure.title("开始审核-整理并提审-用于审核")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login={0}")
    def test_topicsave3(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList(response, cook)
        allure.attach(f"内部参数：topicId={topicId}")
        for i in range(5):          # 有五个用于审核提交
            data = {
                "serviceName": "discussCaseService",
                "submitType": 4,
                "updatedUserId": response["authUserId"],
                "topicId": topicId[i],
                "discussingItem": "[]",
                "conclusion": "勇敢的风格-审核提交",
                "auditType": 3,
                "authUserId": response["authUserId"],
                "authToken": response["authToken"]
            }
            assert_post(url, data, cook, "勇敢的风格-审核提交")

    """
        下面的是另一个的用户登录的：注意 
                要注意判断，可以用来审核的数据的--标记
    """
    @allure.title("审核-待审核列表数据")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login2={0}")
    def test_topicList2(self, login2):
        response, cook = login2
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up,
                    auditType=3, keyword="", sectionId=sectionId, updatedUserId=response["authUserId"],
                    page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook, str(sectionId))

    def topicList_toCheck(self, response, cook):
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up, auditType=3, keyword="",
                    sectionId=sectionId, updatedUserId=response["authUserId"], page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["bbsTopic"]["content"]
        ids = []
        for i in resultdic:
            ids.append(i["TOPIC_ID"])
        return ids

    @allure.title("审核-查看患者详情(用于审核)")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login2={0}")
    def test_topicInfo2(self, login2):
        response, cook = login2
        url = host + port_bbs + "/bbs/topic/info.json"
        topicId = self.topicList_toCheck(response, cook)
        allure.attach(f"内部参数：topicId={topicId}")
        data = dict(serviceName="discussCaseService", topicId=topicId[0],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook, str(topicId[0]))

    @allure.title("审核-整理并提审-通过")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login2={0}")
    def test_topicsave4(self, login2):
        response, cook = login2
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList_toCheck(response, cook)
        allure.attach(f"内部参数：topicId={topicId}")
        data = {
            "serviceName": "discussCaseService",
            "submitType": 4,
            "updatedUserId": response["authUserId"],
            "topicId": topicId[0],
            "checkOption": "勇敢的风格",
            "auditType": 4,
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        assert_post(url, data, cook, "勇敢的风格")

    @allure.title("审核-整理并提审-添加讨论意见")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login2={0}")
    def test_topicsave5(self, login2):
        response, cook = login2
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList_toCheck(response, cook)
        allure.attach(f"内部参数：topicId={topicId}")
        data = dict(serviceName="discussCaseService", submitType=4, updatedUserId=response["authUserId"],
                    topicId=909, discussingItem='[{"orgUserId":"%s","content":"整理谈论结论，发表意见","seq":1}]'
                                                % response["authUserId"],
                    conclusion="添加讨论意见终结", auditType=3,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook, "添加讨论意见终结")

    @allure.title("审核-整理并提审-不通过")
    @allure.story("病例讨论-审核")
    @allure.step("参数：login2={0}")
    def test_topicsave6(self, login2):
        response, cook = login2
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList_toCheck(response, cook)
        allure.attach(f"内部参数：topicId={topicId}")
        data = {
            "serviceName": "discussCaseService",
            "submitType": 4,
            "updatedUserId": response["authUserId"],
            "topicId": topicId[0],
            "checkOption": "勇敢的风格-不通过",
            "auditType": 5,
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        assert_post(url, data, cook, "勇敢的风格-不通过")

    @allure.title("病例讨论中通过审核的患者列表")
    @allure.story("病例讨论-患者")
    @allure.step("参数：login={0}")
    def test_checkpass_topicList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up, auditType=4, keyword="",
                    sectionId=sectionId, updatedUserId=response["authUserId"], page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result, resultdic = assert_get(url, data, cook)
        assert resultdic["responseData"]["bbsTopic"]["totalElements"] == 1

    @allure.title("病例讨论中没有通过审核的患者列表")
    @allure.story("病例讨论-患者")
    @allure.step("参数：login={0}")
    def test_checkNopass_topicList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up, auditType=5, keyword="",
                    sectionId=sectionId, updatedUserId=response["authUserId"], page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result, resultdic = assert_get(url, data, cook)
        assert resultdic["responseData"]["bbsTopic"]["totalElements"] == 1

    """
        这里的是对患者列表的操作：查看详情、编辑信息
    """
    @allure.title("讨论列表查看")
    @allure.story("数据操作-查看详情")
    @allure.step("参数：login={0}")
    def test_intelligentfindList(self, login):
        response, cook = login
        url = host + port_resource + "/analysis/intelligent/findList.json"
        topicId = self.topicList(response, cook)
        data = dict(topicId=topicId[0],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook)

    @allure.title("患者列表中的讨论状态")
    @allure.story("数据操作-讨论管理")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("audittype", (2, 1))
    def test_bbstopicsave(self, login, audittype):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        data = {
            "serviceName": "discussCaseService",
            "submitType": 4,
            "topicId": dataId,
            "auditType": audittype,
            "updatedUserId": response["authUserId"],
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        assert_post(url, data, cook, response["authToken"])

    @allure.title("详情中添加关键字")
    @allure.story("数据操作-查看详情")
    @allure.step("参数：login={0}")
    def test_topicSave7(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList(response, cook)
        data = dict(submitType=2, serviceName="discussCaseService",
                    updatedUserId=response["authUserId"], topicId=topicId[0], tags="新增关键字1",
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook)

    @allure.title("关键字删除")
    @allure.story("数据操作-查看详情")
    @allure.step("参数：login={0}")
    def test_topicSave8(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList(response, cook)
        data = dict(submitType=2, serviceName="discussCaseService",
                    updatedUserId=response["authUserId"], topicId=topicId[0], tags="",
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook)

    @allure.title("添加讨论意见")
    @allure.story("数据操作-查看详情")
    @allure.step("参数：login={0}")
    def test_replysave(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/reply/save.json"
        data = dict(replyContent="<p>表示没有见过患者，不发表意见</p><p><br></p>",
                    topicId=909, createdUserId=response["authUserId"], sectionId=185,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook)

    @allure.title("详情中的讨论意见列表")
    @allure.story("数据操作-查看详情")
    @allure.step("参数：login={0}")
    def test_replygetList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/reply/getList.json"
        data = dict(openSign="true", sectionId=185, topicId=909, page=1, size=20,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = assert_get(url, data, cook)
        assert timelocal in result[0]                   # 断言-创建的日期是当日
        assert response["userName"] in result[0]        # 断言-创建者是作者本人
        global replyId
        for i in result[1]["responseData"]["content"]:
            replyId.append(i["replyId"])

    @allure.title("讨论意见的回复")
    @allure.story("数据操作-查看详情")
    @allure.step("参数：login={0}")
    def test_replysave1(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/reply/save.json"
        data = dict(replyId=replyId[0], replyContent="没意见", topicId=909,
                    createdUserId=response["authUserId"], sectionId=185,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者的就诊信息")
    @allure.story("数据操作-编辑信息")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getAdmissionMrInfoList(self, login, start, end):
        response, cook = login
        url = host + port_es + "/data/getAdmissionMrInfoList.json"
        data = dict(id="YS00014530b85d-99d2-4824-b288-7690b9b2d3c6",
                    startDate=start, endDate=end,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook)

    @allure.title("保存编辑的信息")
    @allure.story("数据操作-编辑信息保存")
    @allure.step("参数：login={0}")
    def test_topicSave9(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        topicId = self.topicList(response, cook)
        data = dict(submitType=3, topicId=topicId[0], serviceName="discussCaseService",
                    patientExamineVo='{"inspect":[],"checkout":[]}',
                    updatedUserId=response["authUserId"], deathTime="Invalid date", inpatientNo="ZY020000582379",
                    visitDate="2018-05-20", orgName=response["orgName"], mainDiagnose="1、急性间质性肺炎",
                    discussAddress="宣武医院", hospitalName="演示医院1",hospitalCode=response["hospitalCode"],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook)

    @allure.title("审核通过/未通过列表展示")
    @allure.story("审核")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("audittype", (4, 5))
    def test_topicList4(self, login, audittype):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/list.json"
        data = dict(serviceName="discussCaseService", timeStamp=time_up,
                    auditType=audittype, keyword="", sectionId=sectionId,
                    updatedUserId=response["authUserId"],
                    page=1, size=10,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_get(url, data, cook)

    @allure.title("审核通过导出病例报告")
    @allure.story("审核")
    @allure.step("参数：login={0}")
    def test_topicreportdownload(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/report/download"
        data = dict(topicId=dataId,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = requests.get(url, data, cookies=cook)
        assert result.status_code == 200

    @allure.title("审核未通过的转套讨论中")
    @allure.story("审核")
    @allure.step("参数：login={0}")
    def test_topicsave10(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/topic/save.json"
        data = dict(serviceName="discussCaseService", submitType=4,
                    updatedUserId=response["authUserId"], topicId=dataId, auditType=1,
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook)

    @allure.title("上传文件")
    @allure.story("组共享")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("filepath",(uploadpath1, uploadpath2, uploadpath3))
    def test_fileSave(self, login, filepath):
        response, cook = login
        url = host + port_bbs + "/bbs/file/save.json"
        file = {"file": open(filepath, "rb")}
        data = {
            "originalFileName": "生成图片.png",
            "operatorId": response["authUserId"],
            "dataId": dataId,
            "dataType": 1
        }
        assert_post(url, data, cook=cook, files=file, hint="生成图片")

    @allure.title("上传文件列表")
    @allure.story("组共享")
    @allure.step("参数：login={0}")
    def test_fileList(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/file/list.json"
        data = {
            "page": 1,
            "size": 10,
            "operatorId": response["authUserId"],
            "displayName": "",
            "dataId": dataId,
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        result = assert_get(url, data, cook, "生成图片")
        assert timelocal in result[0]
        assert response["userName"] in result[0]
        assert '"STATUS":"1"' in result[0]

    def fileId(self, response, cook):
        url = host + port_bbs + "/bbs/file/list.json"
        data = {
            "page": 1,
            "size": 10,
            "operatorId": response["authUserId"],
            "displayName": "",
            "dataId": dataId,
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        result, resultdic = assert_get(url, data, cook)
        ids = []
        for i in resultdic["responseData"]["content"]:
            ids.append(i["FILE_ID"])
        return ids

    @allure.title("上传文件审核")
    @allure.story("组共享")
    @allure.step("参数：login={0}")
    def test_fileUpdataStatus(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/file/updateStatus.json"
        fileId = self.fileId(response, cook)
        allure.attach(f"内部参数：fileId={fileId}")
        data = {
            "fileId": fileId[0],
            "status": 2,
            "operatorId": response["authUserId"],
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("上传文件审核不通过")
    @allure.story("组共享")
    @allure.step("参数：login={0}")
    def test_fileUpdataStatus2(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/file/updateStatus.json"
        fileId = self.fileId(response, cook)
        allure.attach(f"内部参数：fileId={fileId}")
        data = {
            "fileId": fileId[1],
            "status": 3,
            "operatorId": response["authUserId"],
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("上传文件多个下载")
    @allure.story("组共享")
    @allure.step("参数：login={0}")
    def test_downloadBbsFileBatch(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/file/downloadBbsFileBatch.json"
        fileId = self.fileId(response, cook)
        allure.attach(f"内部参数：fileId={fileId}")
        data = dict(fileIds=fileId[0],
                    operatorId=response["authUserId"],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        result = requests.get(url, data, cookies=cook)
        assert result.status_code == 200

    @allure.title("上传文件删除")
    @allure.story("组共享")
    @allure.step("参数：login={0}")
    def test_fileUpdataStatus2(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/file/delete.json"
        fileId = self.fileId(response, cook)
        allure.attach(f"内部参数：fileId={fileId}")
        data = {
            "fileId": fileId[2],
            "operatorId": response["authUserId"],
            "authUserId": response["authUserId"],
            "authToken": response["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("删除讨论列表")
    @allure.story("病例讨论-列表")
    @allure.step("参数：login={0}")
    @pytest.mark.repeat(5)
    def test_sectiondelete(self, login):
        response, cook = login
        url = host + port_bbs + "/bbs/section/delete.json"
        data = dict(serviceName="discussGroupService", sectionId=sectionId,
                    updatedUserId=response["authUserId"],
                    authUserId=response["authUserId"], authToken=response["authToken"])
        assert_post(url, data, cook, str(sectionId))


if __name__ == '__main__':
    pytest.main()