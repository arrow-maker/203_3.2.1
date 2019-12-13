# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_helpCenter.py
    Time:    2019/11/29 15:19
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *


@allure.feature("帮助中心")
class Test_helpCenter:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]

    @allure.title("数据展示")
    @allure.story("首页")
    @pytest.mark.parametrize("category, hint", ((1, "患者列表"), (2, "探索性分析"), (4, "修复了帮助中心能正常运行的bug")))
    def test_findArticleList(self, category, hint):
        url = host + port_help + "/help/findArticleList.json"
        data = dict(page=1, size=15, title="", operatorId=self.authUserId,
                    operatorName=self.userName, menuId="", orderby="",
                    category=category,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint)

    @allure.title("筛选关键字")
    @allure.story("首页")
    def test_findKeywordList(self):
        url = host + port_help + "/help/findKeywordList.json"
        data = dict(status=1, page=1, size=5, name="", isShow=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "筛选")

    @allure.title("用户手册菜单列表，问题汇总菜单")
    @allure.story("帮助中心菜单展示")
    @pytest.mark.parametrize("category", (1, 2))
    def test_findMenuList(self, category):
        url = host + port_help + "/help/findMenuList.json"
        data = dict(category=category,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "科研项目管理")

    @allure.title("更新信息")
    @allure.story("版本更新")
    def test_click(self):
        url = host + port_help + "/help/click.json"
        data = dict(operatorId=self.authUserId, operatorName=self.userName,
                    category=4, status=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, self.userName)

    @allure.title("演示操作1")
    @allure.story("功能演示")
    def test_getDataQueryGroupList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataQueryGroupList.json"
        data = dict(operatorId=self.authUserId, categoryId=15723,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("演示操作2")
    @allure.story("功能演示")
    def test_getSourceNum(self):
        url = host + port_dataindex + "/dataIndex/dataStore/getSourceNum.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("演示操作3")
    @allure.story("功能演示")
    def test_getDataIndexValueTreeList(self):
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(topCategoryId=15723,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "通用指标")