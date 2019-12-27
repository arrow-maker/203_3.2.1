# -*- coding: utf-8 -*-
from public.overWrite_Assert import *


@allure.feature("临床访视计划审核")
class Test_clinicalInterviewAudit:

    # @allure.title("访视计划审核-新增临床访视计划")
    # @allure.story("临床访视计划审核")
    # def test_clinicalVisitsAudit_addNewProject(self, addVisitProject):
    #     pass

    @allure.title("临床访视计划数据展示")
    @allure.story("临床访视计划")
    @pytest.mark.parametrize("check", (1, 2))
    @pytest.mark.parametrize("business", (1, 0))
    def test_show(self, login, check, business):
        allure.title("time")
        response1, cook = login
        url = host + portlogin + "/project/check/list.json"
        data = {
            "dataType": 20,
            "page": 1,
            "size": 15,
            "checkType": check,
            "businessType": business,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    def giveProjectCheckList(self, response1, cook):
        url = host + portlogin + "/project/check/list.json"
        data = {
            "dataType": 20,
            "page": 1,
            "size": 15,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        result_dict = json.loads(result.text)["responseData"]["page"]
        response_dic = {"dataId": [], "checkId": []}
        if len(result_dict["content"]) > 0:
            for i in result_dict["content"]:
                response_dic["dataId"].append(i["DATA_ID"])
                response_dic["checkId"].append(i["ID"])
        return response_dic

    @allure.title("临床访视计划审核")
    @allure.story("临床访视计划")
    def test_viewAudit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/project/check/submit.json"
        dicData = self.giveProjectCheckList(response1, cook)
        allure.attach(f"内部参数：dicdata={dicData}")
        data = dict(dataId=dicData["dataId"][0],
                    checkId=dicData["checkId"][0],
                    result=1,
                    dataType=20,
                    checkOption="",
                    serviceName="projectCheckFollowupService",
                    operatorFunction="54946-submitPlan",
                    operatorId=response1["authUserId"], authUserId=response1["authUserId"],
                    authToken=response1["authToken"])
        header = {"cookie": dlogin}
        assert_post(url, data, headers=header, hint=dicData["dataId"][0])

    @allure.title("查看审核详情")
    @allure.story("临床访视计划")
    def test_viewAuditDetails(self, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/findProjectDetail.json"
        projectId = self.giveProjectCheckList(response1, cook)["dataId"][0]
        data = dict(projectId=projectId,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, projectId)

    @allure.title("CRF展示列表详情")
    @allure.story("CRF审核")
    def test_CRF_crfList(self, login, dlogin):
        response1, cook = login
        url = host + portlogin + "/interview/crflist.json"
        data = dict(
            page=1, pageSize=15,
            viewType="review", taskCode="clinical",
            commitStatus="已提交", orderNo="", isCheck="true",
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, headers={"cookie": dlogin})

    @allure.title("CRF展示列表详情")
    @allure.story("CRF审核")
    def transfer_crfList(self, dlogin, response1, cook):
        url = host + portlogin + "/interview/crflist.json"
        data = dict(page=1, pageSize=15, viewType="review", taskCode="clinical",
                    commitStatus="已提交", orderNo="", isCheck="true",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, headers={"cookie": dlogin})
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicData = {"taskId": [], "patientId": []}
        if "SUCCESS" in result.text:
            if len(resultDic) > 0:
                for i in resultDic:
                    dicData["taskId"].append(i["reviewTaskId"])
                    dicData["patientId"].append(i["patientId"])
        return dicData

    @allure.title("CRF开始审核")
    @allure.story("CRF审核")
    def test_CRF_reviewStart(self,dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/review/start.json"
        taskId = self.transfer_crfList(dlogin, response1, cook)["taskId"]
        if len(taskId) > 0:
            data = dict(taskId=taskId[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers={"cookie": dlogin}, hint=taskId)

    def start123(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/review/start.json"
        taskId = self.transfer_crfList(dlogin, response1, cook)["taskId"]
        token = "6a6ca623-d160-4e41-9eaa-f8246937a8f9"
        allure.attach(f"内部参数：taskId={taskId}\n token={token}")
        if len(taskId) > 0:
            data = dict(taskId=taskId,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            result = requests.post(url, data, {"cookie": dlogin})
            if "token" in result.text:
                resultdic = json.loads(result.text)["responseData"]["questionnaire"]
                token = json.loads(resultdic)["token"]
        return token

    @allure.title("给CRF审核提交传值")
    @allure.story("CRF审核")
    def testtransfer_modelSubmit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/record/item.json"
        patientId = self.transfer_crfList(dlogin, login[0], login[1])["patientId"]
        token = self.start123(dlogin, login)
        allure.attach(f"内部参数：patiendId={patientId}\n token={token}")
        data = dict(token=token,
                    isFirst=0, patientId=patientId[0],
                    index=0,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def linkId123(self, dlogin, login):
        response1, cook = login
        token = self.start123(dlogin, login)
        patientId = self.transfer_crfList(dlogin, login[0], login[1])["patientId"]
        url = host + portlogin + "/record/item.json"
        allure.attach(f"内部参数:token={token}\n patientId={patientId}")
        data = dict(token=token,
                    isFirst=0, patientId=patientId[0],
                    index=0,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        linkId = "685b70ff-26c9-4df0-9c6b-2e8d7124e269"
        result = requests.get(url, data, cookies=cook)
        if "linkId" in result.text:
            resultdic = json.loads(result.text)["responseData"]["questionnaire"]
            linkId = json.loads(resultdic)["linkId"]
        return linkId

    @allure.title("CRF审核保存")
    @allure.story("CRF审核")
    def test_CRF_checkSave(self, dlogin, login):
        response1, cook = login
        url = host + port_project + "/project/check/save.json"
        dataId = self.transfer_crfList(dlogin, response1, cook)["taskId"][0]
        allure.attach(f"内部参数：dataId={dataId}")
        data = dict(serviceName="projectCheckCrfService",
                    dataType=23,
                    operatorId=response1["authUserId"],
                    dataId=dataId,
                    optionType="", result=0,
                    operatorFunction="54826-submitProject",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, dataId)

    @allure.title("CRF审核提交")
    @allure.story("CRF审核")
    def test_CRF_reviewSubmit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/review/submit.json"
        taskId = self.transfer_crfList(dlogin, response1, cook)["taskId"][1]
        linkId = self.linkId123(dlogin, login)
        allure.attach(f"内部参数：taskId={taskId}\n linkId={linkId}")
        data = dict(taskId=taskId,
                    content='[{"linkId":"%s","value":["|never"]}]' % linkId,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, headers={"cookie": dlogin}, hint=taskId)

    @allure.title("CRF审核通过查看结果")
    @allure.story("CRF审核")
    def test_CRF_findCheck(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectPatient/findCheck.json"
        taskId = self.transfer_crfList(dlogin, response1, cook)["taskId"]
        data = dict(taskId=taskId[1],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, taskId[1])

    @allure.title("终止患者访视列表审核通过查看结果")
    @allure.story("终止患者访视")
    def test_UserList(self, login):
        response1, cook = login
        url = host + portlogin + "/project/check/userList.json"
        data = dict(dataType=21,
                    # page=1, size=15,
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证5")

    def transfer_UserList(self, response1, cook):
        url = host + portlogin + "/project/check/userList.json"
        data = dict(dataType=21,  # ??
                    page=1, size=15,
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        dicData = {"dataId": [], "checkId": [], "projectName": []}
        if "SUCCESS" in result.text:
            resultCount = json.loads(result.text)["responseData"]["page"]["content"]
            for i in resultCount:
                dicData["dataId"].append(i["DATA_ID"])
                dicData["checkId"].append(i["ID"])
                dicData["projectName"].append(i["PROJECT_NAME"])
        return dicData

    @allure.title("终止患者访视审核")
    @allure.story("终止患者访视")
    def test_project_checkSubmit(self, login):
        allure.dynamic.title("time-1")
        allure.dynamic.description("")
        response1, cook = login
        url = host + portlogin + "/project/check/submit.json"
        dicData = self.transfer_UserList(response1, cook)
        allure.attach(f"内部参数：dicdata={dicData}")
        data = dict(dataId=dicData["dataId"][0],
                    checkId=dicData["checkId"][0],
                    result=1, dataType=21,
                    checkOption="",
                    serviceName="projectCheckTerminatePatientService",
                    operatorFunction="54946-submitPlan",
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, "无效状态")

    @allure.title("终止患者访视--审核通过查看结果")
    @allure.story("终止患者访视")
    def test_projectDetail_projectPlanInfo(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/findProjectPlanInfoVo.json"
        dataId = self.transfer_UserList(response1, cook)["dataId"][0]
        allure.attach(f"内部参数：dataId={dataId}")
        data = dict(dummyUserId=dataId,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        header = {"cookie": dlogin}
        assert_get(url, data, headers=header, hint=dataId)

    def patiId(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/findProjectPlanInfoVo.json"
        dataId = self.transfer_UserList(response1, cook)["dataId"][0]
        allure.attach(f"内部参数：dataId={dataId}")
        data = dict(dummyUserId=dataId,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        header = {"cookie": dlogin}
        resutl = requests.get(url, data, headers=header)
        patiId = "066513ff-6eb6-43d7-9ea3-d087f4dc04a3"
        if "patiId" in resutl.text:
            resutldic = json.loads(resutl.text)["responseData"]["userInfoVo"]
            patiId = resutldic["patiId"]
        return patiId

    @allure.title("终止患者访视审核 终止计划")
    @allure.story("终止患者访视")
    def test_project_endPlan(self, dlogin, login):
        response1, cook = login
        url = host + port_qt + "/notice/endPlan.json"
        patiId = self.patiId(dlogin, login)
        projectName = self.transfer_UserList(login[0], login[1])["projectName"]
        allure.attach(f"内部参数：patiId={patiId}\n projectName={projectName}")
        data = dict(patiId=patiId,
                    projectName=projectName[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)


if __name__ == '__main__':
    pytest.main()
