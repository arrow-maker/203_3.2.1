#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_initalConfiguration.py
@time: 2019/9/16  13:48
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("初始化配置")
class Test_initalConfiguration:

    @classmethod
    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code

    @allure.title("显示安全设置")
    @allure.story("页面加载信息")
    def test_getParamByCode(self):
        url = host + portlogin + "/param/getParamByCode.json"
        yamdata = congyaml["初始化配置"]["安全设置"]
        data = dict(codes=yamdata["codes"],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "password_expired")

    @allure.title("这里是修改系统设置")
    @allure.story("页面加载信息")
    @pytest.mark.parametrize("code", ("login_error_num", "singleton_login", "password_expired"))
    @pytest.mark.parametrize("values", (1, 0))
    def test_updataParam(self, code, values):
        """
        :param code:    这个是密码过期策略，login_error_num：密码错误次数，singleton_login：单点登录设置"password_expired,
        :param values:  这个是开启和关闭
        :return:
        """
        url = host + portlogin + "/param/updateParam.json"
        data = dict(paramType="system",
                    code=code,
                    value=values,
                    operatorFunction="51042-saveSafeSetting",
                    operatorId=self.authUserId,authUserId=self.authUserId,authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("显示安全设置")
    @allure.story("科研设置")
    def test_getParamByCode_two(self):
        url = host + portlogin + "/param/getParamByCode.json"
        data = dict(codes="hospital_logo,project_name,plat_user_type"
                          "singleton_login,ip_interrupt,initial_password",              # 这里是固定的
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "hospital_logo")


if __name__ == '__main__':
    pytest.main()