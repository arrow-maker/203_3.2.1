# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_medicineKG.py
    Time:    2019/12/10 10:10
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *


@allure.feature("智医AKSO")
class Test_drug:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]

    @allure.title("药物分类")
    @allure.story("药物查询")
    def test_medicine_altasDefault(self):
        url = host + port_python + "/medicine_altas/default"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("药物查询")
    @allure.story("药物查询")
    def test_medicine_altasSearch_button(self):
        url = host + port_python + "/medicine_altas/search_button"
        data = dict(ywmc="", blfy="", syz="", jjz="", yplb="",
                    yytj="", scs="", cf="", pzwh="", page=1, size=200,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def goodId(self):
        url = host + port_python + "/medicine_altas/search_button"
        data = dict(ywmc="", blfy="", syz="", jjz="", yplb="",
                    yytj="", scs="", cf="", pzwh="", page=1, size=200,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        ids = []
        for i in result[1]["resultData"]["drugList"]:
            ids.append(i["商品ID"])
        return ids

    @allure.title("药物使用说明")
    @allure.story("药物查询")
    def test_medicine_altasSearch_button(self):
        url = host + port_python + "/medicine_altas/drug_instruction"
        ids = self.goodId()
        allure.attach(f"内部传参：goodId={ids}")
        data = dict(default=1, goods_id=ids[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("药物图谱")
    @allure.story("药物查询")
    def test_medicine_altasSearch_button(self):
        url = host + port_python + "/medicine_altas/show_durgs_altas"
        ids = self.goodId()
        allure.attach(f"内部传参：goodId={ids}")
        data = dict(goods_id=ids[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)