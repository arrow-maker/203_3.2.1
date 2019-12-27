# -*- coding: utf-8 -*-
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("不良事件")
class Test_badnessEvent:

    def setup_class(self):
        self.response, self.cook = login_cookies()
        self.authUserId = self.response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = self.response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = self.response["responseData"]["userName"]
        self.orgId = self.response["responseData"]["roleList"][0]["orgId"]
        self.hospital = self.response["responseData"]["roleList"][0]["orgName"]  # 获取医院的名字
        self.mobile = self.response["responseData"]["mobileTelephone"]

    @allure.story("不良事件展示列表")
    def test_reportList(self):
        url = host + port_project + "/project/event/findGroupList.json"
        data = {
            "keyword": "",
            "projectName": "",
            "category": "",
            "severity2": "",
            "saeOutcome": "",
            "patientName": "",
            "reportName": "",
            "operatorId": self.authUserId,
            "page": 1,
            "size": 10,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)


if __name__ == '__main__':
    pytest.main(
        [r"-v -q test_Bc_badnessEvent.py"])
