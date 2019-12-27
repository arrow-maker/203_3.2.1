# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_viewsConfigure.py
    Time:    2019/12/27 13:54
    Author:  Arrow
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *
from pytest_lazyfixture import lazy_fixture
# 修改菜单列表
functionIds = "F_8000010,F_8000009,F_8000008,F_8000007,F_8000006,F_8000005,F_8000004,F_8000003,F_8000002,F_8000001," \
              "G_8000012,F_8000025,F_8000013,F_8000012,F_8000011,F_8000024,F_8000014,G_8000013,G_8000002,G_8000001",


@allure.feature("病种管理")
class Test_viewsConfigure:

    @classmethod
    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]

    @pytest.fixture(scope="class")
    def orgId(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400", orgName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        patientId = ["75722"]     # 科室的Id
        for i in result[1]["responseData"][0]['children'][0]["children"]:
            patientId.append(i["id"])
        return patientId

    @allure.title("科室选择列表")
    @allure.story("全景配置")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400", orgName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @pytest.fixture(scope="class", params=[pytest.lazy_fixture("orgId")])
    def param_orgId(self, request):
        print(f"\nparam_orgId={request.param}")
        return request.param

    @allure.title("按照科室的菜单列表")
    @allure.story("全景配置")
    @pytest.mark.parametrize("orgIds", [pytest.lazy_fixture("param_orgId")], indirect=True)
    @pytest.mark.parametrize("Name", ("", "首页"))
    def test_getAuthTreeList(self, orgIds, Name):
        url = host + portlogin + "/auth/function/getAuthTreeList.json"
        data = dict(type=1, orgId=orgIds, roleId=0, groupName=Name,
                    path=8000001, operatorId=self.authUserId, operatorFunction="51054-getMenu",
                    authUserId=self.authUserId, authToken=self.authToken)
        print(f"\norgIds={orgIds}")
        # assert_get(url, data, self.cook)

    @allure.title("添加/删除菜单列表")
    @allure.story("菜单列表操作")
    @pytest.mark.parametrize("adds", ("", functionIds))
    @pytest.mark.parametrize("deleIds", (functionIds, ""))
    def test_saveRoleFunctionR(self, dlogin, adds, deleIds):
        url = host + portlogin + "/auth/function/saveRoleFunctionR.json"
        header = {"cookie": dlogin}
        data = dict(addIds=adds,
                    deleteIds=deleIds,
                    orgId=self.orgId, roleId=0, operatorId=self.authUserId, operatorFunction="51054-editMenu",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, headers=header)

    @allure.title("用户列表")
    @allure.story("全景配置")
    def test_getUsersList(self):
        url = host + portlogin + "/projectUser/getUsersList.json"
        # print(f"\norgId={self.orgId}")
        data = dict(keyword="", path="400,75722,75726",
                    page=1, size=15,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)