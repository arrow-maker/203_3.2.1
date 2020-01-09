#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_roleBasedAccessControl.py
@time: 2019/9/16  14:36
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("角色权限管理")
class Test_roleBasedAccessControl:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]
        self.itemOrgId = response1["responseData"]["itemOrgId"]
        self.idToken = response1["responseData"]["roleList"][0]["idToken"]
        self.ids = response1["responseData"]["roleList"][0]["id"]

    @allure.story("获取医院列表")
    def test_getHospitalList(self, dlogin):
        url = host + portlogin + "/platform/hospital/getHospitalList.json"
        data = dict(name="", orgId=self.itemOrgId,
                    authUserId=self.authUserId, authToken=self.authToken)
        header = {"cookie": dlogin}
        assert_get(url, data, headers=header, hint=str(self.itemOrgId))

    @allure.title("获取患者列表")
    def test_getOrgPositionList(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        data = dict(orgId=self.itemOrgId,
                    status=1, operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def transfer_getOrgPositionList(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        data = dict(orgId=self.itemOrgId,
                    status=1, operatorFunction="51054-getRoleList",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        datadic = {"ids": [], "postionIds": [], "token": [], "make": []}
        if "SUCCESS" in result.text:
            content = json.loads(result.text)["responseData"]["content"]
            if len(content) > 0:
                for i in content:
                    datadic["ids"].append(i["ROLEID"])
                    datadic["postionIds"].append(i["POSITION_ID"])
                    datadic["token"].append(i["token"])
        return datadic

    @allure.title("菜单列表")
    def test_getAuthTreeList(self):
        url = host + portlogin + "/auth/function/getAuthTreeList.json"
        ids = self.transfer_getOrgPositionList()["ids"][0]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(type=2, roleId=ids, groupName="", operatorFunction="51054-getMenu",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def transfer_MenuIds(self):  # 传递 菜单的ids
        url = host + portlogin + "/auth/function/getAuthTreeList.json"
        ids = self.transfer_getOrgPositionList()["ids"][0]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(type=2, roleId=ids, groupName="", operatorFunction="51054-getMenu",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]
        if type(resultdic) is list:
            # transfer = resultdic[0]["children"]
            for i in resultdic:  # 第一层菜单列表
                if len(i["children"]) > 0:
                    for j in i["children"]:  # 第二层菜单
                        if j["children"]:
                            if len(j["children"]) > 0:
                                lastmenu = []  # 以第二层为基组
                                for k in j["children"]:  # 第三层菜单
                                    if k["children"]:
                                        for m in k["children"]:  # 第四层
                                            lastmenu.append(m["id"])
                                    else:
                                        lastmenu.append(k["id"])
                                ids.append(lastmenu)  # 以最底层的id分组
        return tuple(ids)

    @allure.title("项目中的用户列表")
    def test_getUsersList(self):
        url = host + portlogin + "/projectUser/getUsersList.json"
        postionIds = self.transfer_getOrgPositionList()["postionIds"][0]
        data = dict(postionIds=postionIds, isDetail="true", status=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, postionIds)

    def transfer_getUserList(self):
        url = host + portlogin + "/projectUser/getUsersList.json"
        postionIds = self.transfer_getOrgPositionList()["postionIds"][0]
        allure.attach(f"内部参数：postionIds={postionIds}")
        data = dict(postionIds=postionIds, isDetail="true", status=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        dicdata = {"userId": [], "orgId": [], "dummyUserId": [], "token": [], "tokenId": []}
        if len(resultdic) > 0:
            for i in resultdic:
                dicdata["userId"].append(i["ORG_USER_ID"])
                dicdata["orgId"].append(i["ORG_ID"])
                dicdata["dummyUserId"].append(i["DUMMY_USER_ID"])
                dicdata["token"].append(i["token"])
                dicdata["tokenId"].append(i["USERID"])
        return dicdata

    @allure.title("患者医院的数据")
    def test_getPositionHospitalByPositionId(self):
        url = host + portlogin + "/common/positionHospitalData/getPositionHospitalByPositionId.json"
        postionIds = self.transfer_getOrgPositionList()["postionIds"][0]
        allure.attach(f"内部参数：postionIds={postionIds}")
        data = dict(positionId=postionIds,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, postionIds)

    def test_getListByPosition(self):
        url = host + port_resource + "/disease/getListByPosition.json"
        postionIds = self.transfer_getOrgPositionList()["postionIds"][0]
        allure.attach(f"内部参数：postionIds={postionIds}")
        data = dict(positionId=postionIds,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.story("选择 病种权限 列表")
    def test_getTreeList(self):
        url = host + port_resource + "/disease/getTreeList.json"
        data = dict(status=1, diseaseName="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.story("新增 角色")
    @pytest.mark.parametrize("name", ("院长", "科室主任", "病区主任"))
    def test_saveOrUpdateOrgPosition(self, name):
        url = host + portlogin + "/org/orgPosition/saveOrUpdateOrgPosition.json"
        data = dict(
            positionName=name,
            positionDesc="由描述",
            positionStatus=1,
            orgId=self.itemOrgId,
            operatorFunction="51054-addRole",
            operatorId=self.authUserId,
            authUserId=self.authUserId, authToken=self.authToken)
        result = requests.post(url, data, cookies=self.cook)
        self.roleid()  # 这里是刷新角色列表
        assert "由描述" in result.text

    def roleid(self):
        url = host + portlogin + "/org/orgPosition/getOrgPositionList.json"
        data = dict(orgId=self.itemOrgId,
                    status=1, operatorFunction="51054-getRoleList",  # 固定格式
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        temp = []
        content = result[1]["responseData"]["content"]
        if len(content) > 0:
            for i in content:
                if i["POSITION_DESC"] == "由描述":
                    temp.append((i["ROLEID"], i["token"]))
        tup1 = tuple(temp)
        return tup1

    @allure.story("新增 用户前的数据展示")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38",
                    path="400,73439,", orgName="", hospitalType=2,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.story("新增 用户")
    def test_saveOrUpdateOrgDummyUser(self):
        url = host + portlogin + "/org/orgDummyUser/saveOrUpdateOrgDummyUser.json"
        postionIds = self.transfer_getOrgPositionList()["postionIds"][0]
        dicdata = self.transfer_getUserList()
        userId = dicdata["userId"]
        orgId = dicdata["orgId"]
        allure.attach(f"内部参数：dicdata={dicdata}\n userId={userId}\n orgId={orgId}")
        data = dict(userId=userId[0], positionId=postionIds, orgId=orgId[0], operatorFunction="51054-addUser",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, postionIds)

    @allure.story("保存菜单修改")
    @pytest.mark.addrole1
    @pytest.mark.parametrize("deleteids", ("", "G_769598", "G_769598,G_771657", "G_769598,G_771657"))
    @pytest.mark.parametrize("addids", ("G_769598", "G_769598,G_771657", "G_769598,G_771657", ""))
    def test_saveRoleFunctionR(self, addids, deleteids, dlogin):
        """
            给的是固定的菜单（可以验证添加和删除固定的菜单 用parametrize）验证了删除，
                新增，新增两次，新增后删除，删除后新增等多种情况
            ids = self.transfer_MenuIds()     # 这里是给的动态添加的菜单
            print(f"\n={ids}")
        :param addids: 添加是菜单的Id
        :param deleteids: 删除的菜单的Id
        :return:
        """
        url = host + portlogin + "/auth/function/saveRoleFunctionR.json"
        header = {"cookie": dlogin}
        dicdata = self.roleid()
        allure.attach(f"内部参数：dicdata={dicdata}")
        data = dict(addIds=addids, deleteIds=deleteids, roleId=dicdata[0][0],
                    operatorId=self.authUserId, operatorFunction="51054-editMenu",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data, headers=header)
        # 在右侧菜单栏中验证
        if len(addids) > 0:
            idmenu = re.findall("\d+", addids)
            self.transfer_getMenu(idmenu[-1])  # 这里是右侧菜单栏验证
            assert addids in result[0]
        else:
            assert "SUCCESS" in result[0]

    # -----------新增 用户的删除------------------
    @allure.story("删除 用户")
    def test_deleteOrgDummyUser(self):
        url = host + portlogin + "/org/orgDummyUser/deleteOrgDummyUser.json"
        dicdata = self.transfer_getUserList()
        dummyUserId = dicdata["dummyUserId"][0]
        token = dicdata["token"][0]
        tokenId = dicdata["tokenId"][0]
        allure.attach(f"内部参数：dicdata={dicdata}\n dummyUesrId={dummyUserId}\n token={token}\n tokenId={tokenId}")
        data = dict(dummyUserId=dummyUserId, token=token,
                    tokenId=tokenId, operatorFunction="51054-delUser",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, str(dummyUserId))

    # -----------------------------保存修改信息-------------------------------------
    @allure.title("获取系统右侧的菜单列表 关联菜单的正确性")
    @allure.story("保存修改信息")
    def transfer_getMenu(self, hint):
        url = host + portlogin + "/ext/system/getMenu.json"
        data = {"id": self.ids,
                "idToken": self.idToken,
                "userAllMenu": "true",
                "authUserId": self.authUserId,
                "authToken": self.authToken}
        assert_post(url, data, self.cook, hint)

    @allure.title("删除角色信息")
    @allure.story("保存修改信息")
    def test_saveOrUpdateOrgPosition1(self):
        url = host + portlogin + "/org/orgPosition/saveOrUpdateOrgPosition.json"
        dicdata = self.roleid()
        allure.attach(f"内部参数：dicdata={dicdata}")
        for i in dicdata:
            data = dict(positionId=i[0], positionStatus=9, token=i[1],
                        orgId=self.itemOrgId, operatorFunction="51054-delRole",
                        operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
            assert_post(url, data, self.cook)


if __name__ == '__main__':
    pytest.main("test_roleBasedAccessControl.py -vv -reruns=5")
