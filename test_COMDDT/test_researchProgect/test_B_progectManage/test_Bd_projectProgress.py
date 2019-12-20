# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_Bd_projectProgress.py
    Time:    2019/12/19 9:29
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *
projectId = []        # 项目进度中的项目的Id


@allure.feature("科研项目管理->项目进度")
class Test_projectprogress:

    @classmethod
    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.title("可选的项目")
    @allure.story("项目进度-默认展示")
    def test_listByCenter(self):
        url = host + port_project + "/project/listByCenter.json"
        data = {
            "operatorId": self.authUserId,
            "checkType": 2,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        global projectId
        for i in result[1]["responseData"]["content"]:
            projectId.append(i["PROJECT_ID"])

    @allure.title("项目的基础的信息")
    @allure.story("项目进度-分组入组展示")
    def test_projectInfoBase(self):
        url = host + port_project + "/project/info/base.json"
        data = {
            "projectId": projectId[0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("项目中心返回结果")
    @allure.story("项目进度-分组入组展示")
    def test_resultCenterList(self):
        url = host + port_project + "/project/result/center/info/list.json"
        data = dict(parentProjectId=projectId[0], operatorId=self.authUserId, projectStage=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("项目分组入组情况")
    @allure.story("项目进度-分组入组展示")
    def test_resultprojectGroup(self):
        url = host + port_project + "/project/report/group.json"
        data = dict(projectId=projectId[0], createUserId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("病例研究情况")
    @allure.story("项目进度-受试者研究进度")
    def test_resultCaseResearch(self):
        url = host + port_project + "/project/report/caseResearch.json"
        data = dict(projectId=projectId[0], createUserId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("实验组数据")
    @allure.story("项目进度-受试者访视进度")
    def test_resultCaseFollowUp(self):
        url = host + port_project + "/project/report/caseFollowUp.json"
        data = dict(projectId=projectId[0], createUserId=self.authUserId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("项目输入信息")
    @allure.story("项目进度-中期/结题汇报")
    @pytest.mark.parametrize("stage", (1, 2))
    def test_resultInfo(self, stage):
        url = host + port_project + "/project/result/info.json"
        data = dict(projectId=projectId[1], operatorId=self.authUserId, projectStage=stage,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("项目配置信息")
    @allure.story("项目进度-中期/结题汇报")
    @pytest.mark.parametrize("stage", (1, 2))
    def test_resultPaymentList(self, stage):
        url = host + port_project + "/project/result/paymentList.json"
        data = dict(projectId=projectId[1], operatorId=self.authUserId, projectStage=stage,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("时间轴信息")
    @allure.story("项目进度-中期/结题汇报")
    @pytest.mark.parametrize("stage", (1, 2))
    def test_resultTimelineList(self, stage):
        url = host + port_project + "/project/result/timelineList.json"
        data = dict(projectId=projectId[1], operatorId=self.authUserId, projectStage=stage,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("分中心信息")
    @allure.story("项目进度-中期/结题汇报")
    @pytest.mark.parametrize("stage", (1, 2))
    def test_resultCenterProgressList(self, stage):
        url = host + port_project + "/project/result/center/progress/list.json"
        data = dict(projectId=projectId[1], operatorId=self.authUserId, projectStage=stage,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("不良事件信息")
    @allure.story("项目进度-中期/结题汇报")
    @pytest.mark.parametrize("stage", (1, 2))
    def test_findProejctEventStatistics(self, stage):
        url = host + port_project + "/project/event/findProejctEventStatistics.json"
        data = dict(projectId=projectId[1],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)


if __name__ == '__main__':
    pytest.main()