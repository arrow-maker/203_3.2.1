# -*- coding: utf-8 -*-
from public.overWrite_Assert import *
from public.auditProject import auditProjectList,submitProject



@allure.feature("科研项目管理->科研审核")
class Test_project_audict:

    @allure.title("我的项目->项目申请 ->提交到审核-用于审核")
    @allure.story("项目审核")
    def test_AudictProject_addProject(self, login, questionId):
        submitProject(login, questionId)

    @allure.title("项目管理->科研审核->项目申请 项目展示")
    @allure.story("项目审核")
    def test_Apply(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/list.json"
        data = {
            # "checkType":2,                                         #审核状态，1：待审核，2：审核已通过，3：审核不通过
            # "projectCenter":"",                                     #研究中心，1：单中心，2：多中心
            # "projectName":"",                                      #用于查询项目的名称的字段
            # "page":  1,
            # "size":10,
            "operatorId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "科研审核-项目申请-数据展示")

    @allure.title("科研项目-项目审核-通过（所有的审核都是这个接口）")
    @allure.story("项目审核")
    def test_projectReview(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/save.json"
        listtemp = auditProjectList(cook, response1["authUserId"], response1["authToken"])  # 待审核的列表
        allure.attach(f"内部参数：listtemp={listtemp}")
        data = {
            "operatorId": response1["authUserId"],  # 操作人员
            "dataId": listtemp["DATA_ID"][0],  # 3573263 数据只能使用一次
            "result": 1,  # 检查类型
            "checkOption": "",  # 审核意见
            "serviceName": "projectCheckFollowupService",   # 服务名称 固定的
            "checkId": listtemp["ID"][0],  # 检查ID
            "dataType": 10,
            "operatorFunction": "54826-submitProject",  # 操作方法
            "authUserId ": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("项目审核通过基本详情")
    @allure.story("项目审核")
    def test_list_projectCheckBaseInfo(self, login):
        response1, cook = login
        url = host + port_project + "/project/info/base.json"
        tempdict = auditProjectList(cook, response1["authUserId"], response1["authToken"])  # 这里是项目列表
        allure.attach(f"内部参数：tempdic={tempdict}")
        data = dict(projectId=tempdict["DATA_ID"][1],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("项目审核通过基本详情")
    @allure.story("项目审核")
    def test_list_projectCheckLastInfo(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/lastInfo.json"
        listdict = auditProjectList(cook, response1["authUserId"], response1["authToken"])
        allure.attach(f"内部参数：listdict={listdict}")
        data = dict(dataType=10, operatorId=response1["authUserId"],
                    dataId=listdict["DATA_ID"][1],  # DATA_ID
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("项目管理->科研审核->知情同意书")
    @allure.story("知情同意书")
    def test_InformedConsent(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/file/list.json"
        data = {
            "operatorId": response1["authUserId"],
            # "patientName":"",#名字存在还有不存在
            # "projectName":"",#名字存在还有不存在
            # "checkType":"", #待审核：2，审核通过：1，审核不通过：0，全部时：空
            # "page":1,
            # "size":10,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "科研审核-知情同意书列表")

    '''
    下面的所有的审核的详情是一致的，这里就统一的说明一下。
    这里的审核通过的审核详情和项目申请的审核详情一致，项目详情和项目申请通过的是一致的，这里就不另外添加了
    '''
    # @allure.title("项目管理->科研审核->不良事件-列表展示")
    # @allure.title("这里的不良事件和项目管理中的不良事件是一样的")
    # @allure.story("不良事件")
    # @pytest.mark.skip("太影响i性能")
    # def test_AdverseEevent(self, login):
    #     response1, cook = login
    #     url = host + port_project + "/project/event/findGroupList.json"
    #     data = {
    #         "keyword": "",
    #         # "projectName":"",#项目名称
    #         # "category":"",  #SAE:1,AE:2
    #         # "status":"",    #待审核：2，通过考核：1，不通过：0
    #         # "patientName":"",#受试者姓名
    #         # "reportName":"",#报告名称
    #         # "page": 1,
    #         # "size":10,
    #         "isEventList": "true",
    #         "operatorId": response1["authUserId"],
    #         "authUserId": response1["authUserId"],
    #         "authToken": response1["authToken"]
    #     }
    #     overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "科研审核-不良事件列表")

    @allure.title("项目管理->科研审核->受试者终止")
    @allure.story("受试者终止")
    def test_SubjecSstop(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/patient/list.json"
        data = {
            # "keyName":"受试者姓名",
            # "projectName":"项目名称",
            # "checkType": 1,#待审核：1，审核通过：2，审核不通过：3
            "operatorId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "科研审核-受试者终止列表")

    @allure.title("科研审核-CRF审核-可选项目列表")
    @allure.story("科研质控-CRF审核")
    def test_auditResearch_function(self, login):
        response1, cook = login
        url = host + port_project + "/project/functionList.json"
        data = dict(keyName="ALL_CENTER_CHECK_CRF,CHECK_CRF",
                    operatorId=response1["authUserId"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def functionList(self,response1, cook):
        url = host + port_project + "/project/functionList.json"
        data = dict(keyName="ALL_CENTER_CHECK_CRF,CHECK_CRF",
                    operatorId=response1["authUserId"], authUserId=response1["authUserId"],
                    authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        for i in resultdic:
            ids.append(i["PROJECT_ID"])
        return ids


    @allure.title("项目管理->科研审核->CRF分组信息")
    @allure.story("CRF")
    def test_CRFGroup(self, login):
        response1, cook = login
        url = host + port_project + "/project/report/group.json"
        ids = self.functionList(response1, cook)
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "projectId": ids[0],
            "createUserId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    @allure.title("项目管理->科研审核->CRF默认团队信息")
    @allure.story("CRF")
    def test_CRFOrgInfoTree(self, login):
        response1, cook = login
        url = host + port_project + "/project/user/orgInfo/tree.json"
        ids = self.functionList(response1, cook)
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "projectId": ids[0],
            "hasGroup": 2,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    @allure.title("项目管理->科研审核->CRF默认团队信息")
    @allure.story("CRF")
    def test_CRFlist(self, login):
        response1, cook = login
        url = host + portlogin + "/interview/crflist.json"
        ids = self.functionList(response1, cook)
        allure.attach(f"内部参数：ids={ids}")
        data = dict(taskCode="project", page=1, commitStatus="已提交", viewType="review",
                    pageSize=10, projectId=ids[0], operatorId=response1["authUserId"], dept="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("这里是获取CRF列表，用于审核传参")
    @allure.story("CRF")
    def giveCRFList(self, response1, cook):
        url = host + portlogin + "/interview/crflist.json"
        ids = self.functionList(response1, cook)
        allure.attach(f"内部参数：ids={ids}")
        data = dict(taskCode="project", page=1, commitStatus="已提交", viewType="review",
                    pageSize=10, projectId=ids[0], operatorId=response1["authUserId"], dept="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        datalist = {"taskId": [], "patientId": []}
        if len(resultdic) > 0:
            for i in resultdic:
                datalist["taskId"].append(i["reviewTaskId"])
                datalist["patientId"].append(i["patientId"])
        return datalist

    @allure.title("审核 导入FHIR")
    @allure.story("CRF")
    def test_importFhirtaskBypatient(self, login):
        response1, cook = login
        url = host + portlogin + "/newDataImport/importFHIRTaskByPatients.json"
        patientId = self.giveCRFList(response1, cook)["patientId"]
        allure.attach(f"内部参数：patientId={patientId}")
        if len(patientId) > 0:
            data = dict(patientIds=patientId[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, patientId[0])

    @allure.title("获取患者的详细的信息")
    @allure.story("CRF")
    def test_patientInfoFHIR(self, login):
        response1, cook = login
        url = host + portlogin + "/projectPatient/getPatientInfo.json"
        patientId = self.giveCRFList(response1, cook)["patientId"]
        allure.attach(f"内部参数：patientId={patientId}")
        if len(patientId) > 0:
            data = dict(patientId=patientId[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, patientId[0])

    @allure.title("审核 CRF项目审核 开始提交")
    @allure.story("CRF")
    def test_list_projectCRFreviewStart(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/project/review/start.json"
        taskId = self.giveCRFList(response1, cook)["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        if len(taskId) > 0:
            header = {"cookie": dlogin}
            data = dict(taskId=taskId,  # 这个只能使用一遍
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers=header, hint=taskId[0])

    @allure.title("审核 CRF项目重新开始")
    @allure.story("CRF")
    def test_list_projectCRFreviewResume(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/project/review/resume.json"
        taskId = self.giveCRFList(response1, cook)["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        if len(taskId) > 0:
            data = dict(taskId=taskId[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers={"cookie": dlogin}, hint=taskId)

    @allure.title("审核 CRF项目审核  保存")
    @allure.story("CRF")
    def test_list_projectCRFreviewsave(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/save.json"
        taskId = self.giveCRFList(response1, cook)["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        if len(taskId) > 0:
            data = dict(serviceName="projectCheckCrfService",
                        dataType=14,
                        operatorId=response1["authUserId"], dataId=taskId[0],
                        optionType="logicality-check,standard-check,repeatability-check,process-check,integrality-check",
                        result=1, operatorFunction="54826-submitProject",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook, taskId[0])

    def transfer_Start(self, dlogin, response1, cook):  # 传递开始的值
        url = host + portlogin + "/project/review/start.json"
        taskId = self.giveCRFList(response1, cook)["taskId"]
        allure.attach(f"内部参数：taskid={taskId}")
        if len(taskId) > 0:
            header = {"cookie": dlogin}
            data = dict(taskId=taskId[0],  # 这个只能使用一遍
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            result, resultDic = assert_post(url, data, headers=header)
            if "SUCCESS" in resultDic:
                token1 = json.loads(resultDic["responseData"]["questionnaire"])["token"]
                token2 = json.loads(resultDic["responseData"]["review"])["token"]
                return token1, token2
            else:
                return "5a7d069d-b12b-4e84-b781-816a66900bc6", "0"

    @allure.title("获取提交中要用到的linkId，和url")
    @allure.story("CRF")
    def test_list_projectCRFRecordItem(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/record/item.json"
        token = self.transfer_Start(dlogin, response1, cook)
        patientData = self.giveCRFList(response1, cook)["patientId"]
        allure.attach(f"内部参数：token={token}\n patinetId={patientData}")
        if token is not None:
            data = dict(token=token[0],  # 这里从开始或者从新开始传递过来的["questionnaire"]
                        isFirst=0,
                        patientId=patientData[0],  # 这里是从CRF列表中传过来的["patientId"]
                        index=0,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook)

    @allure.title("审核 CRF项目审核 提交")
    @allure.story("CRF")
    def test_list_projectCRFreviewSubmit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/project/review/submit.json"
        taskId = self.giveCRFList(response1, cook)["taskId"]
        header = {"cookie": dlogin}
        allure.attach(f"内部参数：taskId={taskId}")
        if len(taskId) > 0:
            data = dict(taskId=taskId[0],
                        # 下面的参数是固定的
                        content='[{"linkId":"1bbfbbc6-ebec-4d1c-8e41-a4f485f9f9b8",'
                                '"value":["http://gyfyy.com/fhir/inspection-mode|logicality-check",'
                                '"http://gyfyy.com/fhir/inspection-mode|standard-check",'
                                '"http://gyfyy.com/fhir/inspection-mode|process-check",'
                                '"http://gyfyy.com/fhir/inspection-mode|integrality-check",'
                                '"http://gyfyy.com/fhir/inspection-mode|repeatability-check"]},'
                                '{"linkId":"349d3bde-40e5-4fd7-99d1-e8882bcca2de","value":["|1"]}]',
                        authUserId=response1["authUserId"], authToken=response1["authToken"])

            assert_post(url, data, headers=header)

    @allure.title("项目管理->科研审核->项目汇报")
    @allure.story("项目汇报")
    def test_ProjectReportList(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/report/list.json"
        data = {
            "operatorId": response1["authUserId"],
            # "page":1,
            # "size":10,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证")

    @allure.title("项目管理->科研审核->项目汇报")
    @allure.story("项目汇报")
    def transfer_ProjectReportList(self, response1, cook):
        url = host + port_project + "/project/check/report/list.json"
        data = {
            "operatorId": response1["authUserId"],
            "page":1,
            "size":10,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = assert_get(url, data, cook)
        resultDic = result[1]["responseData"]["content"]
        dicdata={"checkId": [], "projectId": []}
        for i in resultDic:
            dicdata["checkId"].append(i["CHECK_ID"])
            dicdata["projectId"].append(i["PROJECT_ID"])
        return dicdata

    @allure.title("项目汇报审核提交")
    @allure.story("项目汇报")
    def test_ProjectReportSave(self, login):
        response1, cook = login
        url = host + port_project + "/project/check/save.json"
        tempdict = self.transfer_ProjectReportList(response1, cook)
        allure.attach(f"内部参数：tempdict={tempdict}")
        if len(tempdict["checkId"]) > 0:
            data = dict(checkId=tempdict["checkId"][0],  # 从项目列表中传值过来["CHECK_ID"]6271
                        result=1, checkOption="",
                        serviceName="projectCheckReportService",  # 项目报告中固定的格式
                        projectId=tempdict["projectId"][0],  # 从项目列表中传值过来["PROJECT_ID"]3583118
                        operatorId=response1["authUserId"], operatorFunction="54826-submitProject",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook, "已审核")
