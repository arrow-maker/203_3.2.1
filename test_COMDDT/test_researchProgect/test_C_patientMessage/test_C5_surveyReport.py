# -*- coding: utf-8 -*-
from public.overWrite_Assert import *


@allure.feature("检验报告")
class Test_surveyReport:

    @allure.title("报告结果列表 数据展示")
    @allure.story("检验报告数据展示")
    def test_showList(self,login):
        response1, cook = login
        url = host + port_es + "/data/getVisitLabList.json"
        data = dict(packageItem="a",  # 检验组套 ：组套显示
                    patientname="", patientNo="",
                    startDate="",  # 时间设置
                    endDate="",
                    page=1, size=10, authUserId=response1["authUserId"],
                    authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("从报告结果列表中传值")
    @allure.story("检验报告数据展示")
    def transfer_visitLabList(self, response1, cook):
        url = host + port_es + "/data/getVisitLabList.json"
        data = dict(packageItem="",  # 检验组套 ：组套显示
                    patientname="", patientNo="",
                    startDate="",  # 时间设置
                    endDate="",
                    page=1, size=10, authUserId=response1["authUserId"],
                    authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicData = {"packageItem": [], "labSerialnum": []}
        if "SUCCESS" in result.text:
            if len(resultDic) > 0:
                for i in resultDic:
                    dicData["labSerialnum"].append(i["labSerialnum"])
                    dicData["packageItem"].append(i["packageItem"])
        return dicData

    @allure.title("检验结果 检验结果详情")
    @allure.story("检验报告数据展示")
    def test_getVisitLabByLabSerialnum(self, login):
        response1, cook = login
        url = host + port_es + "/data/getVisitLabByLabSerialnum.json"
        dd = self.transfer_visitLabList(response1, cook)
        allure.attach(f"内部参数：数据列表={dd}")
        if len(dd["packageItem"]) > 0:
            data = dict(labSerialnum=dd["labSerialnum"][0],  # 这里中报告结果列表中传值 ["responseData"]["content"][0]["labSerialnum"]
                        packageItem=dd["packageItem"][0],  # 这里中报告结果列表中传值 ["responseData"]["content"][0]["packageItem"]
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, dd["packageItem"][0])
        else:
            data = dict(labSerialnum=111111111111111,
                        # 这里中报告结果列表中传值 ["responseData"]["content"][0]["labSerialnum"]
                        packageItem="诱导痰",  # 这里中报告结果列表中传值 ["responseData"]["content"][0]["packageItem"]
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, "诱导痰")

    @allure.title("检验结果 录入患者列表")
    @allure.story("新录入患者信息")
    def test_add_findByCondition(self, login):
        response1, cook = login
        url = host + port_es + "/identifier/findByCondition"
        data = dict(
            page=11, size=10,
            globalParam="",
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("这个医生所在的科室")
    @allure.story("新录入患者信息")
    def test_add_getPatientTeam(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/visitLab/getPatientTeamInfo.json"
        data = dict(curUserId=response1["userId"],  # userid
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("报告配置 套件详情列表")
    @allure.story("报告配置")
    def test_dictItemGroup_findByDictItemGroup(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/dictItemGroup/findByDictItemGroup.json"
        data = dict(itemName="",
                    # page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证5")

    @allure.title("报告配置 套件详情列表")
    @allure.story("报告配置")
    def transfer_GroupList(self, response1, cook):
        url = host + port_sourcedata + "/dictItemGroup/findByDictItemGroup.json"
        data = dict(itemName="", page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicData = {"id": []}
        if "SUCCESS" in result.text:
            if len(resultDic) > 0:
                for i in resultDic:
                    dicData["id"].append(i["id"])
        return dicData

    @allure.title("报告配置 套件详情 新增套件")
    @allure.story("报告配置")
    def test_dictItemGroup_saveOrUpdateDictItemGroup(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/dictItemGroup/saveOrUpdateDictItemGroup.json"
        data = dict(id="",
                    itemName="儿童微软",
                    itemType="微软",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("套件详情 删除套件")
    @allure.story("报告配置")
    def test_dictItemGroup_deleteById(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/dictItemGroup/deleteById.json"
        ids = self.transfer_GroupList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = dict(ids=ids[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, str(ids))

    @allure.title("套件详情 套件里面的项目")
    @allure.story("报告配置")
    def test_dictItemGroup_findGroupIdandProjectName(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/dictItemProject/findGroupIdandProjectName.json"
        ids = self.transfer_GroupList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = dict(groupId=ids[0],  # 这里是从套件详情列表中传递过来的 ["responseData"]["content"][0]["id"]
                        projectName="",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, str(ids))

    @allure.title("套件详情 套件里面的项目")
    @allure.story("报告配置")
    def transfer_ProjectName(self, response1, cook):
        url = host + port_sourcedata + "/dictItemProject/findGroupIdandProjectName.json"
        ids = self.transfer_GroupList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = dict(groupId=ids[0],  # 这里是从套件详情列表中传递过来的 ["responseData"]["content"][0]["id"]
                        projectName="",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            result = requests.get(url, data, cookies=cook)
            resultDic = json.loads(result.text)["responseData"]
            ids1 = []
            if "SUCCESS" in result.text:
                if len(resultDic) > 0:
                    for i in resultDic:
                        ids1.append(i["id"])
            return ids1

    @allure.title("报告配置 套件详情 套件里面的项目新增项目")
    @allure.story("报告配置")
    def test_dictItemGroup_addsaveOrUpDictItemProject(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/dictItemProject/saveOrUpdateDictItemProject.json"
        ids = self.transfer_GroupList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = dict(groupId=ids[0],  # 从套件序列中传来的Id
                        sequence="123456",  # 序号 输入的数据
                        projectName="他依然也让8",  # 输入的数据 项目名称
                        projectCode="fgsd4",  # 项目的编码
                        unit="",                # 单位
                        refer="",               # 参考值
                        critical="",            # 危急值
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook, str(ids))

    @allure.title("报告配置 套件详情 删除套件 里面的项目")
    @allure.story("报告配置")
    def test_dictItemGroup_dictItemProjectDeleteById(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/dictItemProject/deleteById.json"
        ids = self.transfer_GroupList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = dict(ids=ids[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, str(ids[0]))


if __name__ == '__main__':
    pytest.main()