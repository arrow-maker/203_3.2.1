#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_menuFeatures.py
@time: 2019/9/19  9:41
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("菜单管理")
class Test_menuFeatures:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.story("菜单列表的显示")
    def test_getMenuTreeList(self):
        url = host + portlogin + "/auth/menu/getMenuTreeList.json"
        data = dict(type=2, groupName="", operatorFunction="51052-getMenu",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def transfer_getMenuTreeList(self):
        url = host + portlogin + "/auth/menu/getMenuTreeList.json"
        data = dict(type=2, groupName="", operatorFunction="51052-getMenu",
                    operatorId=self.authUserId, authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)



if __name__ == '__main__':
    pytest.main()