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


@allure.feature("全景配置")
class Test_viewsConfigure:

    @classmethod
    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]

    @pytest.fixture(scope="class")
    def orgId(self, request):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400", orgName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        patientId = ["75722"]     # 科室的Id
        for i in result[1]["responseData"][0]['children'][0]["children"]:
            patientId.append(i["id"])
        return patientId[request.param]

    @allure.title("科室选择列表")
    @allure.story("全景配置")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400", orgName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("按照科室的菜单列表")
    @allure.story("全景配置")
    @pytest.mark.parametrize("orgId", [0, 1, 2], indirect=True)
    @pytest.mark.parametrize("Name", ("", "首页"))
    def test_getAuthTreeList(self, orgId, Name):
        """
        :param orgId: 这里的是点击不同的科室
        :param Name:    这里是搜索不同的菜单
        :return:
        """
        url = host + portlogin + "/auth/function/getAuthTreeList.json"
        data = dict(type=1, orgId=orgId, roleId=0, groupName=Name,
                    path=8000001, operatorId=self.authUserId, operatorFunction="51054-getMenu",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("添加/删除菜单列表")
    @allure.story("菜单列表操作")
    @pytest.mark.parametrize("adds", ("", functionIds))
    @pytest.mark.parametrize("deleIds", (functionIds, ""))
    def test_saveRoleFunctionR(self, dlogin, adds, deleIds):
        """
        :param dlogin:  登录的cookie
        :param adds:    添加的菜单的Id
        :param deleIds: 删除的菜单的Id
        :return:
        """
        url = host + portlogin + "/auth/function/saveRoleFunctionR.json"
        header = {"cookie": dlogin}
        data = dict(addIds=adds,
                    deleteIds=deleIds,
                    orgId=self.orgId, roleId=0, operatorId=self.authUserId, operatorFunction="51054-editMenu",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, headers=header)

    @allure.title("用户列表")
    @allure.story("全景配置")
    @pytest.mark.parametrize("orgId", [0], indirect=True)
    @pytest.mark.parametrize("word", ("", "a", "1"))
    def test_getUsersList(self, orgId, word):
        """
        :param orgId:   用户所在的科室
        :param word:    搜索配置的关键字
        :return:
        """
        url = host + portlogin + "/projectUser/getUsersList.json"
        print(f"\norgId={orgId}")
        data = dict(keyword=word, path=f"400,{orgId}",
                    page=1, size=15,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, word)