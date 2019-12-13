# coding=utf-8
from public.overWrite_Assert import *


@allure.feature("临床访视计划")
class Test_clinicalVisits:

    @allure.title("临床访视计划-访视计划列表")
    @allure.story("访视计划")
    def test_getProjectInfoList(self, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/getProjectInfoList.json"
        data = dict(groupFlag="3",  # 固定的？？
                    projectName="", authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_ProjectList(self, response1, cook):
        url = host + portlogin + "/projectDetail/getProjectInfoList.json"
        data = dict(groupFlag="3",  # 固定的？？
                    projectName="", authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data=data, cookies=cook)
        dicData = {"projectId": [], "date": [], "planDefinitionId": []}
        if "SUCCESS" in result.text:
            dataDic1 = json.loads(result.text)["responseData"]["content"]
            if len(dataDic1) > 0:
                for i in dataDic1:
                    if i["STATUS"] == "3":  # 这里的项目的状态是进行中的
                        dicData["projectId"].append(i["PROJECT_ID"])
                        dicData["planDefinitionId"].append(i["PLAN_DEFINITION_ID"])
                        dicData["date"].append(i["PROJECT_DATE"])
        return dicData

    @allure.title("临床访视计划-添加访视计划")
    @allure.story("访视计划")
    @pytest.mark.smoke1
    @pytest.mark.parametrize("pname",("新增访视计划2.0", "新增访视计划2.0@+"))
    def test_saveProject(self, pname, login, dlogin, questionId):
        response1, cook = login
        url = host + portlogin + "/projectDetail/saveProjectInfo.json"
        header = {"cookie": dlogin}
        data = {
            "groupFlag": 3,  # 分组标识？？？
            "businessType": 1,  # 业务类型
            "projectName": pname,           # 项目名称
            "projectId": "",
            "defaultFunction": "MANAGE_PATIENT,CREATE_CRF,CHECK_CRF,MANAGE_PRACTITIONER",
            "followupPlan": '[{"visitOrder":{"start":1,"end":1},"stepCount":1,"stepUnit":{"value":"d","code":"d",'
                            '"display":"天"},"preThreshold":1,"postThreshold":1,"thresholdType":"d",'
                            '"questionnaireId":"%s"}]'%questionId[0],
            "operatorFunction": "54906-submitProjectInfo",  # 操作方法
            "note": "",  # 笔记
            "status": 1,  # 状态
            "operatorId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_post(url, data, headers=header)

    @allure.title("临床访视计划-添加的临床访视计划审核")
    @allure.story("访视计划")
    def test_clinicalVisitsAudit(self, submitVisits):
            dd = submitVisits


    @allure.title("临床访视计划-查询访视计划")
    @allure.story("访视计划")
    def test_PatientList_findProjectDetail(self, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/findProjectDetail.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"][0]
        allure.attach(f"内部参数projectId={projectId}")
        data = {
            "projectId": projectId,  # dicData["projectId"][0] 第一个信息3583471
            "authUserId": response1["authUserId"], "authToken": response1["authToken"]}
        assert_get(url, data, cook, projectId)

    @allure.title("为获取科室患者来源信息列表添加数据")
    @allure.story("参与患者")
    def transfer_OrgList(self, response1, cook):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="33,35,38", path="400,",
                    orgName="", authUserId=response1["authUserId"], authToken=response1["authToken"])
        result, resultdic = assert_get(url, data, cook)
        path222 = []
        path222.append(resultdic["responseData"][0]["children"][0]["path"])
        return path222

    @allure.title("从科室添加患者-获取患者列表")
    @allure.story("参与患者")
    def test_PatientList_save_projectUserList(self, login):
        response1, cook = login
        url = host + port_project + "/project/user/list.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"][0]
        path = self.transfer_OrgList(response1, cook)
        allure.attach(f"内部参数：projectId={projectId}\n path={path}")
        data = dict(dataType=1, path=path,
                    projectId=projectId,  # 从列表中传过来的   ["responseData"]["content"][14]["PROJECT_ID"]
                    # page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证5")


    def transfer_UserList(self,response1, cook):  # 从科室添加患者-获取患者列表
        url = host + port_project + "/project/user/list.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        path = self.transfer_OrgList(response1, cook)[0]
        allure.attach(f"内部参数：projectId={projectId}\n path={path}")
        data = dict(dataType=1, path=path,  # 从前一个传过来的 ["children"][0]["path"]
                    projectId=projectId[0],  # 从列表中传过来的   ["PROJECT_ID"] 7206
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        dictData = {"patientId": [], "orgUserId": [], "taskId": []}
        if len(resultdic) > 0:
            for i in resultdic:
                dictData["patientId"].append(i["PATIENT_ID"])
                dictData["orgUserId"].append(i["ORG_USER_ID"])
                # dictData["taskId"].append(i["taskId"])
        return dictData

    @allure.title("从科室筛选表中选择一条数据 这里添加所有的数据")
    @allure.story("参与患者")
    def test_save_clinicalInstance(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/instance.json"
        dataDic = self.transfer_ProjectList(response1, cook)
        patientId = self.transfer_UserList(response1, cook)["patientId"]
        allure.attach(f"内部参数：dataDic={dataDic}\n patientId={patientId}")
        header = {"cookie": dlogin}
        if len(patientId) > 0:
            for i in range(len(patientId)):
                data = dict(patientId=patientId[i],
                            # 从科室患者列表中传过来的     ["PATIENT_ID"]     只能用一次
                            projectId=dataDic["projectId"][0],
                            # 从菜单列表中传过来的      ["PROJECT_ID"]
                            activated=dataDic["date"][0],  # 从菜单列表传过来的["responseData"]["content"][0]["PROJECT_DATE"]
                            planDefinitionId=dataDic["planDefinitionId"][0],
                            # 从菜单列表传过来的  ["responseData"]["content"][14]["PLAN_DEFINITION_ID"]
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                assert_post(url, data, headers=header, hint=patientId[i])

    @allure.title("从科室筛选表中保存选择的一条数据")
    @allure.story("参与患者")
    def test_save_projectDetail(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/saveProjectUserBatch.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"][0]
        dataList = self.transfer_UserList(response1, cook)
        allure.attach(f"内部参数：projectId={projectId}\n dataList={dataList}")
        header = {"cookie": dlogin}
        if len(dataList["patientId"]) > 0:
            for i in range(len(dataList["orgUserId"])):
                orgUserId = dataList["orgUserId"][i]
                patientId = dataList["patientId"][i]
                data = dict(isPatient=1,  # 是否为病人
                            params='[{"projectId": "%s", '%(projectId)+f'"orgUserId": "{orgUserId}", "patientId": "{patientId}"'+',"positionId": "2202"}]',
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                assert_post(url, data, headers=header)

    @allure.title("从指标筛选表中选择一条数据   这里添加了所有的第一页的患者")
    @allure.story("参与患者")
    def test_save_indexclinicalInstance(self, dlogin, login, resultList):
        response1, cook = login
        url = host + portlogin + "/clinical/instance.json"
        dataDic = self.transfer_ProjectList(response1, cook)
        patientId = resultList["patientId"]
        allure.attach(f"内部参数 datadic= {dataDic}\n patientId = {patientId}")
        header = {"cookie": dlogin}
        for i in range(len(patientId)):
            data = dict(patientId=f"Patient/{patientId[i]}",                         # 从指标患者列表中传过来的          只能用一次
                        projectId=dataDic["projectId"][0],              # 从菜单列表中传过来的
                        activated=dataDic["date"][0],                   # 从菜单列表传过来的
                        planDefinitionId=dataDic["planDefinitionId"][0],
                        # 从菜单列表传过来的  ["responseData"]["content"][14]["PLAN_DEFINITION_ID"]
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers=header, hint=patientId[i])

    @allure.title("从筛选筛选表中保存选择数据")
    @allure.story("参与患者")
    def test_save_indexSaveProjectDetail(self, dlogin, login, resultList):
        response1, cook = login
        url = host + portlogin + "/projectDetail/saveProjectUserBatch.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"][0]
        datadic = resultList
        orgUserId = datadic["orgUserId"]
        patientId = datadic["patientId"]
        patiId = datadic["patiId"]
        header = {"cookie": dlogin}
        paramsdata = []
        for i in range(len(patientId)):
            paramsdata.append({"patientId":f"Patient/{patientId[i]}","projectId":f"{projectId}","orgUserId":f"{orgUserId[i]}","patiId":f"{patiId[i]}","positionId":"2202"})
        paramdatastr = json.dumps(paramsdata)
        allure.attach(f"内部参数：筛选的患者信息={datadic}\n paransdatastr={paramdatastr}")
        data = dict(isPatient=1,  # 是否为病人
                    # params=[{"projectId": "3583471",        #从菜单列表中传过来的      ["PROJECT_ID"]
                    #          "orgUserId": "4530550",         #从患者列表中传过来的     ["ORG_USER_ID"]
                    #          "patientId": "Patient/205521",    #从科室患者列表中传过来的     ["PATIENT_ID"]     只能用一次
                    #          "positionId": "2202"}],            #好像是固定的
                    params=paramdatastr,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, headers=header)

    @allure.title("参与患者信息列表")
    @allure.story("参与患者")
    def test_getProjectPatientLsit(self, login, dlogin):
        response1, cook = login
        url = host + portlogin + "/projectDetail/getProjectPatientList.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        header = {"cookie": dlogin}
        allure.attach(f"内部参数：projectId={projectId}")
        data = dict(
            page=1, size=15,
            projectId=projectId[0],  # 这是从访视计划列表中传值过来的7206
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        # assert_get(url, data, cook)
        assert_get(url, data, headers=header)

    def transfer_PatientList(self, dlogin, response1, cook):
        url = host + portlogin + "/projectDetail/getProjectPatientList.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        allure.attach(f"内部参数：prjectId={projectId}")
        data = dict(
            page=1, size=15,
            projectId=projectId[0],  # 这是从访视计划列表中传值过来的，但是这里给固定的值
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, headers={"cookie": dlogin})
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicData = {"taskId": [], "dummyUserId": [], "carePlanId": [], "patiId": [], "patientId": []}
        if len(resultDic) > 0:
            for i in resultDic:
                if "DUMMY_USER_ID" in i and "carePlanId" in i:
                    dicData["dummyUserId"].append(i["DUMMY_USER_ID"])
                    dicData["carePlanId"].append(i["carePlanId"])
                if "taskId" in i:
                    dicData["taskId"].append(i["taskId"])
                dicData["patiId"].append(i["PATI_ID"])
                dicData["patientId"].append(i["patientId"])
        return dicData

    @allure.title("添加失访记录  这里的数据都添加了访视记录")
    @allure.story("添加失访记录")
    def test_list_appointmentReason(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/appointment/reason.json"
        taskId = self.transfer_PatientList(dlogin, response1, cook)["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        header = {"cookie": dlogin}
        if len(taskId) > 3:
            for i in range(len(taskId)//2):           # 这里有一半的数据添加访视记录
                data = {
                    "taskId": taskId[i],  # 从患者列表信息中来的 ["taskId"]
                    "reason": "|unwillingness",
                    "authUserId": response1["authUserId"],
                    "authToken": response1["authToken"]
                }
                assert_post(url, data, headers=header, hint=taskId[i])
        else:
            for i in range(len(taskId)):           # 这里有一半的数据添加访视记录
                data = {
                    "taskId": taskId[i],  # 从患者列表信息中来的 ["taskId"]
                    "reason": "|unwillingness",
                    "authUserId": self.authUserId,
                    "authToken": self.authToken
                }
                assert_post(url, data, headers=header, hint=taskId[i])

    @allure.title("开始添加CRF记录")
    @allure.story("添加失访记录")
    def test_list_qtStart(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/interview/start.json"
        taskId = self.transfer_PatientList(dlogin, response1, cook)["taskId"]
        allure.attach(f"内部参数：taskid={taskId}")
        header = {"cookie": dlogin}
        for i in range(len(taskId)):        # 这里可以全部的添加记录了
            data = dict(taskId=taskId[i],      # 从患者列表信息中来的 ["responseData"]["content"][0]["taskId"]
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers=header, hint="无效状态")

    def start(self, dlogin, response1, cook):
        url = host + portlogin + "/clinical/interview/resume.json"
        taskId = self.transfer_PatientList(dlogin, response1, cook)["taskId"]
        allure.attach(f"内部参数：taskid={taskId}")
        data = dict(taskId=taskId[0],  # 从患者列表信息中来的 ["responseData"]["content"][0]["taskId"]
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        header = {"cookie": dlogin}
        result = requests.post(url, data, headers=header)
        token = "9709413d-dc38-41a0-818f-a75d9d575c03"
        if "token" in result.text:
            resultstr = json.loads(result.text)["responseData"]["questionnaire"]
            token = json.loads(resultstr)["token"]
        return token

    @allure.title("重新开始添加CRF记录")
    @allure.story("添加失访记录")
    def test_list_qRtesume(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/interview/resume.json"
        taskId = self.transfer_PatientList(dlogin, response1, cook)["taskId"]
        allure.attach(f"内部参数：taskID={taskId}")
        header = {"cookie": dlogin}
        for i in range(len(taskId)):        # 这里可以全部的添加记录了
            data = dict(taskId=taskId[i],      # 从患者列表信息中来的 ["responseData"]["content"][0]["taskId"]
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers=header, hint="无效状态")

    @allure.title("这里是中间值的传递和传参接口")
    @allure.story("添加失访记录")
    def test_giveItem(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/record/item.json"
        token = self.start(dlogin, response1, cook)
        patientId = self.transfer_PatientList(dlogin, response1, cook)["patientId"]
        allure.attach(f"内部参数：token={token}\n patientId={patientId}")
        data = dict(token=token,
                    index=0, isFirst=1,
                    patientId=patientId[0],  # 这里是从start传过来的  ["responseData"]["patientId"]
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def linkId(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/record/item.json"
        token = self.start(dlogin, response1, cook)
        patientId = self.transfer_PatientList(dlogin, response1, cook)["patientId"]
        allure.attach(f"内部参数：token={token}\n patientId={patientId}")
        data = dict(token=token,
                    index=0, isFirst=1,
                    patientId=patientId[0],  # 这里是从start传过来的  ["responseData"]["patientId"]
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, headers={"cookie": dlogin})
        linkId = "09f2f032-760a-4b15-a609-b7caf673aa51"
        if "linkId" in result.text:
            resultStr = json.loads(result.text)["responseData"]["questionnaire"]
            linkId = json.loads(resultStr)["item"][0]["linkId"]
        return linkId

    @allure.title("添加CRF记录")
    @allure.story("添加失访记录")
    def test_list_qtCheck(self, dlogin, login):
        response1, cook = login
        url = host + port_qt + "/qtCheck/check.json"
        patientId = self.transfer_PatientList(dlogin, response1, cook)["patientId"]
        linkId = self.linkId(dlogin, login)
        allure.attach(f"内部参数：patientId={patientId}\n linkId={linkId}")
        if len(patientId) > 3:
            for i in range(int(len(patientId)/2)):    # 这里大概有一半的数据添加CRF记录
                data = {
                    "answerContent": '[{"linkId":"%s","value":["|past"]}]' % linkId,
                    "patientId": patientId[i],  # "	Patient/72068"
                    "questionnaireUrl": "http://gyfyy.com/fhir/Questionnaire/xzwj0011-1571910299116",  # 这里也是从start中传过来的
                    "type": "submit",  # 这里是固定的
                    "authUserId": response1["authUserId"],
                    "authToken": response1["authToken"]
                }
                assert_post(url, data, cook)

    @allure.title("这里是提交CRF记录 这里的一组数据都提交了")
    @allure.story("添加失访记录")
    def test_list_qtSubmit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/interview/submit.json"
        taskId = self.transfer_PatientList(dlogin, response1, cook)["taskId"]
        linkId = self.linkId(dlogin, login)
        allure.attach(f"内部参数：taskID={taskId}\n linkId={linkId}")
        header = {"cookie": dlogin}
        if len(taskId) > 3:
            for i in range(int(len(taskId)/2)):           # 这里大概是有一半的数据提交CRF
                data = dict(taskId=taskId[i],  # 从患者列表信息中来的 ["responseData"]["content"][0]["taskId"]
                            # 这个参数和选取的值是一致的
                            content='[{"linkId":"%s","value":["|past"]}]' % linkId,
                            practitionerId="",
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                assert_post(url, data, headers=header, hint=taskId[i])


    @allure.title("申请终止参与临床访视计划")
    @allure.story("添加失访记录")
    def test_list_endPlanDefinition(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/endPlanDefinition.json"
        dataDict = self.transfer_PatientList(dlogin, response1, cook)
        dummyUserId = dataDict["dummyUserId"]
        carePlanId = dataDict["carePlanId"]
        allure.attach(f"内部参数：datadict={dataDict}\n dummyuserId={dummyUserId}\n carePlanId={carePlanId}")
        if len(dummyUserId) > 3:
            for i in range(int(len(dummyUserId)/2)+1):
                data = {
                    "note": f"委任为1{i}",  # 自己填写的提示信息 这个是非必填项
                    "dummyUserId": dummyUserId[i],  # 从患者信息列表中传过来的 ["DUMMY_USER_ID"]
                    "carePlanId": carePlanId[i],  # 从患者信息列表中传过来的 ["carePlanId"]
                    "authUserId": response1["authUserId"],
                    "authToken": response1["authToken"]
                }
                assert_post(url, data, cook, carePlanId[i])
        else:
            for i in range(len(dummyUserId)):
                data = {
                    "note": f"委任为1{i}",  # 自己填写的提示信息 这个是非必填项
                    "dummyUserId": dummyUserId[i],  # 从患者信息列表中传过来的 ["DUMMY_USER_ID"]
                    "carePlanId": carePlanId[i],  # 从患者信息列表中传过来的 ["carePlanId"]
                    "authUserId": response1["authUserId"],
                    "authToken": response1["authToken"]
                }
                assert_post(url, data, cook, carePlanId[i])

    @allure.title("查看临床访视计划参与患者详情")
    @allure.story("添加失访记录")
    def test_list_findProjectPlanInfo(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/findProjectPlanInfoVo.json"
        dummyUserId = self.transfer_PatientList(dlogin, response1, cook)["dummyUserId"]
        allure.attach(f"内部参数：dummyuserId={dummyUserId}")
        if len(dummyUserId) > 0:
            data = {
                "dummyUserId": dummyUserId[0],  # 从患者列表信息来["responseData"]["content"][2]["DUMMY_USER_ID"]
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_get(url, data, headers={"cookie": dlogin}, hint=dummyUserId[0])

    @allure.title("移除临床访视计划中的参与患者")
    @allure.story("添加失访记录")
    def test_list_deletePlandefinition(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/deletePlanDefinition.json"
        dataDict = self.transfer_PatientList(dlogin, response1, cook)
        dummyUserId = dataDict["dummyUserId"]
        carePlanId = dataDict["carePlanId"]
        allure.attach(f"内部参数：dataDic={dataDict}\n dummyuserId={dummyUserId}\n carePlanId={carePlanId}")
        for i in range(int(len(carePlanId)/2)):
            data = {
                "status": 9,
                "dummyUserId": dummyUserId[i],  # 从患者信息列表中来的数据 ["responseData"]["content"][5]["DUMMY_USER_ID"]
                "carePlanId": carePlanId[i],  # 从患者信息列表中来的数据 ["responseData"]["content"][5]["carePlanId"]
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_post(url, data, cook, carePlanId[i])

    @allure.title("CRF展示列表")
    @allure.story("CRF记录")
    def test_CRFList(self, login):
        response1, cook = login
        url = host + portlogin + "/interview/crflist.json"
        data = dict(
            page=1, pageSize=15,
            # planDefinitionId=planDefinitionId[0],
            # 从临床访视计划中提取 ["responseData"]["content"][14]["PLAN_DEFINITION_ID"]
            orderNo="", taskCode="clinical", viewType="view",  # 固定的
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)
        # overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证  5")

    def transfer_CRFlist(self, response1, cook):  # CRF列表展示
        url = host + portlogin + "/interview/crflist.json"

        data = dict(page=1, pageSize=15,
                    orderNo="", taskCode="clinical", viewType="view",  # 固定的
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicData = {"taskId": [], "responseId": [], "patientId": []}
        if len(resultDic) > 0:
            for i in resultDic:
                dicData["taskId"].append(i["taskId"])
                dicData["patientId"].append(i["patientId"])
                if "qrId" in i.keys():
                    dicData["responseId"].append(i["qrId"])
        return dicData

    @allure.title("CRF审核 修订")
    @allure.story("CRF记录")
    def test_CRFList_amendResume(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/amend/resume.json"
        taskId = self.transfer_CRFlist(response1, cook)["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        data = dict(taskId=taskId[0],
                    authUserId=response1["authUserId"], authToken=response1["authUserId"])
        header = {"cookie": dlogin}
        assert_post(url, data, headers=header, hint=taskId[0])

    # 给中间函数传值
    def giveRecordView(self, response1, cook):  # 给中间传值的函数传值
        url = host + portlogin + "/record/view.json"
        responseId = self.transfer_CRFlist(response1, cook)["responseId"]
        allure.attach(f"内部参数：reponseId={responseId}")
        if len(responseId) > 0:
            data = dict(responseId=responseId[0],  # 从CRF列表中传递过来 ["responseData"]["content"][0]["qrId"]
                        version="",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            result, resultDic = assert_get(url, data, cook)
            tokenDic = json.loads(resultDic["responseData"]["questionnaire"])
            return tokenDic

    # @allure.title("CRF添加批注的中间的传值的函数")
    # @allure.story("CRF记录")
    # @pytest.mark.skip("这里没有数据")
    # def testgiveMoveData(self, dlogin, login):
    #     response1, cook = login
    #     url = host + portlogin + "/record/item.json"
    #     token = self.giveRecordView(response1, cook)
    #     patientId = self.transfer_CRFlist(response1, cook)["patientId"]
    #     data = dict(token=token,  # 从前一个函数中传递过来ee46d495-9091-4083-85ae-bbab4179cd33
    #                 index=0, isFirst=0,
    #                 patientId=patientId[0],  # 从CRF列表之中传值 ["responseData"]["content"][0]["patientId"]
    #                 authUserId=response1["authUserId"], authToken=response1["authToken"])
    #     print(f"\nurl = {url}\ndata= {data}")
    #     assert_get_header(url, data, {"cookie": dlogin})

    @allure.title("CRF审核 点击查看详情（通过后或者待审核）添加批注")
    @allure.story("CRF记录")
    def test_CRFList_recordComment(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/record/comment.json"
        responseId = self.transfer_CRFlist(response1, cook)["responseId"]
        linkId = self.linkId(dlogin, login)
        header = {"cookie": dlogin}
        allure.attach(f"内部参数：responseId={responseId}\n linkId={linkId}")
        for i in range(len(responseId)):
            data = dict(responseId=responseId[i],  # 从CRF列表中传递过来 ["responseData"]["content"][0]["qrId"]
                        content='[{"linkId":"%s","value":["|past"]}]' % linkId,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])  # 这个要问数据的来源
            assert_post(url, data, headers=header)

    @allure.title("CRF记录 提交审核")
    @allure.story("CRF记录")
    def test_CRFList_amendSubmit(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/clinical/amend/submit.json"
        taskId = self.transfer_CRFlist(response1, cook)["taskId"]
        linkId = self.linkId(dlogin, login)
        header = {"cookie": dlogin}
        allure.attach(f"内部参数：taskId={taskId}\n linkId={linkId}")
        for i in range(int(len(taskId)/2)+1):
            data = dict(taskId=taskId[i],
                        content='[{"linkId":"%s","value":["|past"]}]' % linkId,
                        practitionerId="",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, headers=header, hint=taskId[i])

    @allure.title("参与医生 列表展示")
    @allure.story("参与医生")
    def test_projectDetail(self, login):  # 参与医生 列表展示
        response1, cook = login
        url = host + portlogin + "/projectDetail/getProjectPractitionerList.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        allure.attach(f"内部参数：projectId={projectId}")
        data = dict(
            # page=1, size=5,
            projectId=projectId[0],  # 从菜单列表中传过来的      ["responseData"]["content"][14]["PROJECT_ID"]
            authUserId=response1["authUserId"], authToken=response1["authUserId"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证  5")

    @allure.title("给医生设置权限传值")
    @allure.story("参与医生")
    def transfer_orgDoctor(self, response1, cook):
        url = host + portlogin + "/projectDetail/getProjectPractitionerList.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        allure.attach(f"内部参数：projectId={projectId}")
        data = dict(
            page=1, size=15,
            projectId=projectId[0],  # 从菜单列表中传过来的      ["responseData"]["content"][14]["PROJECT_ID"]
            authUserId=response1["authUserId"], authToken=response1["authUserId"])
        result = requests.get(url, data, cookies=cook)
        dicdata = {"defaultFunction": [], "dummyUserId": []}
        if "SUCCESS" in result.text:
            resultDic = json.loads(result.text)["responseData"]["content"]
            for i in resultDic:
                if "DEFAULT_FUNCTION" in i.keys() and "DUMMY_USER_ID" in i.keys():
                    dicdata["dummyUserId"].append(i["DUMMY_USER_ID"])
                    dicdata["defaultFunction"].append(i["DEFAULT_FUNCTION"])
        return dicdata

    @allure.title("获取医生列表")
    @allure.story("参与医生")
    def test_getDoctor(self, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/getProjectPractitionerAddList.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        allure.attach(f"内部参数：projectId={projectId}")
        data = dict(status=1, path=f"400,{response1['orgId']},",  # def testgive(self):  #为获取患者列表添加数据 传值
                    projectId=projectId[0],  # 从菜单列表中传过来的    ["PROJECT_ID"]
                    # page=1, size=5,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证  5")

    def transfer_doctorAddlist(self, response1, cook):  # 用于医生列表传值
        url = host + portlogin + "/projectDetail/getProjectPractitionerAddList.json"
        projectId = self.transfer_ProjectList(response1, cook)["projectId"]
        allure.attach(f"内部参数：projectId={projectId}")
        data = dict(status=1, path=f"400,{response1['orgId']},",  # def testgive(self):  #为获取患者列表添加数据 传值
                    projectId=projectId[0],  # 从菜单列表中传过来的      ["responseData"]["content"][14]["PROJECT_ID"]
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        dicdata = {"orgUserId": [], "positionId": [], "projectId": projectId, }
        if "SUCCESS" in result.text:
            resultDic = json.loads(result.text)["responseData"]["content"]
            if len(resultDic) > 0:
                for i in resultDic:
                    if "ORG_USER_ID" in i:
                        dicdata["orgUserId"].append(i["ORG_USER_ID"])
                        dicdata["positionId"].append(i["ALL_POSITION_ID"])
        return dicdata

    @allure.title("参与医生  添加参与的医生")
    @allure.story("参与医生")
    def test_saveUserBatch(self, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/saveProjectUserBatch.json"
        params1 = self.transfer_doctorAddlist(response1, cook)
        allure.attach(f"内部参数 params={params1}")
        for i in range(len(params1["orgUserId"])):
            data = dict(isPatient=1,
                        # params=[{"projectId":"3583471",
                        #                      "orgUserId":"4379014",   # 从AddList中传递过来的["ORG_USER_ID"]
                        #                      "positionId":"2468,2770,2911"    # 从AddList中传递过来的["ALL_POSITION_ID"]
                        #                      }],
                        params='[{"projectId": "%s", "orgUserId": "%s", "positionId": "%s"}]' % (
                            params1["projectId"][0], params1["orgUserId"][i], params1["positionId"][i]),
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook)

    @allure.title("参与医生  添加参与的医生")
    @allure.story("参与医生")
    def test_saveProjectUser(self, dlogin, login):
        response1, cook = login
        url = host + portlogin + "/projectDetail/saveProjectUser.json"
        dicdata = self.transfer_orgDoctor(response1, cook)
        defaultFunction = dicdata["defaultFunction"]
        dummyUserId = dicdata["dummyUserId"]
        allure.attach(f"内部参数：dicdata={dicdata}\n defaultFunction={defaultFunction}\n dummyuseId={dummyUserId}")
        if len(dummyUserId) > 0:
            data = dict(defaultFunction=defaultFunction[0],  # 从医生列表中传值  ["responseData"]["content"][0]["DEFAULT_FUNCTION"]
                        dummyUserId=dummyUserId[0],  # 从医生的列表中的数据来源 ["responseData"]["content"][0]["DUMMY_USER_ID"]
                        status="",  # 当为9时是移除    不用添加权限
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook, dummyUserId[0])



if __name__ == '__main__':
    pytest.main()