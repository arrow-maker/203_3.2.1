# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_medicineKG.py
    Time:    2019/12/10 10:10
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *
goodsList = ["100286"]              # 药物的Id

@allure.feature("智医AKSO")
class Test_drug:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]

    @allure.title("药物分类")
    @allure.severity(A3)
    @allure.story("药物查询")
    def test_Default(self):
        url = host + port_python + "/medicine_altas/default"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("药物查询")
    @allure.severity(A2)
    @allure.story("药物查询")
    def test_Search_button(self):
        url = host + port_python + "/medicine_altas/search_button"
        data = dict(ywmc="", blfy="", syz="", jjz="", yplb="",
                    yytj="", scs="", cf="", pzwh="", page=1, size=200,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        global goodsList
        for i in result[1]["resultData"]["drugList"]:
            goodsList.append(i["商品ID"])

    @allure.title("药物使用说明")
    @allure.severity(A4)
    @allure.story("药物查询")
    def test_drug_instruction(self):
        url = host + port_python + "/medicine_altas/drug_instruction"
        allure.attach(f"内部传参：goodId={goodsList}")
        data = dict(default=1, goods_id=goodsList[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("药物图谱")
    @allure.severity(A3)
    @allure.story("药物查询")
    @pytest.mark.parametrize("goodIds", ("100005", "100005,100010", "100005,100010,100052,100305",
                                         pytest.param(goodsList[0])), ids=["查询一种药物", "查询两种药物", "查询多种药物", "动态添加参数"])
    def test_show_durgs_altas(self, goodIds):
        url = host + port_python + "/medicine_altas/show_durgs_altas"
        allure.attach(f"内部传参：goodId={goodsList}")
        data = dict(goods_id=goodIds,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)



if __name__ == '__main__':
    pytest.main()