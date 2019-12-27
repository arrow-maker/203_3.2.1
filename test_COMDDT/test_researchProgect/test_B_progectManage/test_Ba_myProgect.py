from public.Login_Cookies import *
from public.overWrite_Assert import *
from public.auditProject import auditCheckSave as aduit1



@allure.feature("科研项目管理->项目管理类")
class Test_projectManage:
    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]  # 用户姓名
        self.orgId = response["responseData"]["roleList"][0]["orgId"]
        self.hospital = response["responseData"]["platformList"][0]["platformName"]  # 获取医院的名字
        self.mobile = response["responseData"]["mobileTelephone"]
        self.itemOrgId = response["responseData"]["itemOrgId"]

    @allure.title("项目管理->我的项目")
    @allure.story("我加入的")
    def test_list(self):
        url = host + port_project + "/project/list.json"
        data = {
            # "ProjectName":"",
            # "projectCenter":"",
            # "projectStatus":"",  #10：待提交,1:待审核，7：审核不通过，11：启动中，3进行中，8：已终止，5：已结束
            # "page":1,
            # "size":15,
            "operatorId": self.authUserId,
            # "projectUserStatus":1,
            # "joinType": "1",          #1：我加入的，2：邀请我的，3：其他公开的
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, data, self.cook, researchCatePath, "我的项目-项目数据")

    @allure.title("项目管理->我的项目2")
    @allure.story("我加入的")
    @pytest.mark.parametrize("status", (1, 2, 3, 4, 5, 7, 8, 9, 10, 11))
    @pytest.mark.parametrize("joinpath", (1, 2, 3))
    def test_list2(self, status, joinpath):
        """
        :param status:  10：待提交,1:待审核，7：审核不通过，11：启动中，3进行中，8：已终止，5：已结束
        :param joinpath:  1：我加入的，2：邀请我的，3：其他公开的
        :return:
        """
        url = host + port_project + "/project/list.json"
        data = {
            "ProjectName":"",
            "projectCenter":"",
            "projectStatus":"",
            "page":1,
            "size":15,
            "operatorId": self.authUserId,
            "projectUserStatus":1,
            "joinType": "1",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)
    @allure.title("我的项目->申请项目->（字典数据）中的下拉菜单")
    @allure.story("我加入的")
    def test_apply_for_project(self):
        url = host + port_project + "/project/config/itemCodeList.json"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "队列性研究")

    @allure.title("我的项目->申请项目->学科下来单")
    @allure.story("我加入的")
    def test_apply_forSubject(self):
        url = host + port_resource + "/disease/getListByUser.json"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "慢阻肺")

    @allure.title("项目审核 提交一")
    @allure.story("我加入的")
    def test_apply_save(self):
        url = host + port_project + "/project/save.json"
        data = {
            # "projectName": "0123456",  # *项目名称xls
            # "projectNameEn": "adfs",  # 项目英文名xls
            # "solutionCode": "1111",  # 方案编号xls
            # "planStartDateStr": "2019-07-09",  # *项目的开始时间xls
            # "planEndDateStr": "2019-08-21",  # *项目的结束时间xls

            # "projectOrganizer": "甲方1",  # 申办方xls
            # "researchDesign": "研究设计@",  # 研究设计xls
            # "projectObjective": "0123456789",  # **研究主要目的xls
            # "projectObjectiveSecond": "研究次要目的",  # 研究次要目的xls
            # "projectObjectiveOther": "研究其他目的",  # 研究其他目的xls

            # "projectCenter": "1",  # *研究中心1：单中心2:多中心xls
            # "diseaseIds": "110",  # *学科分类的id
            # "centerCode": "01234567890123456789",  # *中心编号xls
            # "organizerPhone": "15599999555",  # 申办方电话xls
            # "synergyType": 3,  # *协同方式1：不公开，2：公开仅可见，3：协同参与
            # "projectUserInMult": 1,  # 多元的
            # "isStartUpPeriod": 1,  # *允许选择入组时间

            # "followupLostHandling": "",  # 最大失访数
            # "followupLostNumber": "",
            # "projectUserElutionTime": "",  # 受试者洗脱期限xls
            # "deadlineType": 1,  # 1:天，2：周，3：月xls
            # "needAgreement": 1,  # 受试者同时参与其他项目,1:同意，2：不同意xls

            "disciplineTypeId": "123",
            "projectTypeId": 2,
            "operatorId": self.authUserId,
            "projectId": "",  # 项目   3583081      没有找到xls
            "orgId": self.orgId,  # 登录的orgID
            "newDrugClinicalStudyNo": "",
            "clinicalStudyTypeCode": "",
            "studyDrugNameZn": "",
            "studyDrugNameEn": "",
            "studyDrugTypeCode": "",
            "studyDrugTypeValue": "",
            "studyDrugRegisterTypeCode": "",
            "studyDrugDosageFormCode": "",
            "clinicalIndications": "",
            "randomGroupType": 0,
            "grouptimeFlag": 1,
            "unblinding": "",
            "randomPart": "",
            "randomLength": "",
            "projectContact": self.userName,
            "projectContactId": self.authUserId,
            "projectContactUnitId": self.orgId,
            "projectContactMobile": self.mobile,
            "projectContactUnit": self.hospital,
            "entryRequire": "",
            "projectUserInType": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "我的项目-项目申请-基本信息保存")  # 这里添加的判断的情况比较少 需要注意

    @allure.title("这里是获取保存项目的id")
    @allure.story("我加入的")
    def get_projectId(self, stutasList):
        url = host + port_project + "/project/list.json"
        data = {
            "ProjectName": "",
            "projectCenter": "",
            "projectStatus": stutasList[0],  # 10：待提交,1:待审核，7：审核不通过，11：启动中，3进行中，8：已终止，5：已结束
            "page": 1,
            "size": 15,
            "operatorId": self.authUserId,
            "projectUserStatus": 1,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result, resultData = assert_get(url, data, self.cook)
        dataDict = {"projectId": [], "dataId": []}
        if int(resultData["responseData"]["numberOfElements"] > 0):
            for i in resultData["responseData"]["content"]:
                dataDict["projectId"].append(i["PROJECT_ID"])
                dataDict["dataId"].append(i["PROJECT_USER_DATA_R_ID"])
        return dataDict

    @allure.title("申请项目保存基础信息-用于修改项目信息")
    @allure.story("我加入的")
    def test_apply_save_base(self):
        url = host + port_project + "/project/info/base.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, dataDict["projectId"][0])

    @allure.title("我的项目->申请项目：筛选期")
    @allure.story("我加入的")
    def test_apply_save_screen(self,questionId):
        url = host + port_project + "/project/info/start-up-period/save.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "operatorId": self.authUserId,
            # "unInGroupDeadline":22,
            # "deadlineType":1,
            "followupPlan":'[{"visitOrder":{"start":1,"end":2},"stepCount":2,"stepUnit":{"value":"d","code":"d",'
                            '"display":"天"},"preThreshold":1,"postThreshold":4,"thresholdType":"d",'
                            '"questionnaireId":"%s"}]'%questionId[0],
            # '[{"visitOrder":{"start":1,"end":1},"stepCount":1,"stepUnit":{"value":"d","code":"d","display":"天"},
            # "preThreshold":1,"postThreshold":1,"thresholdType":"d","questionnaireId":"Questionnaire/117087"}]'
            # "startUpPeriodRule":1,
            # "startUpPeriodDesc":123456789,
            # "startUpPeriodPart":0,
            # "startUpPeriodLength":"",
            # "startUpPeriodPrefix":"",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "我的项目-项目申请-筛选期保存")

    @allure.title("我的项目->申请项目：受试者分组  保存数据")
    @allure.story("我加入的")
    def test_apply_save_groups(self, questionId):
        url = host + port_project + "/project/info/project-group/save.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "operatorId": self.authUserId,
            # "projectName":"试验组1",
            # "projectDesc":'{"inCriteria": "纳入标准", "outCriteria": "排除标准"}',
            # "centerCode":"0011",
            "projectCount": 0,
            "allowScaleOver": 0,
            "followupPlan": '[{"visitOrder":{"start":1,"end":2},"stepCount":2,"stepUnit":{"value":"d","code":"d",'
                            '"display":"天"},"preThreshold":1,"postThreshold":3,"thresholdType":"d",'
                            '"questionnaireId":"%s"}]'%questionId[0],
            "dataIds": dataDict["dataId"][0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "我的项目-申请项目-受试者分组保存数据")

    @allure.title("申请项目：分中心 数据展示")
    @allure.story("我加入的")
    def test_apply__save_groupsList(self):
        url = host + port_project + "/project/info/minute-center/list.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            # "centerProjectName": "",
            "operatorId": self.authUserId,
            # "page": 1,
            # "size": 10,
            "projectStatus": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, data, self.cook, researchCatePath, "我的项目-未提交-分中心数据列表")

    @allure.title("获取医院的orgId 用于添加分中心")
    @allure.story("我加入的")
    def get_userHospitalList(self):
        url = host + port_project + "/project/user/hospital/list.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = dict(projectId=dataDict["projectId"][0],
                    authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        aa = json.loads(result.text)["responseData"]
        OrgId = {"orgId": [], "name": []}
        if len(aa) > 0:
            for i in aa:
                OrgId["orgId"].append(i["orgId"])
                OrgId["name"].append(i["name"])
        return OrgId

    @allure.title("获取这个医院的医生的id 用于添加分中心")
    @allure.story("我加入的")
    def getPricipalUsersList(self):
        url = host + portlogin + "/projectUser/getUsersList.json"
        data = dict(
            path=f"400,{self.get_userHospitalList()['orgId'][1]}",
            keyword="", page=1, size=9999, status=1,
            authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        aa = json.loads(result.text)["responseData"]["content"]
        dictPrici = {"USERNAME": [], "ORG_USER_ID": [], "orgId": []}
        if len(aa) > 0:
            for i in aa:
                dictPrici["USERNAME"].append(i["USERNAME"])
                dictPrici["ORG_USER_ID"].append(i["ORG_USER_ID"])
                dictPrici["orgId"].append(i["ORG_ID"])
        return dictPrici

    @allure.title("我的项目->申请项目：分中心 修改上浮数")
    @allure.story("我加入的")
    def test_apply__save_groupsUpdate(self):
        url = host + port_project + "/project/info/minute-center/allowScaleOver/update.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "allowScaleOver": 20,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("我的项目->申请项目：分中心 添加分中心")
    @allure.story("我加入的")
    def test_apply_save_centerChange(self):
        url = host + port_project + "/project/info/minute-center/save.json"
        dataDict = self.get_projectId(["10"])
        userdata = self.getPricipalUsersList()
        allure.attach(f"项目Id={dataDict['projectId']}\n医生data={userdata}")
        data = {
            "projectId": dataDict["projectId"][0],
            "orgId": userdata["orgId"][0],
            "projectName": "清远人民医院",
            "operatorId": self.authUserId,
            "principalUserId": userdata["ORG_USER_ID"][0],
            "principalUserName": userdata["USERNAME"][0],
            "planStartDateStr": timelocal,
            "projectGroupsData": '[{"projectCount":"555","groupProjectId":7397}]',
            "centerCode": 5435,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("我的项目->申请项目：共享文件列表 上传文件")
    @allure.story("我加入的")
    def test_apply__share_uploading(self):
        try:
            url = host + port_project + "/project/file/save.json"
            dataDict = self.get_projectId(["10"])
            allure.attach(f"项目Id={dataDict['projectId']}")
            file = {"file": r"C:\Users\TP-GZ-A02-050\Desktop\数据库表关系.png"}
            # file = open(r"C:\Users\TP-GZ-A02-050\Desktop\数据库表关系.png","rb")
            data = {
                "file": "(binary)",
                "dataId": dataDict["projectId"][0],
                "dataType": 210,
                "operatorId": self.authUserId,
                "projectId": dataDict["projectId"][0],
                "shareType": 1,
                "orgId": self.orgId,
                "displayName": "analysis_result.csv"
            }
            assert_post(url, data, self.cook, files=file)
        except Exception as e:
            print("---", e)
            raise e

    @allure.title("我的项目->申请项目：共享文件列表")
    @allure.story("我加入的")
    def test_apply__share_list(self):
        url = host + port_project + "/project/file/list.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            # "shareType": 0,  # 0:全部，1：本人，2:仅中心，3：仅项目
            # "page": 1,
            "projectId": dataDict["projectId"][0],
            "operatorId": self.authUserId,
            # "size": 10,
            # "status": 10,  # 我的状态
            "orgId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, data, self.cook, researchCatePath, "我的项目-未提交-共享文件-展示数据")

    @allure.title("未提交的共享文件")
    @allure.story("我加入的")
    def givesharefileList(self):
        url = host + port_project + "/project/file/list.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        if len(dataDict["projectId"]) > 0:
            data = {
                "shareType": 0,
                "page": 1,
                "projectId": dataDict["projectId"][0],
                "operatorId": self.authUserId,
                "size": 10,
                "status": 1,
                "orgId": self.authUserId,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            result = requests.get(url, data, cookies=self.cook)
            aa = json.loads(result.text)["responseData"]["content"]
            if len(aa) > 0:
                return aa[0]["FILE_ID"]
        else:
            return 0

    @allure.title("我的项目 申请项目 提交")
    @allure.story("我加入的")
    def test_apply_handProgect(self):
        url = host + port_project + "/project/submit.json"
        dataDict = self.get_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "operatorId": self.authUserId,
            "operatorFunction": "54806-submitProject",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("审核特定人员的项目")
    @allure.story("项目进行审核")
    def test_Showlist(self):
        aduit1(self.userName, self.cook, self.authUserId, self.authToken)

    def get_delect_projectId(self, stutasList):
        url = host + port_project + "/project/list.json"
        data = {
            "ProjectName": "",
            "projectCenter": "",
            "projectStatus": stutasList[0],
            "page": 1,
            "size": 20,
            "operatorId": self.authUserId,
            "projectUserStatus": 1,
            "joinType": "1",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        actualResult = requests.get(url, data, cookies=self.cook)
        dataDict = {"projectId": [], "dataId": []}
        resultData = json.loads(actualResult.text)
        if int(resultData["responseData"]["numberOfElements"] > 0):
            for i in resultData["responseData"]["content"]:
                if i["PROJECT_OBJECTIVE_SECOND"] == "研究次要目的":
                    dataDict["projectId"].append(i["PROJECT_ID"])  # 这里添加的是给定的状态
                    dataDict["dataId"].append(i["PROJECT_USER_DATA_R_ID"])
        return dataDict

    # @allure.title("我的项目->申请项目：受试者分组 保存后删除")
    # @allure.story("我加入的")
    # @pytest.mark.skip("这里没有受试者分组")
    # def test_apply_save_groups_add(self):
    #     url = host + port_project + "/project/info/project-group/delete.json"
    #     dataDict = self.get_projectId(["3"])
    #     print(f'审核前的操作-受试者分组删除\n{dataDict["projectId"]}')
    #     if len(dataDict["projectId"]) > 0:
    #         data = {
    #             "projectId": dataDict["projectId"][0],  # 项目的id
    #             "operatorId": self.authUserId,  # 我的id
    #             "dataIds": dataDict["dataId"],  # 项目数据的id？
    #             "authUserId": self.authUserId,
    #             "authToken": self.authToken
    #         }
    #         print(f"\nurl={url},\ndata={data}")
    #         assert_post(url, data, self.cook)

    @allure.title("我的项目->申请项目：共享文件 删除")
    @allure.story("我加入的")
    def test_apply__share_uploadingFileDelect(self):
        url = host + port_project + "/project/file/delete.json"
        fileId = self.givesharefileList()
        data = {
            "fileId": fileId,
            "operatorId": self.authUserId,
            "status": 9,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("我的项目：我加入的 项目删除")
    @allure.story("我加入的")
    @pytest.mark.repeat(2)
    def test_list_delect(self):
        url = host + port_project + "/project/delete.json"
        dataDict = self.get_delect_projectId(["10"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        if dataDict["projectId"] is not None:
            for i in range(len(dataDict["projectId"])):  # 删除这一页造的数据
                data = {
                    "projectId": dataDict["projectId"][i],
                    "operatorId": self.authUserId,
                    "operatorFunction": "54806-deleteProject",
                    "authUserId": self.authUserId,
                    "authToken": self.authToken
                }
                assert_post(url, data, self.cook)

    @allure.title("修改后来启动项目--开启项目的状态")
    @allure.story("项目审核后的操作")
    def test_startStatus(self):
        url = host + port_project + "/project/info/status/update.json"
        dataDict = self.get_projectId(["11"])  # 待启动 的项目
        allure.attach(f"项目Id={dataDict['projectId']}")
        if len(dataDict["projectId"]) > 0:
            data = {
                "projectId": dataDict["projectId"][0],
                "dataIds": int(dataDict["projectId"][0]) + 1,
                "operatorId": self.authUserId,
                "status": 3,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook)

    @allure.title("添加研究者列表")
    @allure.story("项目审核后的操作")
    def giveDoctorList(self):
        url = host + port_project + "/project/user/list.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = dict(dataType=2,
                    projectId=dataDict["projectId"][0],
                    path=f"400,{self.itemOrgId},",
                    status=1,
                    username="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        ff = json.loads(result.text)["responseData"]["content"]
        listdataId = []
        if len(ff) > 0:
            for i in ff:
                listdataId.append(i["ORG_USER_ID"])
            return listdataId

    @allure.title("添加医生的团队")
    @allure.story("项目审核后的操作")
    def givePratitionerBase(self):
        url = host + port_project + "/project/user/practitioner/base.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = dict(projectId=dataDict["projectId"][0], orgUserId=self.authUserId, authUserId=self.authUserId,
                    authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        aa = json.loads(result.text)["responseData"]["orgInfoVo"]
        return aa["teamOrgId"]

    @allure.title("也可以添加医生 参与医生")
    @allure.story("项目审核后的操作")
    def test_startStatus_addDoctor(self):
        url = host + port_project + "/project/user/create.json"
        dataDict = self.get_projectId(["3"])
        listDataId = self.giveDoctorList()
        orgId = self.givePratitionerBase()
        allure.attach(f"项目Id={dataDict['projectId']}\nlistdataId={listDataId}\norgId={orgId}")
        data = dict(dataType=2,
                    projectId=dataDict["projectId"][0],
                    dataIds=listDataId[0],
                    status=2,
                    joinType=2,
                    orgId=orgId,
                    operatorId=self.authUserId,
                    authUserId=self.authUserId,
                    authToken=self.authToken)
        assert_post(url, data, self.cook, str(orgId))

    # # 这个接口吃了一个ID
    # @pytest.mark.q1
    # def test_startStatus_updataUser(self):  # 参与研究者-撤回申请 撤回参与人员的申请
    #     url = host + port_project + "/project/user/practitioner/update.json"
    #     ids = self.get_practitionerList()
    #     dataDict = self.get_projectId(["3"])
    #     print(f'审核后-进行项目的状态+{dataDict["projectId"]}')
    #     data = dict(id=ids,
    #                 status=9,
    #                 operatorId=self.authUserId,
    #                 authUserId=self.authUserId,
    #                 authToken=self.authToken)
    #     requests.post(url, data, cookies=self.cook)
    #     assert "true" in result.text
    @allure.title("获取审核过后的 参与研究者的信息 参与医生列表")
    @allure.story("项目审核后的操作")
    def get_practitionerList(self):
        url = host + port_project + "/project/user/practitioner/list.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "path": f"400,{self.itemOrgId}",
            "username": "",
            "page": 1,
            "size": 10,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        valuesList = json.loads(result.text)["responseData"]["content"]
        if len(valuesList) >= 1:
            for i in valuesList:
                if i["PROJECT_FUNCTION"] is not None:
                    return i["ID"]
        else:
            print(f"请先添加参与的医生")

    @allure.title("获取指标列表的，受试者分组-来添加患者-指标列表")
    @allure.story("项目审核后的操作")
    def test_startStatus_dataIndex(self):
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = {
            "operatorId": self.authUserId,
            "topCategoryId": 3108,
            "diseaseIds": 1,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "3018")

    @allure.title("申请项目保存基础信息-用于修改项目信息")
    @allure.story("项目审核后的操作")
    def transfer_saveBase(self):
        url = host + port_project + "/project/info/base.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "orgUserId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        resultDic = json.loads(result.text)
        projectGroupId = 7390
        if "startUpPeriodDTO" in result.text:
            projectGroupId = resultDic["responseData"]["startUpPeriodDTO"]["projectGroupId"]
        return projectGroupId

    @allure.title("我的项目->申请项目：分中心 数据展示")
    @allure.story("项目审核后的操作")
    def transfer_groupsList(self):
        url = host + port_project + "/project/info/minute-center/list.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "centerProjectName": "",
            "operatorId": self.authUserId,
            "page": 1,
            "size": 10,
            "projectStatus": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        listIds1 = {"PATIENT_ID": [], "dataIds": []}
        resultdic = json.loads(result.text)["responseData"]
        if type(resultdic) is list:
            aa = resultdic[0]["dataPage"]["content"]
            if len(aa) > 0:
                for i in aa:
                    listIds1["PATIENT_ID"].append(i["PATIENT_ID"])
                    listIds1["dataIds"].append(i["ORG_USER_ID"])
        else:
            aa = resultdic["content"]
            for i in aa:
                listIds1["PATIENT_ID"].append(i["CENTER_PROJECT_ID"])
        return listIds1

    @allure.title("进行中的项目 从筛选中 添加受试患者")
    @allure.story("项目审核后的操作")
    def test_startStatus_userCreate(self, resultList):
        url = host + port_project + "/project/user/create.json"
        # orgId = ['4400004', '4398028', '4400025', '4399480', '4399358', '4399695', '4398293',
        #  '4399608', '4400047', '4400077', '4398368', '4399231']
        dataId = resultList["orgUserId"]
        dataIds = ""
        for i in dataId:
            dataIds += i + ","
        projectId = self.transfer_saveBase()
        centerProjectId = self.transfer_groupsList()["PATIENT_ID"]
        allure.attach(f"内部参数：筛选患者列表={resultList}\nprojectId={projectId}\ncenterProjectId={centerProjectId}")
        data = dict(dataType=1, status=1, projectId=projectId,
                    operatorId=self.authUserId,
                    centerProjectId=centerProjectId[0],
                    dataIds=dataIds,
                    grouptime=timelocal,
                    authUserId=self.authUserId,
                    authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("获取分组列表  并取值prevTaskId")
    @allure.story("项目审核后的操作")
    def getcarePlanId_ID(self):
        url = host + port_project + "/project/user/patient/list.json"
        projectId = self.transfer_saveBase()
        teamOrgId = self.givePratitionerBase()
        allure.attach(f"内部参数：projectId={projectId}\nteamOrgId={teamOrgId}")
        data = {
            "projectId": projectId, "fileStatus": "", "keyword": "",
            "operatorId": self.authUserId, "teamOrgId": teamOrgId,
            "page": 1, "size": 15,
            "authUserId": self.authUserId, "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        listPatient = {"taskId": [], "carePlanId": [], "ID": [], "ORG_USER_ID": [], "PROJECT_ID": [], "name": [],
                       "PROJECT_NAME": [], "patientId": [], "birthDay": [], "age": []}
        if len(resultdic) > 0:
            for i in resultdic:
                if "taskId" in i.keys():
                    listPatient["taskId"].append(i["taskId"])
                if "ID" in i.keys():  # 这两个参数是同是使用的
                    listPatient["carePlanId"].append(i["carePlanId"])
                    listPatient["ID"].append(i["ID"])
                if "ORG_USER_ID" in i.keys() and "PROJECT_ID" in i.keys() and "name" in i.keys() \
                        and "PROJECT_NAME" in i.keys():  # 用于添加不良事件用到指标
                    listPatient["ORG_USER_ID"].append(i["ORG_USER_ID"])
                    listPatient["PROJECT_ID"].append(i["PROJECT_ID"])
                    listPatient["name"].append(i["name"])
                    listPatient["PROJECT_NAME"].append(i["PROJECT_NAME"])
                listPatient["patientId"].append(i["patientId"])
                listPatient["birthDay"].append(i["BIRTHDAY"])
                listPatient["age"].append(i["age"])
        return listPatient

    @allure.title("把患者添加到分组里面 (添加失访和CRF记录都要 在受试者分组里面添加)")
    @allure.story("项目审核后的操作")
    def test_startStatus_patientCopy(self):
        url = host + port_project + "/project/user/patient/copy.json"
        dataDict = self.get_projectId(["3"])
        ids = self.getcarePlanId_ID()
        patiId = ""
        for i in ids["ID"]:
            patiId += i + ","
        allure.attach(f"内部参数：dataDict={dataDict}\nids={ids}")
        data = {
            "ids": patiId,
            "projectId": dataDict["projectId"][0],
            "grouptime": timelocal,
            "operatorId": self.authUserId,
            "groupType": 1,
            "centerProjectId": int(dataDict["projectId"][0]) + 1,
            "groupProjectId": int(dataDict["projectId"][0]) + 2,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("上传知情同意书")
    @allure.story("项目审核后的操作")
    def test_startStatus_uploadFile(self):
        url = host + port_project + "/project/user/patient/file/save.json"
        file = {"file": uploadpath1}
        dataDict = self.get_projectId(["3"])
        allure.attach(f"内部参数：dataDict={dataDict}")
        data = {
            "file": "(binary)",
            "projectId": dataDict["projectId"][0],
            # "dataId": 4609599,
            "dataType": 100,
            "status": 3,
            "operatorId": self.authUserId,
            "displayName": "生成图片.png"
        }
        assert_post(url, data, self.cook, files=file)

    @allure.title("添加失访记录")
    @allure.story("项目审核后的操作")
    def test_startStatus_appoint(self, dlogin):
        url = host + portlogin + "/appointment/reason.json"
        taskId = self.getcarePlanId_ID()["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        data = {
            "taskId": taskId[0],
            "comment": "备注",
            "reason": "|refuse-call",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        header = {"cookie": dlogin}
        assert_post(url, data, headers=header, hint=taskId[0])

    # @allure.title("标记访视记录")
    # @allure.story("项目审核后的操作")
    # @pytest.mark.skip("这个版本没有看见这个规则")
    # def test_startStatus_appoint(self):
    #     url = host + portlogin + "/appointment/expire.json"
    #     taskId = self.getcarePlanId_ID()["taskId"]
    #     data = {
    #         "taskId": taskId[0],
    #         "authUserId": self.authUserId,
    #         "authToken": self.authToken
    #     }
    #     assert_post_hint(url, data, self.cook, taskId[0])

    @allure.title("开始对CRF记录操作")
    @allure.story("项目审核后的操作")
    def test_InterviewStart(self, dlogin):
        url = host + portlogin + "/project/interview/start.json"
        taskId = self.getcarePlanId_ID()["taskId"]
        allure.attach(f"内部参数：taskId={taskId}")
        header = {"cookie": dlogin}
        if len(taskId) > 0:
            data = dict(taskId=taskId[1], performed="",
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_post(url, data, headers=header, hint=taskId[1])

    def token(self, dlogin):
        url = host + portlogin + "/project/interview/start.json"
        taskId = self.getcarePlanId_ID()["taskId"]
        token = "dac15828-f527-40b1-b6d4-493ccfa9fedd"
        allure.attach(f"内部参数：taskId={taskId}")
        if len(taskId) > 0:
            data = dict(taskId=taskId[0], performed="",
                        authUserId=self.authUserId, authToken=self.authToken)
            result = requests.post(url, data, headers={"cookie": dlogin})
            if "token" in result.text:
                resultdic = json.loads(result.text)["responseData"]["questionnaire"]
                token = json.loads(resultdic["token"])
        return token

    @allure.title("保存CRF记录")
    @allure.story("项目审核后的操作")
    def test_recordItem(self, dlogin):
        url = host + portlogin + "/record/item.json"
        patientId = self.getcarePlanId_ID()["patientId"]
        token = self.token(dlogin)
        allure.attach(f"内部参数：patientId={patientId}\n token={token}")
        data = dict(token=token, index=0,
                    isFirst=1, patientId=patientId[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def linkId(self, dlogin):
        url = host + portlogin + "/record/item.json"
        patientId = self.getcarePlanId_ID()["patientId"]
        token = self.token(dlogin)
        allure.attach(f"内部参数：patientId={patientId}\n token={token}")
        data = dict(token=token, index=0,
                    isFirst=1, patientId=patientId[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        linkId = "7a942264-7aac-4ff3-b91c-8dbe5a3ccf7b"
        result = requests.get(url, data, cookies=self.cook)
        if "linkId" in result.text:
            resultdic = json.loads(result.text)["responseData"]["questionnaire"]
            linkId = json.loads(resultdic)["item"][0]["linkId"]
        return linkId

    @allure.title("保存CRF记录")
    @allure.story("项目审核后的操作")
    def test_startStatus_saveCRF(self, dlogin):
        url = host + portlogin + "/project/interview/save.json"
        taskId = self.getcarePlanId_ID()["taskId"]
        linkId = self.linkId(dlogin)
        allure.attach(f"内部参数：taskID={taskId}\nlinkId={linkId}")
        data = {
            "taskId": taskId[0],
            "content": '[{"linkId":"%s","value":["|never"]}]' % linkId,
            "practitionerId": "Practitioner/190852",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, taskId[0])

    @allure.title("提交CRF问卷")
    @allure.story("项目审核后的操作")
    def test_startStatus_qtCheck(self, dlogin):
        url = host + port_qt + "/qtCheck/check.json"
        linkId = self.linkId(dlogin)
        patientId = self.getcarePlanId_ID()["patientId"]
        allure.attach(f"内部参数：linkId={linkId}\n patientId={patientId}")
        data = {
            "answerContent": '[{"linkId":"%s","value":["|never"]}]' % linkId,
            "patientId": patientId[0],
            "questionnaireUrl": "http://gyfyy.com/fhir/Questionnaire/xzwj0011-1571910299116",
            "type": "submit",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("提交CRF问卷信息")
    @allure.story("项目审核后的操作")
    def test_startStatus_interviewSubmit(self, dlogin):
        url = host + portlogin + "/project/interview/submit.json"
        linkId = self.linkId(dlogin)
        taskId = self.getcarePlanId_ID()["taskId"]
        allure.attach(f"内部参数：linkID={linkId}\n taskId={taskId}")
        data = {
            "taskId": taskId[0],
            "content": '[{"linkId":"%s","value":["|never"]}]' % linkId,
            "practitionerId": "Practitioner/190858",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, taskId[0])

    @allure.title("患者申请终止")
    @allure.story("项目审核后的操作")
    def test_startStatus_patientEndPlan(self):
        url = host + port_project + "/project/user/patient/endPlan.json"
        datadic = self.getcarePlanId_ID()
        ids = datadic["ID"]
        carePlanId = datadic["carePlanId"]
        allure.attach(f"内部参数：ids={ids}\n carePlanId={carePlanId}\n dataDic={datadic}")
        data = {
            "id": ids[0],
            "carePlanId": carePlanId[0],
            "operatorId": self.authUserId,
            "note": "为人踏实的",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, carePlanId[0])

    @allure.title("患者移除  项目")
    @allure.story("项目审核后的操作")
    def test_startStatus_patientRemovePlan(self):
        url = host + port_project + "/project/user/patient/removePlan.json"
        datadic = self.getcarePlanId_ID()
        ids = datadic["ID"]
        carePlanId = datadic["carePlanId"]
        allure.attach(f"内部参数：dataDic={datadic}\n ids={ids}\n carePlanId={carePlanId}")
        data = {
            "id": ids[0],
            "carePlanId": carePlanId[0],
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, carePlanId[0])

    @allure.title("受试者详情")
    @allure.story("项目审核后的操作")
    def test_startStatus_patientBase(self):
        url = host + port_project + "/project/user/patient/base.json"
        datadic = self.getcarePlanId_ID()
        ids = datadic["ID"]
        allure.attach(f"内部参数：datadic={datadic}\n ids={ids}")
        data = {
            "id": ids[0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("修改受试者的编号")
    @allure.story("项目审核后的操作")
    def test_startStatus_patientNumberUpdate(self):
        url = host + port_project + "/project/user/patient/update.json"
        datadic = self.getcarePlanId_ID()
        ids = datadic["ID"]
        allure.attach(f"内部参数：dataDic={datadic}\n    ids={ids}")
        data = {
            "id": ids[0],
            "dataCode": 123456789,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, str(ids[0]))

    @allure.title("添加AE不良事件")
    @allure.story("不良事件")
    def test_startStatus_event_eventToSavaGroup(self):
        url = host + port_project + "/project/event/toSaveGroup.json"
        listProject = self.getcarePlanId_ID()
        allure.attach(f"内部参数：listProject={listProject}")
        if len(listProject["PROJECT_ID"]) > 0:
            data = {
                "type": 1,
                "projectId": listProject["PROJECT_ID"][0],
                "patientId": listProject["ORG_USER_ID"][0],
                "patientName": listProject["name"][0],
                "projectName": listProject["PROJECT_NAME"][0],
                "category": 2,
                "reportUser": self.userName,
                "operatorId": self.authUserId,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook, listProject["ORG_USER_ID"][0])

    def getCode(self):
        url = host + port_project + "/project/event/toSaveGroup.json"
        listProject = self.getcarePlanId_ID()
        allure.attach(f"内部参数：projectId={listProject}")
        if len(listProject["PROJECT_ID"]) > 0:
            data = {
                "type": 1,
                "projectId": listProject["PROJECT_ID"][0],
                "patientId": listProject["ORG_USER_ID"][0],
                "patientName": listProject["name"][0],
                "projectName": listProject["PROJECT_NAME"][0],
                "category": 2,
                "reportUser": self.userName,
                "operatorId": self.authUserId,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            result = requests.post(url, data, cookies=self.cook)
            code = 1573117730317
            if "code" in result.text:
                code = json.loads(result.text)["responseData"]["code"]
            return code

    @allure.title("不良事件AE-实验相关资料显示")
    @allure.story("不良事件")
    @pytest.mark.parametrize(("code", "hint"), [("TEST_CLINICAL_TRIALS", "临床验证"), ("TEST_DRUG_DOSAGE","注射剂"), ("TEST_DRUG_REGIST_CATEGORY", "境内外均未上市的创新药"),
                                            ("TEST_DRUG_CATEGORY", "治疗用生物制品"), ("TEST_REPORT_SITUATION", "已在规定时限内完成上报"), ("SAE_SEVERITY1", "严重"), ("SAE_SEVERITY2", "4级（危及生命；需要紧急治疗"),
                                            ("SAE_DRUG_TEST_METHOD", "继续用药"), ("SAE_OUTCOME", "症状持续"), ("SAE_PATIENT_RELATED", "调整研究用药剂量"), ("PROJECT_EVENT_UNIT", "mg"),
                                            ("PROJECT_EVENT_USED", "Q6H"), ("SAE_DRUG_RELATED", "肯定有关")])
    def test_getCodeItemList(self, code, hint):
        url = host + portlogin + "/code/codeItem/getCodeItemList.json"
        data = dict(code=code, t=time_up,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint)

    @allure.title("不良事件AE-实验相关资料保存")
    @allure.story("不良事件")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_startStatus_event_SaveTestAE(self, start, end):
        url = host + port_project + "/project/event/saveTest.json"
        datadic = self.getcarePlanId_ID()
        projectName = datadic["PROJECT_NAME"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n projectName={projectName}\n code={code}")
        data1 = dict(no=22, reportDate="2019-11-07 00:00", clinicalApprovalNo="", orgName=self.hospital, centerNo="",
                     dept=self.hospital, projectName=projectName[0], projectStartdate=start, projectEnddate=end,
                     drugCategory="", drugRegistCategory="", drugDosage="", clinicalTrialsCategory="", code=code,
                     operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data1, self.cook)

    @allure.title("不良事件AE-实验相关资料修改保存")
    @allure.story("不良事件")
    def test_startStatus_event_updateTestAE(self):
        url = host + port_project + "/project/event/updateTest.json"
        datadic = self.getcarePlanId_ID()
        projectName = datadic["PROJECT_NAME"]
        allure.attach(f"内部参数：datdic={datadic}\n progectName={projectName}")
        data = dict(no=12, reportDate="2019-08-20 00:00", clinicalApprovalNo="新药临床研究批准文号",
                    orgName=self.hospital,
                    centerNo="中心编号", dept="胸外一区",
                    projectName=projectName[0],
                    projectStartdate="", projectEnddate="", drugName="试验用药品中文名称", drugNameEn="试验用药品英文名称",
                    drugCategory="BIOLOGICAL_PRODUCTS_PREVENTION", drugRegistCategory=1, drugDosage="TABLETS",
                    clinicalTrials="临床试验适应症", clinicalTrialsCategory="PHASE1",
                    id=700016, operatorId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("不良事件AE-受试者情况-保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveSubjectAE(self):
        url = host + port_project + "/project/event/saveSubjects.json"
        datadic = self.getcarePlanId_ID()
        birthDay = datadic["birthDay"]
        age = datadic["age"]
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n birthday={birthDay}\n age={age}\n "
                      f"projectId={projectId}\n patientId={patientId}\n code={code}")
        data = dict(nameRenPing="zzz", sex=1, birthDate=birthDay[0], age=age[0],
                    height="", weight="", randomNo="", importantInfo="",
                    code=code, complicationJson="", projectId=projectId[0], patientId=patientId[0],
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("不良事件AE情况详情保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveSaeAE(self):
        url = host + port_project + "/project/event/saveSae.json"
        datadic = self.getcarePlanId_ID()
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n projectId={projectId}\n patientId={patientId}\n code={code}")
        data = dict(saeName="未知事件", isSae=1, saeStartDate="2019-11-07 00:00",
                    saeEndDate="", severity1=1, severity2=1, drugTestMethod="继续用药",
                    saeOutcome=2, projectId=projectId[0], patientId=patientId[0], saePatientRelated="",
                    code=code, lastDate="", lastWeekNo="", chiefComplaint="",
                    analyticResult="有好转的迹象，结果分析", saeId="", labJson="", checkJson="",
                    complicationJson='[{"drug":"","usage":"","consumption":"","unit":"","startDate":"","endDate":"",'
                                     '"category":"3","id":""}]',
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, projectId[0])

    @allure.title("不良事件SAE-实验相关资料保存")
    @allure.story("不良事件")
    def test_startStatus_event_SaveTestSAE(self):
        url = host + port_project + "/project/event/saveTest.json"
        datadic = self.getcarePlanId_ID()
        projectName = datadic["PROJECT_NAME"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n projectName={projectName}\n code={code}")
        data = dict(reportFirst=1, reportSummary="", reportDate="2019-11-07 00:00", reportSituation=1, orgName=self.hospital,
                    centerNo=444444, dept=self.hospital, deptPhone="", projectName=projectName[0], projectStartdate="2019-11-07",
                    projectEnddate="2019-12-31", drugCategory="", drugRegistCategory="", drugDosage="", clinicalTrialsCategory="",
                    code=code, operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("不良事件SAE-实验相关资料修改保存")
    @allure.story("不良事件")
    def test_startStatus_event_updateTestSAE(self):
        url = host + port_project + "/project/event/updateTest.json"
        datadic = self.getcarePlanId_ID()
        projectName = datadic["PROJECT_NAME"]
        allure.attach(f"内部参数：datadic={datadic}\n projectName={projectName}")
        data = dict(reportFirst=1, reportDate="2019-08-20 00:00", clinicalApprovalNo="新药临床研究批准文号",
                    orgName=self.hospital,
                    centerNo="中心编号", dept="胸外一区",
                    projectName=projectName[0],
                    projectStartdate="", projectEnddate="", drugName="试验用药品中文名称", drugNameEn="试验用药品英文名称",
                    drugCategory="BIOLOGICAL_PRODUCTS_PREVENTION", drugRegistCategory=1, drugDosage="TABLETS",
                    clinicalTrials="临床试验适应症", clinicalTrialsCategory="PHASE1",
                    id=700016, operatorId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("不良事件SAE-受试者情况-保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveSubjectSAE(self):
        url = host + port_project + "/project/event/saveSubjects.json"
        datadic = self.getcarePlanId_ID()
        birthDay = datadic["birthDay"]
        age = datadic["age"]
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n birthday={birthDay}\n age={age}\n "
                      f"projectId={projectId}\n patientId={patientId}\n code={code}")
        data = dict(nameRenPing="zzz", sex=1, birthDate=birthDay[0], age=age[0],
                    height="", weight="", randomNo="", importantInfo="", isTest="",
                    isAgree="", agreeDate="", isChoice="", screenNo="", isAppropriate="",
                    code=code, complicationJson="", projectId=projectId[0], patientId=patientId[0],
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("不良事件SAE情况详情保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveSaeSAE(self):
        url = host + port_project + "/project/event/saveSae.json"
        datadic = self.getcarePlanId_ID()
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datdic={datadic}\n projectId={projectId}\n patientId={patientId}\n code={code}")
        data = dict(saeName="未知事件", isSae=1, saeStartDate="2019-11-07 00:00", saeInfo="延长住院时间",
                    saeEndDate="", severity1=1, severity2=1, drugTestMethod="继续用药", saeRealDate="2019-11-07 00:00",
                    saeOutcome=5, projectId=projectId[0], patientId=patientId[0], saePatientRelated="",
                    code=code, saeDrugRelated=1, testDrugRelated="",
                    drugStopStatus="", drugUseStatus="", saeReportIn=2, saeReportOut=3,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, projectId[0])


    @allure.title("不良事件SAE-发生及处理详情保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveProce(self):
        url = host + port_project + "/project/event/saveProce.json"
        datadic = self.getcarePlanId_ID()
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n projectId={projectId}\n patientId={patientId}\n code={code}")
        data = {
            "firstDate": "2019-11-01",
            "useDrugAmount": 1,
            "lastDate": "2019-12-07 00:00",
            "saeFirstInfo": "SAE发生前一次访视患者情况",
            "chiefComplaint": "主诉",
            "symptom": "症状",
            "sign": "体征",
            "diagnosis": "",
            "treatment": "",
            "saeSummary": '没有SAE汇总',
            "projectId": projectId[0],
            "patientId": patientId[0],
            "code": code,
            "description": "",
            "labJson": "",
            "checkJson": "",
            "complicationJson": "",
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, projectId[0])

    @allure.title("不良事件SAE-合并疾病详情保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveComplic(self):
        url = host + port_project + "/project/event/saveComplic.json"
        datadic = self.getcarePlanId_ID()
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n projectId={projectId}\n patientId={patientId}\n code={code}")
        data = {
            "complicationName": "合并疾病名称",
            "chiefComplaint": "主诉",
            "symptom": "症状",
            "sign": "体征",
            "diagnosis": "诊断",
            "treatment": "治疗",
            "projectId": projectId[0],
            "patientId": patientId[0],
            "code": code,
            "description": "",
            "labJson": "",
            "checkJson": "",
            "complicationJson": "",
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, projectId[0])

    @allure.title("不良事件SAE-单位以及报告人详情保存")
    @allure.story("不良事件")
    def test_startStatus_event_saveReport(self):
        url = host + port_project + "/project/event/saveReport.json"
        datadic = self.getcarePlanId_ID()
        projectId = datadic["PROJECT_ID"]
        patientId = datadic["ORG_USER_ID"]
        code = self.getCode()
        allure.attach(f"内部参数：datadic={datadic}\n projectId={projectId}\n patientId={patientId}\n code={code}")
        data = {
            "name": "广州医科大学附属第一医院",
            "contactName": "联系人",
            "phone": "0371665432",
            "reportUser": "报告人",
            "reportUserNo": 74349,
            "reportUserPost": "报告人职务/职称",
            "reportUserPhone": 22215,
            "remark": "备注",
            "projectId": projectId[0],
            "patientId": patientId[0],
            "status": "",
            "code": code,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, projectId[0])

    # @allure.title("不良事件SAE-单位以及报告人详情保存")
    # @allure.story("不良事件")
    # @pytest.mark.skip("这个版本没有这个功能")
    # def test_startStatus_event_updateProjectEvent(self):
    #     url = host + port_project + "/project/event/updateProjectEvent.json"
    #     datadic = self.getcarePlanId_ID()
    #     ids = datadic["ID"]
    #     data = dict(id=ids[0],  # 注意ID
    #                 authUserId=self.authUserId,
    #                 authToken=self.authToken)
    #     assert_post(url, data, self.cook)

    @allure.title("发起中期汇报")
    @allure.story("中期汇报")
    def test_startStatus_interimReport(self):
        url = host + port_project + "/project/result/report/interimReport/initiate.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "operatorId": self.authUserId,
            "interimReportRemind": "新增中期汇报",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("发起中期汇报-开始发起汇报")
    @allure.story("中期汇报")
    def test_startStatus_reportmodel(self):
        url = host + port_project + "/project/result/save.json"
        projectId = self.get_projectId(["3"])["projectId"]
        allure.attach(f"项目Id={projectId}")
        data = dict(status=3, projectId=projectId[0], projectStage=1,
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("发起中期汇报-发起汇报-进行中")
    @allure.story("中期汇报")
    @pytest.mark.parametrize("jsonparam",('[{"paymentType":""}]','[{"fromTime":"","endTime":""}]',
                                          '[{"centerProjectId":"5569"}]'))
    def test_startStatus_reportreSultModel(self, jsonparam):
        url = host + port_project + "/project/result/save.json"
        projectId = self.get_projectId(["3"])["projectId"]
        if "centerProjectId" in jsonparam:
            jsonparam = '[{"centerProjectId":"%s"}]' % projectId[0]
        allure.attach(f"内部参数：projectId={projectId}\n jsonparam={jsonparam}")
        data = dict(projectId=projectId[0], projectStage=1, operatorId=self.authUserId,
                    jsonParam=jsonparam,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("锁库结题")
    @allure.story("中期汇报")
    def test_startStatus_lockLibraryReport(self):
        url = host + port_project + "/project/result/report/lockLibraryReport.json"
        dataDict = self.get_projectId(["3"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": dataDict["projectId"][0],
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, dataDict["projectId"][0])

    @allure.title("锁库结题-项目分中心列表")
    @allure.story("中期汇报")
    def test_myProgect_startStatus_report_infolist(self):
        url = host + port_project + "/project/info/minute-center/list.json"
        projectId = self.get_projectId(["5"])["projectId"]
        allure.attach(f"项目Id={projectId}")
        data = dict(projectId=projectId[0], centerProjectName="", operatorId=self.authUserId,
                    page=1, size=10, projectStatus="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("项目进度-汇报-保存")
    @allure.story("中期汇报")
    def test_startStatus_report_projectResultSave(self):
        url = host + port_project + "/project/result/save.json"
        dataDict = self.get_projectId(["5"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "status": 2,
            "projectId": int(dataDict["projectId"][0]) + 1,
            "projectStage": 1,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("项目进度-汇报-详情列表")
    @allure.story("中期汇报")
    def test_startStatus_report_centerPorgressList(self):
        url = host + port_project + "/project/result/center/progress/list.json"
        dataDict = self.get_projectId(["5"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "projectId": int(dataDict["projectId"][0]) + 1,
            "projectStage": 1,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("项目进度-汇报-保存阶段成果")
    @allure.story("中期汇报")
    def test_startStatus_report_paymentListSave(self):
        url = host + port_project + "/project/result/paymentList/save.json"
        dataDict = self.get_projectId(["5"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "jsonParam": '[{"paymentType": ""}]',
            "projectId": int(dataDict["projectId"][0]) + 1,
            "projectStage": 1,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("项目进度-汇报-保存项目具体情况")
    @allure.story("中期汇报")
    def test_startStatus_report_timeLineListSave(self):
        url = host + port_project + "/project/result/timelineList/save.json"
        dataDict = self.get_projectId(["5"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "jsonParam": '[{"fromTime":"2019-08-01","endTime":"2019-08-20","phaseDesc":"委任为"}]',
            "projectId": int(dataDict["projectId"][0]) + 1,
            "projectStage": 1,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data,self.cook)

    @allure.title("项目进度-汇报-保存项目汇报数据情况")
    @allure.story("中期汇报")
    def test_startStatus_report_centerProgressSave(self):
        url = host + port_project + "/project/result/center/progress/save.json"
        dataDict = self.get_projectId(["5"])
        allure.attach(f"项目Id={dataDict['projectId']}")
        data = {
            "jsonParam": '[{"centerProjectId":"3583136"},{"centerProjectId":"3583139"}]',
            "projectId": int(dataDict["projectId"][0]) + 1,
            "projectStage": 1,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)


if __name__ == '__main__':
    pytest.main(["-v -s test_myProgect.py -m=q1"])
