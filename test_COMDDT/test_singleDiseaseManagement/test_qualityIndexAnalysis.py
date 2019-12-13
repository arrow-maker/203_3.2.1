#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_qualityIndexAnalysis.py
@time: 2019/9/19  10:21
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("质控指标分析")
class Test_qualityIndexAnalysis:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]
        self.itemOrgId = response1["responseData"]["itemOrgId"]

    @allure.title("指标预填 - 获取间隔周期")
    @allure.story("首次加载的接口加载")
    def test_getInterval(self):
        url = host + port_sourcedata + "/reportWarning/getInterval.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "指标预填")

    @allure.title("顶部的选择医院")
    @allure.story("首次加载的接口加载")
    def test_getHospitalList(self, dlogin):
        url = host + portlogin + "/platform/hospital/getHospitalList.json"
        header = {"cookie": dlogin}
        data = dict(orgTypeId=38, authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, headers=header)

    @allure.title("显示可选菜单")
    @allure.story("首次加载的接口加载")
    def test_getGroupInfoList(self):
        url = host + port_sourcedata + "/quality/control/getGroupInfoList.json"
        data = dict(multiCenter=0, groupType="质量控制",
                    medCode="COPD-001", authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "质量控制")

    @allure.title("显示图表的固定的信息")
    @allure.story("首次加载的接口加载")
    def test_getReportItemList(self):
        url = host + port_sourcedata + "/quality/control/getReportItemList.json"
        data = dict(multiCenter=0, groupType="质量控制", orgUserId=self.authUserId, medCode="COPD-001",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("获取报告分组")
    @allure.story("首次加载的接口加载")
    def test_getReportGroup(self):
        url = host + port_sourcedata + "/quality/control/getReportGroup.json"
        data = dict(multiCenter=0, medCode="COPD-001",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("质控首页 上面的最后的更新时间")
    @allure.story("首次加载的接口加载")
    def test_metadata(self):
        url = host + port_sourcedata + "/report/metadata"
        data = dict(name="质量控制",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "质量控制")

    @allure.title("顶部的 预警信息")
    @allure.story("首次加载的接口加载")
    def test_findRecord(self):
        url = host + port_sourcedata + "/reportWarning/findRecord.json"
        data = dict(hospitalCode=self.hospitalCode, medCode="COPD-001",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, self.hospitalCode)

    @allure.title("查看预警详情")
    @allure.story("首次加载的接口加载")
    def test_getReportData(self):
        url = host + port_sourcedata + "/quality/control/getReportData.json"
        data = dict(hospitalCode=self.hospitalCode, reportNo=21003, timeSlice="月",
                    indexTimeStart="2019-01-01", indexTimeEnd="2019-09-14",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("设置 - 预警值设置 - 选择质控指标类型")
    @allure.story("首次加载的接口加载")
    def test_findGroup(self):
        url = host + port_sourcedata + "/reportWarning/findGroup.json"
        data = dict(medCode="COPD-001",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title(" 设置  质控预警值的上下限 安全指标的图像展示")
    @allure.story("首次加载的接口加载")
    def test_findConfig(self):
        url = host + port_sourcedata + "/reportWarning/findConfig.json"
        data = dict(hospitalCode=self.hospitalCode, medCode="COPD-001",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, self.hospitalCode)

    @allure.title("设置 数据 刷新频率")
    @allure.story("首次加载的接口加载")
    def test_changeInterval(self):
        url = host + port_sourcedata + "/reportWarning/changeInterval.json"
        data = dict(value=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("获取报告分组列表")
    @allure.story("首次加载的接口加载")
    def test_getReportGroupList(self):
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo="01", multiCenter=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("质控首页的数据展示，合理用药指标展示，患者基础指标")
    @allure.story("首次加载的接口加载")
    def test_getReportDatas(self):
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(hospitalCode=self.hospitalCode, slave="true",
                    reportNos="01001,01002,01004,01005,01006,01003,02001,02002,05001,05005",
                    timeSlice="月", indexTimeStart="2019-09-01", indexTimeEnd="2019-09-30",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "01004")


if __name__ == '__main__':
    pytest.main()
