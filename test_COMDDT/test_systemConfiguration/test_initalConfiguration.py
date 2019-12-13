#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_initalConfiguration.py
@time: 2019/9/16  13:48
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("临床辅助决策系统-患者相似性度量")
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
        # 修改codes
        data = dict(codes="	verification_code_login,password_expired,password_expired_time,"
                          "password_expired_time_unit,login_error_time,login_error_num,"
                          "singleton_login,ip_interrupt,initial_password",              # 这里是固定的
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "password_expired")

    @allure.title("这里是修改系统设置")
    @allure.story("页面加载信息")
    def test_updataParam(self):
        url = host + portlogin + "/param/updateParam.json"
        data = dict(paramType="system",         # 这里是系统设置
                    code="password_expired,",   # 这里是修改的类型，这个是密码过期策略，login_error_num：密码错误次数，singleton_login：单点登录设置
                    value=1,                    # 这里是修改的值
                    operatorFunction="51042-saveSafeSetting",   # 这里是安全设置
                    operatorId=self.authUserId,authUserId=self.authUserId,authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("显示安全设置")
    @allure.story("科研设置")
    def test_getParamByCode_two(self):
        url = host + portlogin + "/param/getParamByCode.json"
        # 修改codes
        data = dict(codes="hospital_logo,project_name,plat_user_type"
                          "singleton_login,ip_interrupt,initial_password",              # 这里是固定的
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "hospital_logo")


if __name__ == '__main__':
    pytest.main()