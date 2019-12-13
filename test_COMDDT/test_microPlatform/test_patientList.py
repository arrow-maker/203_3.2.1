# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_patientList.py
    Time:    2019/12/2 13:51
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *


@allure.feature("帮助中心管理")
class Test_patientList:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]

    @allure.title("信息状态展示")
    @allure.story("患者数据授权")
    def test_getFunction(self):
        url = host + portlogin + "/app/function/getFunction.json"
        data = {
            "orgUserIdToken": self.authToken,
            "orgUserId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("数据列表展示")
    @allure.story("预填答卷")
    def test_findAnswerPage(self):
        url = host + port_qt + "/qtAnswer/findAnswerPage.json"
        data = {
            "editStatus": 1,
            "page": 1,
            "size": 10,
            "referType": "",
            "qtInfoId": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("问卷标题选择-筛选用的标题")
    @allure.story("预填答卷")
    def test_findFhirQsList(self):
        url = host + port_qt + "/qtInfo/findFhirQsList"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("科研项目列表")
    @allure.story("随访患者信息")
    @pytest.mark.parametrize("groupFlag", ("", 3))
    def test_findProjectPage(self, groupFlag):
        url = host + port_mobile + "/project/findProjectPage"
        data = {
            "groupFlag": groupFlag,
            "page": 1, "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    def projectId(self):
        url = host + port_mobile + "/project/findProjectPage"
        data = {
            "groupFlag": 3,
            "page": 1, "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        ids = []
        for i in result[1]["responseData"]["content"]:
            ids.append(i["projectId"])
        return ids

    @allure.title("项目或计划的详细信息")
    @allure.story("随访患者信息")
    @pytest.mark.parametrize("code", ("sms_inform_invited", "medicine_remind_sms"))
    def test_getValue(self, code):
        url = host + portlogin + "/param/getValue.json"
        data = dict(code=code,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("信息详情-密码修改设置")
    @allure.story("随访患者信息")
    def test_findPatientPageByInterview(self):
        url = host + portlogin + "/param/getParamByCode.json"
        data = dict(codes="initial_password",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "初始密码")

    @allure.title("列表信息详情")
    @allure.story("随访患者信息")
    def test_findPatientPageByInterview(self):
        url = host + port_mobile + "/project/findPatientPageByInterview.json"
        projectId = self.projectId()
        allure.attach(f"内部参数：projectId={projectId}")
        data = {
            "projectId": projectId[0],
            "searchWord": "",
            "page": 1,
            "size": 10,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    def orgUserId(self):
        url = host + port_mobile + "/project/findPatientPageByInterview.json"
        projectId = self.projectId()
        allure.attach(f"内部参数：projectId={projectId}")
        data = {
            "projectId": projectId[0],
            "searchWord": "",
            "page": 1,
            "size": 10,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        for i in resultdic:
            ids.append(i["orgUserId"])
        return ids

    @allure.title("患者关系绑定")
    @allure.story("随访患者信息")
    def test_findMyBind(self):
        url = host + port_mobile + "/relatives/findMyBind"
        ids = self.orgUserId()
        allure.attach(f"传值参数：ids={ids}")
        if len(ids) > 0:
            data = dict(orgUserId=ids[0],  # 4348409
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_get(url, data, self.cook)

    @allure.title("重置患者密码")
    @allure.story("随访患者信息")
    def test_resetDefaultPasswd(self):
        url = host + port_mobile + "/patient/resetDefaultPasswd.json"
        ids = self.orgUserId()
        allure.attach(f"传值参数：ids={ids}")
        if len(ids) > 0:
            data = dict(orgUserId=ids[0],  # 4316920
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_post(url, data, self.cook)

    def answerPatientId(self):
        url = host + port_qt + "/qtAnswer/findAnswerPage.json"
        data = {
            "editStatus": 1,
            "page": 1,
            "size": 10,
            "referType": "",
            "qtInfoId": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result, resultdic = assert_get(url, data, self.cook)
        ids = {"qtId": [], "answerPatientId": []}
        for i in resultdic["responseData"]["content"]:
            ids["qtId"].append(i["qtId"])
            ids["answerPatientId"].append(i["answerPatientId"])
        return ids

    @allure.title("查看问卷详情")
    @allure.story("预填问卷")
    def test_findSection(self):
        url = host + port_qt + "/qtSection/findSection.json"
        ids = self.answerPatientId()
        qtId = ids["qtId"]
        answerPatientId = ids["answerPatientId"]
        allure.attach(f"传值参数：ids={ids}\nqtId={qtId}\nanswerPatientId={answerPatientId}")    # 1000005   10192
        if len(answerPatientId) > 0:
            data = dict(appUse=1, qtId=qtId[0], isShow=1, answerPatientId=answerPatientId[0],
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_get(url, data, self.cook)

    @allure.title("查看问卷详情")
    @allure.story("预填问卷")
    def test_findItemBySection(self):
        url = host + port_qt + "/qtSection/findItemBySection.json"
        ids = self.answerPatientId()
        qtId = ids["qtId"]
        answerPatientId = ids["answerPatientId"]
        allure.attach(f"传值参数：ids={ids}\nqtId={qtId}\nanswerPatientId={answerPatientId}")
        if len(answerPatientId) > 0:
            data = dict(sectionId=qtId[0], answerPatientId=answerPatientId[0], isShow=1,
                        appUse=1, page=1, size=1000,
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_get(url, data, self.cook)

    @allure.title("保存患者数据权限")
    @allure.story("患者数据权限")
    def test_saveEnable(self):
        url = host + portlogin + "/app/function/saveEnable.json"
        data = dict(orgUserIdToken=self.authToken, orgUserId=self.authUserId,
                    enableParam='{"1":1,"2":1,"3":1,"4":1,"5":1,"6":1,"7":1}',
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("修改患者数据权限")
    @allure.story("患者数据权限")
    def test_changeEnable(self):
        url = host + portlogin + "/app/function/changeEnable.json"
        data = dict(orgUserIdToken=self.authToken, orgUserId=self.authUserId,
                    id=8, enable=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("通知受邀患者和用药通知")
    @allure.story("患者数据权限")
    @pytest.mark.parametrize("code", ("sms_inform_invited", "medicine_remind_sms"))
    @pytest.mark.parametrize("value", (1, 0))
    def test_changeEnable(self, code, value):
        url = host + portlogin + "/param/updateParam.json"
        data = dict(paramType="environment", code=code, value=value,
                    operatorFunction="51042-saveScienceSetting", operatorId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)
