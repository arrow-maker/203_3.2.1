# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_diseaseManagement.py
    Time:    2019/12/24 9:38
    Author:  Arrow
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *
picturepath = "/attachment/fileattachment/20191224103952-663025.png"
diseaseId = 202

@allure.feature("病种管理")
class Test_diseaseManage:

    @classmethod
    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]

    @allure.title("列表展示")
    @allure.story("病种类型操作")
    def test_getDataCategoryTreeList(self):
        url = host + port_resource + "/disease/meaCategory/getDataCategoryTreeList.json"
        data = {
            "categoryId": "",
            "categoryName": "",
            "path": "",
            "type": 1,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("添加新病种类型")
    @allure.story("病种类型操作")
    def test_saveDataCategory(self):
        url = host + port_resource + "/disease/meaCategory/saveDataCategory.json"
        data = {
            "categoryName": "新增病种",
            "categoryNameEng": "no name",
            "sequence": "",
            "remark": "添加数据",
            "categoryId": "",
            "parentCategoryId": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("病种类型列表")
    @allure.story("病种类型操作")
    def test_getTreeListByUser(self):
        url = host + port_resource + "/disease/getTreeListByUser.json"
        data = {
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("病种类型修改")
    @allure.story("病种类型操作")
    def test_saveDataCategory1(self):
        url = host + port_resource + "/disease/meaCategory/saveDataCategory.json"
        data = {
            "categoryNameEng": "no name",
            "remark": "添加数据",
            "type": 1,
            "categoryName": "新增病种",
            "sequence": "",
            "parentCategoryId": "",
            "categoryId": 141,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("删除病种类型")
    @allure.story("病种类型操作")
    def test_diseaseUpdateStatus(self):
        url = host + port_resource + "/disease/meaCategory/updateStatus.json"
        data = {
            "categoryId": 141,
            "status": 9,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("病种数据列表")
    @allure.story("病种数据操作")
    def test_disease_getList(self):
        url = host + port_resource + "/disease/getList.json"
        data = {
            "categoryId": 1,
            "page": 1,
            "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        global diseaseId
        for i in result[1]["responseData"]["content"]:
            if i["REMARK"] == "新增病种":
                diseaseId = i["DISEASE_ID"]

    def diseaseList(self):
        url = host + port_resource + "/disease/getList.json"
        data = {
            "categoryId": 1,
            "page": 1,
            "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        ids = []
        for i in result[1]["responseData"]["content"]:
            ids.append(i["DISEASE_ID"])
        return ids

    @allure.title("选择科室")
    @allure.story("病种数据操作")
    def test_orgInfogetOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = {
            "listType": 2,
            "status": 1,
            "orgTypeIds": "33,35,38",
            "path": 400,
            "orgName": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("上传病种图标")
    @allure.story("病种数据操作")
    def test_uploadFileattachment(self):
        url = host + portlogin + "/common/fileattachment/uploadFileattachment.json"
        file = {"file": open(uploadpath1, "rb")}
        result = assert_post(url, cook=self.cook, files=file, hint="生成图片")
        global picturepath
        picturepath = result[1]["responseData"]["path"] + result[1]["responseData"]["name"]

    @allure.title("保存新增病种数据")
    @allure.story("病种数据操作")
    def test_diseasesave(self):
        url = host + port_resource + "/disease/save.json"
        param = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        data = {
            "diseaseCodeId": 4,
            "diseaseId": "",
            "remark": "新增病种",
            "categoryId": 1,
            "addOrgIds": self.orgId,
            "deleteOrgIds": "",
            "status": 1,
            "url": "codp",
            "image": picturepath
        }
        assert_post(url, data, self.cook, params=param)

    @allure.title("病种状态修改")
    @allure.story("病种数据操作")
    @pytest.mark.parametrize("status", (0, 1))
    def test_updateStatusBatch(self, status):
        url = host + port_resource + "/disease/updateStatusBatch.json"
        data = {
            "diseaseIds": diseaseId,
            "status": status,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("修改病种数据")
    @allure.story("病种数据操作")
    def test_diseasesave1(self):
        url = host + port_resource + "/disease/save.json"
        param = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        data = {
            "diseaseCodeId": 11,
            "diseaseId": diseaseId,
            "remark": "慢阻肺",
            "categoryId": 1,
            "addOrgIds": self.orgId,
            "deleteOrgIds": "",
            "status": 1,
            "url": "codp",
            "image": picturepath
        }
        assert_post(url, data, self.cook, params=param)

    @allure.title("删除病种数据")
    @allure.story("病种数据操作")
    def test_updateStatusBatch2(self):
        url = host + port_resource + "/disease/updateStatusBatch.json"
        data = {
            "diseaseIds": diseaseId,
            "status": 9,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)