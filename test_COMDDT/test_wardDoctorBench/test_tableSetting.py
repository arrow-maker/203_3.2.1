#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_tableSetting.py
@time: 2019/9/23  11:34
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("工作台设置")
class Test_tableSetting:

    @allure.title("工作台首页指标 - 指标数据展示")
    @allure.story("预警设置")
    def test_findConfig(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/findConfig.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    medCode="COPD-001",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("工作台首页指标 - 预警列表")
    @allure.story("预警设置")
    def transfer_findConfig(self, response1, cook):
        url = host + port_sourcedata + "/reportWarning/findConfig.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    medCode="COPD-001",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        datadic = {"ids": [], "reportNo": []}
        resultdic = json.loads(result.text)["responseData"]
        if len(resultdic) > 0:
            for i in resultdic:
                datadic["ids"].append(i["id"])
                datadic["reportNo"].append(i["reportNo"])
        return datadic

    def transfer_findReport(self, response1, cook):
        url = host + port_sourcedata + "/reportWarning/findReport.json"
        data = dict(medCode="COPD-001", groupNo="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        ids = []
        for i in resultdic:
            ids.append(i["reportNo"])
        return ids

    @allure.title("工作台首页指标 - 可选-选择-指标名称下拉列表")
    @allure.story("预警设置")
    def test_findReport(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/findReport.json"
        data = dict(medCode="COPD-001", groupNo="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("工作台首页指标 - 添加预警指标")
    @allure.story("预警设置")
    def test_saveConfig(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/saveConfig.json"
        reportNo1 = self.transfer_findConfig(response1, cook)["reportNo"]  # 添加过的report
        reportNo2 = self.transfer_findReport(response1, cook)  # 所有的report
        allure.attach(f"内部参数：report1={reportNo1}\n report2={reportNo2}")
        if len(reportNo1) > 0:  # 这里是取没有添加过的reportNo
            reportNo = list(set(reportNo2) ^ set(reportNo1))  # 取差集 这里可以使用^或者使用-都可以
        else:
            reportNo = reportNo2
        data = dict(hospitalCode=response1["hospitalCode"], medCode="COPD-001",
                    reportNo=reportNo[0],  # 这个只能使用一次
                    upper=9, lower=1,
                    # id="",               # 当有参数id时，是修改的指标
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("工作台首页指标 -删除 指定的预警信息")
    @allure.story("预警设置")
    def test_deleteConfig(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/deleteConfig.json"
        ids = self.transfer_findConfig(response1, cook)["ids"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(id=ids[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("诊疗组指标-指标类型-下拉框")
    @allure.story("诊疗组设置")
    def test_findGroup(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/findGroup.json"
        data = dict(medCode="COPD-001",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("诊疗组设置 医院和科室选择")
    @allure.story("诊疗组设置")
    def test_getOrgInfoTreeList(self, login):
        response1, cook = login
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400,",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_path(self, response1, cook):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400,",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        path = []
        resultdic = json.loads(result.text)["responseData"][0]["children"]
        if resultdic is not None:
            for i in resultdic:
                path.append(i["path"])  # 医院
                if i["children"] is not None:
                    for j in i["children"]:
                        path.append(j["path"])  # 科室
                        if j["children"] is not None:
                            for k in j["children"]:
                                if k["children"] is not None:
                                    path.append(k["children"])  # 组
        return path

    @allure.title("样式 有科室没有可以添加的数据")
    @allure.story("诊疗组设置")
    def test_style(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/report/basicInfo/style.json"
        reportNo = self.transfer_findConfig(response1, cook)["reportNo"]
        allure.attach(f"内部参数：reportNo={reportNo}")
        if len(reportNo) > 0:
            data = dict(reportNos=reportNo[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, reportNo[0])

    @allure.title("诊疗组设置 - 诊疗组列表数据展示")
    @allure.story("诊疗组设置")
    def test_groupList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/list"
        path1 = self.transfer_path(response1, cook)
        allure.attach(f"内部参数：path={path1}")
        data = dict(path=path1[0], groupId="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("可选择的--诊疗组组长列表")
    @allure.story("诊疗组设置")
    def test_groupUserList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/user/list"
        path = self.transfer_path(response1, cook)
        allure.attach(f"内部参数：path={path}")
        data = dict(groupId="", path=path[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("查询组内的医生")
    @allure.story("诊疗组设置")
    def test_groupUserList2(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/user/list"
        path = self.transfer_path(response1, cook)
        groupId = self.transfer_groupId(response1, cook)
        allure.attach(f"内部参数：path={path}\n groupId={groupId}")
        if len(groupId[0]) > 0:
            data = dict(groupId=groupId[0][0],
                        # page=1,size=10,
                        # keyName="0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789",
                        path=path[0],
                        memberType=2,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            overWrite_assert_get_xls_hint(url, data, cook, wardDoctorBenchPath, "诊疗组内的医生")

    @allure.title("这里是诊疗组中的医生的列表")
    @allure.story("诊疗组设置")
    def transfer_groupUserList(self, response1, cook):
        url = host + port_sourcedata + "/workbench/group/user/list"
        path = self.transfer_path(response1, cook)
        allure.attach(f"内部参数：path={path}")
        data = dict(groupId="", path=path[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        userId = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                userId.append(i["ORG_USER_ID"])
        return userId

    @allure.title("新增诊疗组")
    @allure.story("诊疗组设置")
    def test_workBenchGroupSave(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/save"
        path = self.transfer_path(response1, cook)
        groupLeaderId = self.transfer_groupUserList(response1, cook)
        allure.attach(f"内部参数：path={path}\n groupleaderId={groupLeaderId}")
        data = dict(name="新增诊疗组3",
                    groupLeaderId=groupLeaderId[1],  # 诊疗组-组长传值过来
                    operatorId=response1["authUserId"],
                    path=path[1],  # 400,75635,75637,医院科室传值(这里可以确定是哪个科室的)400,75635,75827,沿江呼吸科
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    def transfer_groupId(self, response1, cook):
        url = host + port_sourcedata + "/workbench/group/list"
        path1 = self.transfer_path(response1, cook)
        allure.attach(f"内部参数：path={path1}")
        data = dict(path=path1[0], groupId="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = [[], []]
        resultdic = json.loads(result.text)["responseData"]["content"]
        if resultdic is not None:
            for i in resultdic:
                if int(i["MEMBER_COUNT"]) > 0:
                    ids[0].append(i["ID"])
                else:
                    ids[1].append(i["ID"])
        return ids

    @allure.title("诊疗组添加医生")
    @allure.story("诊疗组设置")
    def test_workBenchGroupUserSave(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/user/save"
        orgUserIds = self.transfer_groupUserList(response1, cook)
        groupId = self.transfer_groupId(response1, cook)
        allure.attach(f"内部参数:orguserId={orgUserIds}\n groupId={groupId}")
        if len(groupId[1][0]) > 0:   # 有医生可以添加
            data = {
                "groupId": groupId[1][0],  # 分组ID      给没有医生的组添加医生
                "operatorId": response1["authUserId"],
                "memberType": 2,  # 固定类型
                "orgUserIds": orgUserIds[0],  # 医生ID
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_post(url, data, cook, orgUserIds[0])

    def transfer_delectGroupList(self, group, response1, cook):
        url = host + port_sourcedata + "/workbench/group/user/list"
        path = self.transfer_path(response1, cook)
        allure.attach(f"内部参数：path={path}")
        data = dict(groupId=group, path=path[0],  # 这里数据是所有全部
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        userId = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                userId.append(i["ORG_USER_ID"])
        return userId

    @allure.title("诊疗组 移除医生")
    @allure.story("诊疗组设置")
    def test_workBenchGroupUserDelete(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/user/delete"
        groupId1 = self.transfer_groupId(response1, cook)
        if len(groupId1[0][0]) > 0:     # 有多余的组可以移除医生
            orgUserIds1 = self.transfer_delectGroupList(groupId1[0][0], response1, cook)  # 注意这里要保证是同一个的诊疗组
            allure.attach(f"内部参数：groupId={groupId1}\n orgUserIds={orgUserIds1}")
            data = dict(groupId=groupId1[0][0],
                        orgUserIds=orgUserIds1[0],
                        operatorId=response1["authUserId"], memberType=2,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook, groupId1[0][0])

    @allure.title("删除诊疗组")
    @allure.story("诊疗组设置")
    def test_workBenchGroupDelete(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/delete"
        groupId = self.transfer_groupId(response1, cook)
        assertdic = "存在组员，不允许删除", "SUCCESS"
        allure.attach(f"内部参数：groupId={groupId}")
        if len(groupId[1]) > 0 and len(groupId[0]) > 0:
            for i in range(len(groupId)):  # 分别删除带有成员和不带成员的
                data = dict(groupId=groupId[i][0], operatorId=response1["authUserId"],
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                assert_post(url, data, cook, assertdic[i])


if __name__ == '__main__':
    pytest.main(["-s", "-m", "q1", "test_tableSetting.py"])