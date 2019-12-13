# -*- coding: utf-8 -*-
from public.overWrite_Assert import *


@allure.feature("即时访视")
class Test_instantInterview:

    @allure.title("即时访视 访视记录 数据展示")
    @allure.story("访视记录")
    def test_list(self, login, dlogin):
        response1, cook = login
        url = host + portlogin + '/instant/list.json'
        data = dict(query='{"filter":{"group":[],"op":"AND"}}',
                    count=15, index=0, authUserId=response1["authUserId"], authToken=response1["authToken"])
        header = {"cookie": dlogin}
        assert_get(url, data, headers=header)

    @allure.title("记录数据的Id")
    @allure.story("访视记录")
    def transfer_list(self, dlogin, response1, cook):
        url = host + portlogin + '/instant/list.json'
        data = dict(query='{"filter":{"group":[],"op":"AND"}}',
                    count=15, index=0, authUserId=response1["authUserId"], authToken=response1["authToken"])
        header = {"cookie": dlogin}
        result = requests.get(url, data, headers=header)
        dicData = {"patientId": [], "taskId": []}  # 这里是给修改使用的patientId
        if "SUCCESS" in result.text:
            resultDic = json.loads(result.text)["responseData"]["content"]
            for i in resultDic:
                if i["intvStatus"] == "saved":  # 获取保存过的CRF问卷
                    dataInt = i["patientId"]
                    aa = re.findall(r"\d+", dataInt)  # 提取dataInt中的数字
                    dicData["patientId"].append(aa[0])
                    dicData["taskId"].append(i["taskIntvId"])
        return dicData

    @allure.title("医院机构")
    @allure.story("访视记录")
    def transfer_OrgInfoTreeList(self, response1, cook):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2,
                    status=1,
                    orgTypeIds="35,38,33",  # 这个好像在哪里遇到过
                    path=400,  # 医院的广医固定的
                    orgName="",
                    authUserId=response1["authUserId"],
                    authToken=response1["authToken"])
        result, resultDic = assert_get(url, data, cook)
        return resultDic

    @allure.title("添加患者的信息列表")
    @allure.story("访视记录")
    def transfer_ProjectAddlist(self, response1, cook):
        url = host + portlogin + "/projectDetail/getProjectPatientAddList.json"
        path = self.transfer_OrgInfoTreeList(response1, cook)["responseData"][0]["children"][0]["path"]
        allure.attach(f"内部参数：path={path}")
        data = dict(path=path,  # 从前一个接口中传递过来的["responseData"][0]["children"][0]["path"]
                    page=10, size=10,  # 第10页的数据
                    authUserId=response1["authUserId"],
                    authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        dicData = {"patientId": [], }
        if "SUCCESS" in result.text:
            resultDic = json.loads(result.text)["responseData"]["content"]
            if len(resultDic) > 0:
                for i in resultDic:
                    dicData["patientId"].append(i["PATIENT_ID"])
        return dicData

    @allure.title("即时访视 新增患者")
    @allure.story("访视记录")
    def test_interviewStart(self, login, dlogin):
        response1, cook = login
        url = host + portlogin + '/instant/interview/start.json'
        questionnaireId = self.transfer_questionList(response1, cook)["questionnaireId"]
        patientId = self.transfer_ProjectAddlist(response1, cook)["patientId"]
        allure.attach(f"内部参数question={questionnaireId}\n patientId={patientId}")
        for i in range(int(len(patientId)/2)+1):
            data = dict(questionnaireId=questionnaireId[0],  # 这里是从问卷列表展示中的数据["id"]
                        patientId=patientId[0],  # 这里是从添加患者信息中提炼的["PATIENT_ID"]
                        operatorFunction="54926-addInstantPaln",  # 这里是固定的数据
                        operatorId=response1["authUserId"],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            header = {"cookie": dlogin}
            assert_post(url, data, headers=header)

    @allure.title("即时访视 患者信息 继续访视 基本信息")
    @allure.story("访视记录")
    def test_instantList(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + '/projectPatient/getPatientInfo.json'
        patientId = self.transfer_list(dlogin, response1, cook)["patientId"]
        allure.attach(f"内部参数：patientId={patientId}")
        data = dict(patientId=patientId[0],  # 280301,
                    # operatorId=4709832,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, patientId[0])

    @allure.title("保存添加患者是添加的CRF访视记录")
    @allure.story("访视记录")
    def test_importFHIRTaskByPatients(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/newDataImport/importFHIRTaskByPatients.json"
        patientIds = self.transfer_list(dlogin, response1, cook)["patientId"][0]
        allure.attach(f"内部参数：patientIds={patientIds}")
        data = dict(patientIds=patientIds,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("即时访视配置 问卷列表")
    @allure.story("即时访视配置")
    def test_questionnaireList(self, login):
        response1, cook = login
        url = host + portlogin + "/plan/questionnaire/list.json"
        data = dict(query='{"filter":{"field":"useContext","op":"LIKE","data":["task","instant"]}}',
                    count=200,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("问卷列表传值")
    @allure.story("即时访视配置")
    def transfer_questionList(self, response1, cook):
        url = host + portlogin + "/plan/questionnaire/list.json"
        data = dict(query='{"filter":{"field":"useContext","op":"LIKE","data":["task","instant"]}}',
                    count=200,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        dicData = {"questionnaireId": []}
        result = requests.get(url, data, cookies=cook)
        if "SUCCESS" in result.text:
            resultDic = json.loads(result.text)["responseData"]["content"]
            for i in resultDic:
                if "id" in i:
                    dicData["questionnaireId"].append(i["id"])
        return dicData

    @allure.title("问卷修改")
    @allure.story("即时访视配置")
    def test_questionnaireresume(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/instant/interview/resume.json"
        taskId = self.transfer_list(dlogin, response1, cook)["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        data = {
            "taskId": taskId[0],  # 从访视记录中的展示列表中传值过来
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        header = {"cookie": dlogin}
        assert_post(url, data, headers=header, hint=taskId[0])

    @allure.title("即时访视配置 问卷停用或者启用")
    @allure.story("即时访视配置")
    def test_questionnaireToggle(self, login):
        response1, cook = login
        url = host + portlogin + "/record/questionnaire/toggle.json"
        questionnaireId = self.transfer_questionList(response1, cook)["questionnaireId"]
        allure.attach(f"内部参数：questionnaireId={questionnaireId}")
        data = dict(questionnaireId=questionnaireId[0],  # 从列表中传递过来["responseData"]["content"][2]["id"]
                    operatorFunction="54926-addStart",  # 这里是固定的格式 启用：54926-addStart，停用：54926-addStop
                    enabled="true",  # 这里是固定的格式false：停用，true：启用
                    operatorId=response1["authUserId"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, questionnaireId[0])

    @allure.title(" 给下一个接口传值")
    @allure.story("即时访视配置")
    def transfer_FhirQsList(self, response1, cook):
        url = host + port_qt+ "/qtInfo/findFhirQsList.json"
        data = dict(page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultDic = json.loads(result.text)
        tranferV = resultDic["responseData"][0]["resourceId"]
        return tranferV

    @allure.title("添加问卷")
    @allure.story("即时访视配置")
    def test_questionnaireInstant(self, login):
        response1, cook = login
        url = host + portlogin + "/record/questionnaire/instant.json"
        transferV = self.transfer_FhirQsList(response1, cook)
        allure.attach(f"内部参数：transferV={transferV}")
        data = dict(questionnaireId=f"Questionnaire/{transferV}",
                    operatorFunction="54926-addInstant",  # 这里是固定的
                    operatorId=response1["authUserId"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, transferV)


if __name__ == '__main__':
    pytest.main()