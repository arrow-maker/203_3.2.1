#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_userControl.py
@time: 2019/9/17  14:44
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("角色权限管理")
class Test_userControl:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]
        self.itemOrgId = response1["responseData"]["itemOrgId"]

    @allure.title("获取医院机构列表")
    @allure.story("页面加载显示")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38", path="400,",
                    # orgName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        overWrite_assert_get_xls_hint(url, data, self.cook, systemPath, "用户管理-医院机构")

    @allure.title("获取用户列表")
    @allure.story("页面加载显示")
    def test_getUsersList(self):
        url = host + portlogin + "/projectUser/getUsersList.json"
        data = dict(
            # keyword="",     # 输入的
            path=f"400,{self.itemOrgId}",
            # page=1, size=15,
            authUserId=self.authUserId, authToken=self.authToken)
        overWrite_assert_get_xls_hint(url, data, self.cook, systemPath, "用户管理-用户信息")

    def transfer_getUsersList(self):
        url = host + portlogin + "/projectUser/getUsersList.json"
        data = dict(
            keyword="",  # 输入的
            path=f"400,{self.itemOrgId}",
            page=1, size=15,
            authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        dicdata = {"userid": [], "token": [], "orgId": [], "username": [], "mobile": [], "notInPositionIds": []}
        if len(resultdic) > 0:
            for i in resultdic:
                dicdata["userid"].append(i["USERID"])
                dicdata["token"].append(i["token"])
                dicdata["username"].append(i["USERNAME"])
                dicdata["mobile"].append(i["MOBILE"])
                dicdata["orgId"].append(i["ORG_ID"])
                dicdata["notInPositionIds"].append(i["ALL_POSITION_ID"])
        return dicdata

    @allure.title("用户信息 修改")
    @allure.story("操作")
    def test_updatePractitioner(self):
        url = host + portlogin + "/projectUser/updatePractitioner.json"
        dicdata = self.transfer_getUsersList()
        userid = dicdata["userid"]
        token = dicdata["token"]
        username = dicdata["username"]
        mobile = dicdata["mobile"]
        allure.attach(f"内部参数：dicdata={dicdata}\n userId={userid}\n "
                      f"token={token}\n username={username}\n mobile={mobile}")
        data = dict(userid=userid[0], token=token[0],
                    email="1213456@qq.com", username=username[0], mobile=mobile[0], sex=1,
                    companyaccount="meyi", operatorFunction="51050-addUser",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, username[0])

    @allure.title("禁用或者启用")
    @allure.story("操作")
    def test_updateUserStatus(self):
        url = host + portlogin + "/users/users/updateUserStatus.json"
        dicdata = self.transfer_getUsersList()
        userid = dicdata["userid"]
        token = dicdata["token"]
        allure.attach(f"内部参数：dicdata={dicdata}\n userId={userid}\n token={token}")
        data = dict(userid=userid[0], token=token[0], status=1, operatorFunction="51050-addUser",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, userid[0])

    @allure.title("分配权限前 上")
    @allure.story("操作")
    def test_getOrgPositionList(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        dicdata = self.transfer_getUsersList()
        notInPositionIds = dicdata["notInPositionIds"][0]
        orgId = self.itemOrgId
        allure.attach(f"内部参数：dicdata={dicdata}\n orgId={orgId}")
        data = dict(orgId=orgId, status=1, notInPositionIds=notInPositionIds,
                    operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("分配权限前 下")
    @allure.story("操作")
    def test_getOrgPositionList2(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        dicdata = self.transfer_getUsersList()
        notInPositionIds = dicdata["notInPositionIds"][0]
        orgId = self.itemOrgId
        allure.attach(f"内部参数：dicdata={dicdata}\n orgId={orgId}")
        data = dict(orgId=orgId, status=1, positionIds=notInPositionIds,
                    operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def transfer_getOrgPositionList(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        dicdata = self.transfer_getUsersList()
        notInPositionIds = dicdata["notInPositionIds"][0]
        orgId = self.itemOrgId
        allure.attach(f"内部参数：dicdata={dicdata}\n orgId={orgId}")
        data = dict(orgId=orgId, status=1, notInPositionIds=notInPositionIds,
                    operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["POSITION_ID"])
        return ids

    @allure.title("保存分配的权限")
    @allure.story("操作")
    def test_saveOrUpdateOrgDummyUser(self):
        url = host + portlogin + "/org/orgDummyUser/saveOrUpdateOrgDummyUser.json"
        dicdata = self.transfer_getUsersList()
        userId = dicdata["userid"]
        orgId = dicdata["orgId"]
        # 这里从上往下加权限（使用）
        positionId1 = self.transfer_getOrgPositionList()
        # 这里从下往上去权限（使用）
        notInPositionIds = self.transfer_getUsersList()["notInPositionIds"][0]
        positionIdsList = notInPositionIds.split(",")
        positionId2 = positionIdsList[-1]
        allure.attach(f"内部参数：dicdata={dicdata}\n userId={userId}\n position2={positionId2}")
        data = dict(userId=userId[0], orgId=orgId[0], positionId=positionId2, status=9,
                    operatorFunction="51050-roleChange",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, userId[0])

    @allure.title("重置密码的页面显示")
    @allure.story("重置密码")
    def test_getParamByCode(self):
        url = host + portlogin + "/param/getParamByCode.json"
        data = dict(codes="initial_password",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "tP123456@")

    @allure.title("确认重置密码")
    @allure.story("重置密码")
    def test_initUserPassWord(self):
        url = host + portlogin + "/users/users/initUserPassWord.json"
        dicdata = self.transfer_getUsersList()
        token = dicdata["token"]
        userid = dicdata["userid"]
        allure.attach(f"内部参数：dicdata={dicdata}\n token={token} \n userId={userid}")
        data = dict(token=token[4],
                    userid=userid[4],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, "初始化密码成功")

    @allure.title("新增用户前的界面显示")
    @allure.story("新增用户")
    def test_getOrgPositionList3(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        data = dict(orgId=self.itemOrgId, status=1, operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def transfer_getOrgPositionList3(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        data = dict(orgId=self.itemOrgId, status=1, operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["POSITION_ID"])
        return ids

    @allure.title("创建新增的用户")
    @allure.story("新增用户")
    def test_createPractitioner(self):
        url = host + portlogin + "/projectUser/createPractitioner.json"
        positionId = self.transfer_getOrgPositionList3()
        allure.attach(f"内部参数：positionId={positionId}")
        data = dict(gender="male", positionId=positionId[0],orgId=self.itemOrgId,
                    name="abcdef",  loginname="012345691", telecom="aaa", email="邮箱", companyaccount="职称",
                    direct="true", operatorFunction="51050-addUser",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        overWrite_assert_post_xls_hint(url, data, self.cook, systemPath, "角色权限管理-添加用户")


if __name__ == '__main__':
    pytest.main("test_userControl.py")