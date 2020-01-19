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
    @pytest.mark.parametrize("slice,start,end", (("年", "2019-01-01", "2019-12-31"), ("年", "2018-01-01", "2018-12-31"),
                                                 ("季", "2018-01-01", "2019-3-30"),
                                                 ("半年", "2019-01-01", "2019-06-30"), ("月", "2019-04-01", "2019-04-30")))
    def test_getReportData(self, slice, start, end):
        url = host + port_sourcedata + "/quality/control/getReportData.json"
        data = dict(hospitalCode=self.hospitalCode, reportNo=21003, timeSlice=slice,
                    indexTimeStart=start, indexTimeEnd=end,
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
    @pytest.mark.parametrize("groupNos, hint", (("01", "2-31天再入院率"), ("02", "COPD药占比"), ("03", "入院途径分析"),
                                               ("04", "平均住院日分析"), ("05", "入住ICU率")))
    def test_getReportGroupList(self, groupNos, hint):
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo=groupNos, multiCenter=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint)

    data1234 = congyaml["质控首页_患者基本指标"]
    @allure.title("质控首页的数据展示，合理用药指标展示，患者基础指标")
    @allure.story("首次加载的接口加载")
    @pytest.mark.parametrize("reportNos,hint", data1234 +
                             [pytest.param('01006,01003', "肺功能检查率", marks=pytest.mark.xfail)])
    @pytest.mark.parametrize("slice,start,end", (("年", "2019-01-01", "2019-12-31"), ("年", "2018-01-01", "2018-12-31"),
                                                 ("季", "2018-01-01", "2019-3-30"),
                                                 ("半年", "2019-01-01", "2019-06-30"), ("月", "2019-04-01", "2019-04-30")))
    def test_getReportDatas(self, reportNos, hint, slice, start, end):
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(hospitalCode=self.hospitalCode, slave="true",
                    reportNos=reportNos,
                    timeSlice=slice, indexTimeStart=start, indexTimeEnd=end,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint)


if __name__ == '__main__':
    pytest.main()
