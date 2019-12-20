# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_C0_patientList.py
    Time:    2019/12/19 14:37
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *


@allure.feature("科研项目管理->患者列表")
class Test_patientList:

    @classmethod
    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.title("证件类型")
    @allure.story("患者总库")
    def test_getCodeItemList(self):
        url = host + portlogin + "/code/codeItem/getCodeItemList.json"
        data = dict(code="DOCUMENT_TYPE",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("疾病类型")
    @allure.story("患者总库")
    def test_getDiseaseList(self):
        url = host + port_dataindex + "/patient/getDiseaseList.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("医院的数据")
    @allure.story("患者总库")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="33,35,38",
                    path=400, orgName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("患者列表数据")
    @allure.story("患者总库")
    def test_patientSearch(self):
        """
        下面的患者的病例操作是全景，有单独的全景的模块，这里就不赘述
        :return:
        """
        url = host + port_dataindex + "/patient/search.json"
        data = dict(page=1, size=10, orgPath="400,75722,75726,", orgType=35,
                    orgId=75726, searchWord="", sourceType=2, sourceRecord=1,
                    indexTimeBegin="", indexTimeEnd="", visitDateBegin="",
                    visitDateEnd="", followUpDateBegin="", followUpDateEnd="",
                    diseaseType=1, diseaseName="", sourceDataType="",
                    neSourceDataType=3, panoramicSearch="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("患者列表数据-患者的基本的信息")
    @allure.story("患者总库")
    def test_identifierGetOne(self):
        url = host + port_primaryIndex + "/identifier/getOne.json"
        data = dict(uniquNo="YS00010cf961bb-4d26-4ddb-8dd6-992e96d44655", hospitalCode="YS0001",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("删除患者列表数据")
    @allure.story("患者总库")
    def test_projectUserList(self):
        url = host + portlogin + "/projectUser/interview/user/list.json"
        data = dict(orgUserId=4399776,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("新增患者")
    @allure.story("患者总库")
    def test_createPatient(self, dlogin):
        url = host + portlogin + "/projectUser/createPatient.json"
        header = {"cookie": dlogin}
        param = {"authUserId": self.authUserId, "authToken": self.authToken}
        data = {
            "address": "广州天河区",
            "birthDate": "1999-02-13",
            "identitycard": 412721199902132619,
            "contactUserPhone": "",
            "direct": "true",
            "sex": 1,
            "inpatientNumber": "",
            "username": "华仔",
            "outpatientNumber": "",
            "telecom": 15517889640,
            "certificateType": 1,
            "maritalStatus": 2,
            "birthAddress": "",
            "contactUserName": ""
        }
        assert_post(url, data, headers=header, params=param)

    @allure.title("下载患者列表")
    @allure.story("患者总库")
    def test_downloadData(self):
        url = host + portlogin + "/excel/downloadData.json"
        data = dict(beanName="patientExcelService", fileName="excel", path="excel/exportPatientInfo.xlsx",
                    ids="YS00010cf961bb-4d26-4ddb-8dd6-992e96d44655,YS0001abc2b4c6-9228-4690-bc8e-9c104fe64d82,YS0001ead77fe0-6710-4f49-91c4-701a8e3ffea1,YS0001fab84d23-d3a1-481d-adda-05193d4028be,YS000188c8e070-70b1-4d55-8851-f29d509a2b2b,YS0001b5e94aa1-5a8e-430a-b1fc-9008cbaccc06,YS0001f95db489-254d-46ab-8a1c-4a5eb2d4d814,YS0001ef3b33e0-06fc-4d6c-8822-08bf6a712427,YS0001024efe5f-a7b8-43a1-8828-55a0e9f96484,YS0001ebdc81a6-6856-4a29-9444-8e226263f534",
                    operatorFunction="54886-exportPatient", operatorId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        assert "workbook" in result.text


if __name__ == '__main__':
    pytest.main()