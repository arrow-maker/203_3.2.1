#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_wardDoctorWorkBench
@time: 
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("病区医生工作台")
class Test_WorkBench:

    @allure.title("病区的医院设置")
    @allure.story("病区首页")
    def test_getOrgInfoTreeList(self, login):
        response1, cook = login
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1, orgTypeIds="35,38", path="400,",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("病区首页-统计数据展示,核心绩效指标")
    @allure.story("病区首页")
    @pytest.mark.parametrize("groupNo,hint", (["bq01", ["在院人次", "新收人次", "出院人次", "病重(危)人次", "死亡人数", "平均住院日", "平均住院费用"]], ["bq02", ["住院死亡率", "2-31天再入院率", "药占比"]]))
    def test_getReportGroupList(self, groupNo, hint, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo=groupNo,  # 固定值
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = assert_get(url, data, cook=cook)
        for i in hint:              # 断言所有的菜单都在
            assert i in result[0]

    @allure.title("病区首页-统计范围排行")
    @allure.story("病区首页")
    @pytest.mark.parametrize("module1", (1, 2, 3, 4))
    @pytest.mark.parametrize("type1", (1, 2))
    def test_statisticsRange(self,module1,type1,login):
        response1, cook = login
        url = host + port_es + "/wardDoctorWorktable/homePage/statisticsRange.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    deptName=response1["orgName"],
                    inpatientAreaCode="",
                    startDate="2016-07-01",
                    endDate="2019-09-30",
                    statisticsModule=module1,  # 1：病种排行，2：检验排行，3：检查排行，4:药品排行
                    statisticsType=type1,  # 病种排行1：ICD4位，2：ICD3位 这里是子菜单
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = assert_get(url, data, cook)
        database1 = regular_findall(result[0], '"count":',',')
        database1 = [int(x) for x in database1]   # 元素转化为数字
        assert database1 == sorted(database1, reverse=True)  # 这里断言是倒叙

    @allure.title("病区首页-获取公告板数据")
    @allure.story("病区首页")
    def test_getNoticeBoardData(self, login):
        response1, cook = login
        url = host + port_es + "/wardDoctorWorktable/homePage/getNoticeBoardData.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    inDeptName=response1["orgName"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("通知栏更多信息")
    @allure.story("病区首页")
    def test_getNoticeBoardDataDetail(self, login):
        response1, cook = login
        url = host + port_es + "/wardDoctorWorktable/homePage/getNoticeBoardDataDetail.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    inDeptName=response1["orgName"],
                    patientInfo="",
                    startDate="2010-09-01", endDate="2019-09-30",
                    page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("警告患者列表")
    @allure.story("病区首页")
    def patientDetail(self,response1, cook):
        url = host + port_es + "/wardDoctorWorktable/homePage/getNoticeBoardDataDetail.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    inDeptName=response1["orgName"],
                    patientInfo="",
                    startDate="2010-09-01", endDate="2019-09-30",
                    page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            if len(resultdic) > 0:
                for i in resultdic:
                    patient = i["patiId"], i["patientName"]
                    ids.append(patient)
        return ids

    @allure.title("患者的全景信息")
    @allure.story("病区首页")
    def test_getFhirPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/data/getFhirPatientInfo.json"
        patient = self.patientDetail(response1, cook)
        if len(patient) > 0:
            data = dict(id=patient[0][0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, patient[0][1])

    @allure.title("病案首页的主要诊断")
    @allure.story("病区首页")
    def test_metadata(self,login):
        response1, cook = login
        url = host + port_sourcedata + "/report/metadata"
        data = dict(name="病区",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取查询的展示数据")
    @allure.story("病区首页")
    @pytest.mark.parametrize("reportNos", ("bq001,bq002,bq003,bq004,bq005,bq006,bq007", "bq008,bq009,bq010"))
    def test_getReportDatas(self, reportNos, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(timeSlice="false",
                    reportNos=reportNos,
                    indexTimeStart="2017-03-01",
                    indexTimeEnd="2019-09-30",
                    deptName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取配置信息")
    @allure.story("病区首页")
    def test_getConfig(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/reportWarning/getConfig.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    medCode="COPD-001",
                    deptName=response1["orgName"],
                    reportNo="bq004",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("也可以是统计的出院人数的详情")
    @allure.story("病区首页-点击（出院或者死亡）")
    def test_getColumnAndData(self, login):
        response1, cook = login
        url = host + port_qt + "/qtHelper/getColumnAndData.json"
        data = dict(hospitalCode=response1["hospitalCode"], deptName=response1["hospital"], queryIndexId=2004,
                    indexTime_begin="2019-11-01", indexTime_end="2019-11-30",
                    page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("患者列表")
    @allure.story("病区患者")
    def test_workbenchGroupList(self,login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/list"
        data = dict(path=75635,
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取队列消息")
    @allure.story("病区患者")
    def test_getColumnAndData1(self, login):
        response1, cook = login
        url = host + port_qt + "/qtHelper/getColumnAndData.json"
        data = dict(queryIndexId=2005,
                    hospitalCode=response1["hospitalCode"],
                    deptName=response1["orgName"],
                    iTime_begin="2017-01-01",
                    iTime_end="2019-12-31",
                    ageStart="", ageEnd="", sex="", severity="", cgroupId="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取队列消息2")
    @allure.story("病区患者")
    def test_getReportDatas2(self,login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(reportNos="bq038",
                    hospitalCode=response1["hospitalCode"],
                    deptName=response1["orgName"],
                    iTime_begin="2019-01-01",
                    ageStart="", ageEnd="", severity="", cgroupId="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("病种结构分析 数据列表")
    @allure.story("病种分析")
    def test_getDiseaseAnalysisList(self, login):
        response1, cook = login
        url = host + port_es + "/wardDoctorWorktable/workTableData/getDiseaseAnalysisList.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    deptName=response1["orgName"],
                    indexTime_begin="2019-01-01", indexTime_end="2019-12-31",
                    topN=20, statisticsType=1,
                    page=1, size=5,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data,  cook)

    @allure.title("病种列表")
    @allure.story("病种分析")
    def test_deseaseList(self, login):
        response1, cook = login
        url = host + port_es + "/wardDoctorWorktable/warkDoctor/deseaseList.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    deptName=response1["orgName"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("病种排名")
    @allure.story("病种分析")
    def test_getReportDatas3(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    indexTimeStart="2019-01-01", indexTimeEnd="2019-12-31",
                    topN=20, reportNos="bq011",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("病种共病排名")
    @allure.story("病种分析")
    def test_getReportDatas4(self,login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    medCode="icd4", topN=20, reportNos="bq012",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("病区工作量-数据展示")
    @allure.story("医生工作量")
    def test_qualityControl_getReportGroupList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo="bq04",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("医生工作量-指标下拉框")
    @allure.story("医生工作量")
    def test_qualityControl_getReportDatas(self,login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(timeSlice="false",
                    reportNos="bq013,bq014,bq015",
                    indexTimeStart="2019-01-01", indexTimeEnd="2019-12-31",
                    deptName=response1["orgName"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("医生工作量列表")
    @allure.story("医生工作量")
    def test_getDoctorsWorkloadList(self, login):
        response1, cook = login
        url = host + port_es + "/wardDoctorWorktable/workTableData/getDoctorsWorkloadList.json"
        data = dict(
            page=1, size=10,
            queryIndexId=2006, indexTime_begin="2017-01-01", indexTime_end="2019-12-31",
            hospitalCode=response1["hospitalCode"],
            deptName=response1["orgName"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("单诊疗组 -菜单")
    @allure.story("诊疗组管理")
    def test_getGroupInfoList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getGroupInfoList.json"
        data = dict(groupType="病区-单诊疗组",
                    multiCenter=0,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("单诊疗组-工作量指标-详细数据")
    @allure.story("诊疗组管理")
    @pytest.mark.parametrize("groupNo", ("bq05", "bq06", "bq07", "bq08"))
    def test_getReportGroupList3(self, groupNo, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo=groupNo,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("单诊疗组-工作量指标-工作台分组二")
    @allure.story("诊疗组管理")
    def test_workbenchGroupList2(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/workbench/group/list"
        data = dict(path=75635,
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("单诊疗组-工作量指标-报告数据")
    @allure.story("诊疗组管理")
    @pytest.mark.parametrize("reportNos", ("bq016,bq017", "bq018,bq019,bq020,bq021,bq022"))
    @allure.step("参数：reportNos={0}")
    def test_getReportDatas5(self, reportNos, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        data = dict(hospitalCode=response1["hospitalCode"], timeSlice="false", reportNos=reportNos,
                    indexTimeStart="2019-01-01", indexTimeEnd="2019-12-31", deptName=response1["orgName"], cgroupId="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)


if __name__ == '__main__':
    pytest.main(["-v", "--reruns=5"])
