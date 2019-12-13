# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_contentManagement.py
    Time:    2019/12/2 15:46
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *

'''
这个项目现在的： 
    还不能添加标题和链接
    没有删除数据信息
    还没有写完？？？
'''
@allure.feature("内容管理")
class Test_management:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]
        self.orgId = response["responseData"]["roleList"][0]["orgId"]
        self.itemOrgId = response["responseData"]["itemOrgId"]

    @allure.title("患教知识分组")
    @allure.story("患教知识")
    def test_findInfoTypes(self):
        url = host + portlogin + "/info/info/findInfoTypes.json"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    def infoTypeId(self):
        url = host + portlogin + "/info/info/findInfoTypes.json"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result, resultdic = assert_get(url, data, self.cook)
        ids = []
        for i in resultdic["responseData"]:
            ids.append(i["infoTypeId"])
        return ids

    @allure.title("患教知识新增图片")
    @allure.story("患教知识")
    def test_findListInfo(self):
        url = host + portlogin + "/common/fileattachment/uploadImageAttachment.json"
        file = {"file": open(uploadpath1, "rb")}
        assert_post(url, files=file, cookies=self.cook)

    @allure.title("患教知识新增图片")
    @allure.story("患教知识")
    def test_findListInfo(self):
        url = host + portlogin + "/info/info/saveAndFlushInfo.json"
        infoTypeId = self.infoTypeId()
        allure.attach(f"传值参数：infoTypeId={infoTypeId}")
        data = dict(infoTypeId=infoTypeId[0], title="新增主题1.0", content="<p>验证数据组的正确性</p>",
                    imageUrl="http://192.168.0.203:3094/attachment/fileattachment/20191205162059.png",
                    top=0, authorName=self.userName, status=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("患教知识详细的数据来源(发布和已保存)")
    @allure.story("患教知识")
    @pytest.mark.parametrize("status", (1, 2))
    def test_findInfoPage(self, status):
        url = host + portlogin + "/info/info/findInfoPage.json"
        infoTypeId = self.infoTypeId()
        allure.attach(f"传值参数：infoTypeId={infoTypeId}")
        if len(infoTypeId) > 0:
            data = {
                "infoTypeId": infoTypeId[0],
                "title": "",
                "status": status,
                "page": 1,
                "size": 10,
                "timeStamp": time_up,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_get(url, data, self.cook)

    @allure.title("患教知识所有的数据")
    @allure.story("患教知识")
    def test_findListInfo(self):
        url = host + portlogin + "/info/info/findListInfo.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def infoId(self):
        url = host + portlogin + "/info/info/findInfoPage.json"
        infoTypeId = self.infoTypeId()
        allure.attach(f"传值参数：infoTypeId={infoTypeId}")
        if len(infoTypeId) > 0:
            data = {
                "infoTypeId": infoTypeId[0],
                "title": "",
                "status": 1,
                "page": 1,
                "size": 10,
                "timeStamp": time_up,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            result, resultdic = assert_get(url, data, self.cook)
            ids = []
            for i in resultdic["responseData"]["content"]:
                ids.append(i["infoId"])
            return ids

    @allure.title("患教知识数据删除")
    @allure.story("患教知识")
    def test_removeInfo(self):
        url = host + portlogin + "/info/info/removeInfo.json"
        infoId = self.infoTypeId()
        allure.attach(f"传值参数：infoTypeId={infoId}")
        if len(infoId) > 0:
            data = dict(infoId=infoId[0],
                        authUserId=self.authUserId, authToken=self.authToken)
            assert_post(url, data, self.cook)

    @allure.title("图片信息")
    @allure.story("首页发布")
    def test_findHomeList(self):
        url = host + portlogin + "/info/info/findHomeList.json"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)
