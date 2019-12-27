#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: test_pulmonaryTrendAnalysis.py
@time: 2019/10/15 16:48
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("肺功能趋势分析")
class Test_pulmonaryTrendAnalysis:

    @allure.title("组织架构-列表")
    @allure.step("参数：login={0}")
    def test_getOrgInfoTreeList(self, login):
        response1, cook = login
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1,
                    orgTypeIds="33,35,38",
                    path=400, orgName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("患者列表")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_search(self, login, orgPath, start, end):
        response1, cook = login
        url = host + port_dataindex + "/patient/search.json"
        data = dict(
            page=1, size=10, orgPath=orgPath,
            orgType=35,  # 变动的数据
            orgId=response1['orgId'], searchWord="", sourceType=2,
            sourceRecord="", indexTimeBegin=start, indexTimeEnd=end,
            visitDateBegin="", visitDateEnd="", followUpDateBegin="",
            followUpDateEnd="", diseaseType=1, diseaseName="",
            sourceDataType=3, neSourceDataType="",
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def patild(self, response1, cook, orgPath):
        url = host + port_dataindex + "/patient/search.json"
        data = dict(
            page=1, size=10, orgPath=orgPath,
            orgType=35, orgId=response1['orgId'], searchWord= "", sourceType=2,
            sourceRecord="", indexTimeBegin="", indexTimeEnd="",
            visitDateBegin="", visitDateEnd="", followUpDateBegin="",
            followUpDateEnd="", diseaseType=1, diseaseName="",
            sourceDataType=3, neSourceDataType="",
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["patiId"])
        return ids

    @allure.title("患者的详细信息")
    def test_getOne(self, login, orgPath):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/getOne.json"
        path = self.patild(response1, cook, orgPath)
        allure.attach(f"内部参数：path={path}")
        data = dict(uniquNo=path[0],
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取fhirId")
    @allure.story("患者病例")
    def test_getFhirPatientInfo(self, login, orgPath):
        response1, cook = login
        url = host + port_es + "/data/getFhirPatientIds.json"
        path = self.patild(response1, cook, orgPath)
        allure.attach(f"内部参数： path={path}")
        data = dict(id=path[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("报告详情-报告列表")
    @allure.story("肺功能检查")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getExamReportMasterAssistMaster(self, login, orgPath, start, end):
        response1, cook = login
        url = host + port_es + "/panorama/data/getExamReportMasterAssistMaster.json"
        path = self.patild(response1, cook, orgPath)
        allure.attach(f"内部参数： path={path}")
        data = dict(reportName="examReportMaster",
                    id=path[0],
                    startDate=start, endDate=end,
                    page=1, size=10, sort="desc",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def fhirList(self, response1, cook, orgPath):
        url = host + port_es + "/panorama/data/getExamReportMasterAssistMaster.json"
        path = self.patild(response1, cook, orgPath)
        allure.attach(f"内部参数：path={path}")
        data = dict(reportName="examReportMaster",
                    id=path[0],
                    startDate="", endDate="",
                    page=1, size=10, sort="desc",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            if len(resultdic) > 0:
                for i in resultdic:
                    if len(i["mapList"]) > 0:
                        for k in i["mapList"]:
                            ids.append((k["reportId"], k["reportType"]))
        return ids

    @allure.title("报告详情-报告列表-详情")
    @allure.story("肺功能检查")
    def test_getExamReportDetailPageAssistDetail(self, login, orgPath):
        response1, cook = login
        url = host + port_es + "/data/getExamReportDetailPageAssistDetail.json"
        ids = self.fhirList(response1, cook, orgPath)
        allure.attach(f"内部参数：ids={ids}")
        for i in ids:
            data = dict(reportName="examReportDetail",
                        reportId=i[0][0],
                        reportType=i[0][1],
                        hospitalCode=response1["hospitalCode"],
                        page=1, size=10,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook)

    @allure.title("指标类型")
    @allure.story("趋势分析")
    def test_getReportTempList(self, login):
        response1, cook = login
        url = host + port_es + "/data/getReportTempList.json"
        data = dict(type=2,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("指标筛选")
    @allure.story("趋势分析")
    def test_getReportTempDetailList(self, login):
        response1, cook = login
        url = host + port_es + "/data/getReportTempDetailList.json"
        data = dict(id=8, name="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("查看患者基本信息")
    @allure.story("趋势分析")
    def test_getPatientInfo(self, login, orgPath):
        response1, cook = login
        url = host + port_es + "/panorama/data/getPatientInfo.json"
        path = self.patild(response1, cook, orgPath)
        allure.attach(f"内部参数： path={path}")
        data = dict(patiId=path[0],
                    hospitalCode="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)
