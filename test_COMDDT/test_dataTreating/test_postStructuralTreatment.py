#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: test_postStructuralTreatment.py
@time: 2019/10/8 16:04
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("后结构化处理")
class Test_postSturalTreatMent:

    @allure.story("数据处理检索")
    @allure.step("参数：login={0}")
    def test_getPatientInfoPage(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/structuring/tool/getPatientInfoPage.json"
        data = dict(key="",
                    page=1, size=25,
                    startDate="", endDate="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.story("数据验证检索")
    @allure.step("参数：login={0}")
    def test_getStructuringPatientList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/structuring/tool/getStructuringPatientList.json"
        data = dict(
            project=1, type=1, status="-1", key="", startDate="", endDate="",
            page=1, size=10,
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.story("数据展示检索")
    @allure.step("参数：login={0}")
    def test_getValidatePatientInfoPage(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/structuring/tool/getValidatePatientInfoPage.json"
        data = dict(key="",
                    page=1, size=10,
                    startDate="2018-10-08", endDate="2019-10-08",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("以后结构化患者")
    @allure.story("结果统计")
    @allure.step("参数：login={0}")
    def test_getStructuredReport(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/structuredReport/getStructuredReport.json"
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = assert_get(url, data, cook)
        hint = ("现病史", "个人史", "肺功能", "鼻窦CT检查", "泌尿系B超检查")
        for i in hint:
            assert i in result[0]

    # @allure.title("入院记录-现病史(稳定期,加重期)")
    # @allure.story("结果统计")
    # @pytest.mark.skip("这个版本没有后结构化处理")
    # @pytest.mark.parametrize("type", (1, 2))
    # def test_getXbsReport(self, type, login):
    #     response1, cook = login
    #     url = host + port_sourcedata + "/structuredReport/getXbsReport.json"
    #     data = dict(type=type,
    #                 authUserId=response1["authUserId"], authToken=response1["authToken"])
    #     assert_get_hint(url, data, cook, "咳嗽")

    @allure.title("鼻窦CT")
    @allure.story("结果统计")
    @allure.step("参数：login={0}")
    def test_getReportDatas(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/structuredReport/getCtCheckReport.json"
        data = dict(
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("肺功能-肺通气功能障碍程度")
    @allure.story("结果统计")
    @pytest.mark.parametrize("reportno", (70006, 50004, 50003, 50009))
    def test_getReportDatas(self, reportno, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(reportNos=reportno,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "查询操作成功")

    @allure.title("泌尿系B超")
    @allure.story("结果统计")
    @allure.step("参数：login={0}")
    def test_getBCheckReport(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/structuredReport/getBCheckReport.json"
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)
