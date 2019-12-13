#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_panorama.py
@time: 2019/9/4  11:16
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("临床科研一体化- 患者全景")
class Test_patientPanorama:

    @allure.title("医院和科室 列表")
    @allure.step("参数：login={0}")
    def test_getOrgInfoTreeList(self, login):
        response1, cook = login
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1,
                    orgTypeIds="33,35,38",
                    path=400, orgName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_treeList(self, response1, cook):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = dict(listType=2, status=1,
                    orgTypeIds="33,35,38",
                    path=400, orgName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        dicdata = {"orgPath": [], "orgId": [], "orgType": []}
        if "SUCCESS" in result.text:
            # 这里是广医的数据
            resultDic = json.loads(result.text)["responseData"][0]["children"][0]["children"]
            if len(resultDic) > 0:
                for i in resultDic:
                    dicdata["orgPath"].append(i["path"])
                    dicdata["orgId"].append(i["id"])
                    if "orgTypeId" in i.keys():
                        dicdata["orgType"].append(i["orgTypeId"])
                    else:
                        dicdata["orgType"].append(0)
        return dicdata

    @allure.title("查询患者列表")
    @allure.step("参数：login={0}")
    def test_search(self, login):
        response1, cook = login
        url = host + port_dataindex + "/patient/case/inp.json"
        data = dict(
            searchWord="", page=1, size=10,
            operatorId=response1["authUserId"], orgPath=f'400,{response1["itemOrgId"]}',
            orgType=35, orgId=response1["orgId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"]
        )
        assert_get(url, data, cook)

    def transfer_patientList(self, response1, cook):
        url = host + port_dataindex + "/patient/case/inp.json"
        data = dict(
            searchWord="", page=1, size=10,
            operatorId=response1["authUserId"], orgPath=f'400,{response1["itemOrgId"]}',
            orgType=35, orgId=response1["orgId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"]
        )
        result = requests.get(url, data, cookies=cook)  # 这里没有cookies值也可以成功
        resultDic = json.loads(result.text)["responseData"]["content"]
        datadic = {"id": [], "patientId": []}
        if len(resultDic) > 0:
            for i in resultDic:
                datadic["id"].append(i["patiId"])
                datadic["patientId"].append(i["fhirPatientId"])
        return datadic

    @allure.title("顶行的数据展示")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getFhirPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/data/getFhirPatientInfo.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部断言：id={ids}")
        data = dict(id=ids[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("在fhir中获取患者的ids")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getFhirPantientIds(self, login):
        response1, cook = login
        url = host + port_es + "/data/getFhirPatientIds.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：id={ids}")
        data = dict(id=ids[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data,cook)

    @allure.title("获取仓库患者门诊住院统计信息")
    @allure.story("首页数据的显示")
    @pytest.mark.parametrize("sourceType", ("clinical", "project"))
    def test_wareHousePatientDataList(self, login, sourceType):
        response1, cook = login
        ids = self.transfer_patientList(response1, cook)
        patientId = ids["patientId"]
        patiId = ids["id"]
        allure.attach(f"内部参数：ids={ids}")
        url = host + port_es + f"/panorama/data/homePage/{patientId[0]}/warehousePatientDataList.json"
        data = dict(startDate="2019-01-01", endDate="2019-12-31", sourceType=sourceType,
                    patiId=patiId[0],
                    authToken=response1["authToken"], authUserId=response1["authUserId"])
        assert_get(url, data, cook)

    @allure.title("获取project列表")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_projectList123(self, login):
        response1, cook = login
        patientId = self.transfer_patientList(response1, cook)["patientId"]
        allure.attach(f"内部参数：patientId={patientId}")
        url = host + portlogin + f"/warehouse/patient/{patientId[0]}/projectList.json"
        assert_get(url, {}, cook)

    @allure.title("访视次数")
    @allure.story("首页数据的显示")
    @pytest.mark.parametrize("sourceType", ("clinical", "project"))
    def test_visitList(self, login, sourceType):
        response1, cook = login
        url = host + port_es + "/panorama/data/visitList.json"
        ids = self.transfer_patientList(response1, cook)
        patientId = ids["patientId"]
        patiId = ids["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patientId=patientId[0],
                    sourceType=sourceType, patiId=patiId[0],
                    authToken=response1["authToken"], authUserId=response1["authUserId"])
        assert_get(url, data, cook)

    @allure.title("最后一次指标预警操作")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_warnIndicatorList(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/warnIndicatorList.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取住院时间")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_warnIndicatorList(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getHospitalizationTime.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("查询主要诊断比率数据")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getMainDiagRatio(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getMainDiagRatio.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    startDate="2014-09-05", endDate="2019-09-04",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "查询门诊和住院主要诊断比率数据操作成功")

    @allure.title("查询门诊和住院主要诊断类型的比率数据操作")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getMainDiagTypeRatio(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getMainDiagTypeRatio.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    startDate="2014-09-05", endDate="2019-09-04",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "查询门诊和住院主要诊断类型的比率数据操作成功")

    @allure.title("查询住院费用和天数据操作")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getTotalCosts(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getTotalCosts.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    startDate="2014-09-05", endDate="2019-09-04",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "查询住院费用和天数据操作成功")

    @allure.title("仓库患者详情")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_warehousePatientDataList(self, login):
        response1, cook = login
        ids = self.transfer_patientList(response1, cook)
        patientId = ids["patientId"]
        url = host + port_es + f"/panorama/data/homePage/{patientId}/warehousePatientDataList.json"
        patiId = ids["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=patiId[0],
                    startDate="2014-09-05", endDate="2019-09-04",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("查询时间轴数据【住院诊断，门诊诊断，吸烟，临床主要诊断，胸部影像学】数据操作")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getTimeAxisList(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getTimeAxisList.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    startDate="2019-09-01", endDate="2019-09-30",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data,  cook, "查询时间轴数据【住院诊断，门诊诊断，吸烟，临床主要诊断，胸部影像学】数据操作成功")

    @allure.title("查询检验预警指标趋势分析数据操作")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_eosinophilCountList(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/eosinophilCountList.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    testItem="嗜酸性粒细胞数", itemCode="",
                    startDate="2018-09-01", endDate="2019-12-30",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "查询检验预警指标趋势分析数据操作成功")

    @allure.title("查询访视，门诊，住院的统计数量操作")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_getStatisticsCount(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getStatisticsCount.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    hospitalCode="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"]
                    )
        assert_get(url, data, cook, ids[0])

    @allure.title("访视页数的列表展示")
    @allure.story("首页数据的显示")
    @allure.step("参数：login={0}")
    def test_visitPageList(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/visitPageList.json"
        ids = self.transfer_patientList(response1, cook)
        patientId = ids["patientId"]
        patiId = ids["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=patiId[0], patientId=patientId[0],
                    startDate="2019-09-01", endDate="2019-09-30",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("全部的访视列表")
    @allure.story("对访视的操作")
    @allure.step("参数：login={0}")
    def test_zhpbgList(self, login):
        response1, cook = login
        url = host + portlogin + "/warehouse/zhpgbg/list.json"
        patientId = self.transfer_patientList(response1, cook)["patientId"]
        allure.attach(f"内部参数：patientId={patientId}")
        data = dict(patientId=f"Patient/{patientId[0]}",
                    start="", end="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取版权信息")
    @allure.story("对访视的操作")
    @allure.step("参数：login={0}")
    def test_printPageFindList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/print/page/findList.json"
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("获取值")
    @allure.story("门诊信息页面操作")
    @allure.step("参数：login={0}")
    def test_getValue(self, login):
        response1, cook = login
        url = host + portlogin + "/param/getValue.json"
        data = dict(code="show_iconography_data",  # 这里是固定的格式
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("显示页面的门诊的信息")
    @allure.story("门诊信息页面操作")
    @allure.step("参数：login={0}")
    def test_getClinicDiagnosisAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/data/getClinicDiagnosisAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(reportName="clinicDiagnosis",  # 这里是固定的格式
                    id=ids[0],
                    startDate="", endDate="",
                    page=1, size=20,  # 这里没有可选的页数的按钮
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("这里是主要的展示")
    @allure.story("门诊信息页面操作")
    def transfer_outPatientNo(self, response1, cook):
        url = host + port_es + "/data/getClinicDiagnosisAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = dict(reportName="clinicDiagnosis",  # 这里是固定的格式
                    id=ids[0],
                    startDate="", endDate="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)  # 没有cookies值
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicdata = {"outPatientNo": []}
        if len(resultDic) > 0:
            for i in resultDic:
                dicdata["outPatientNo"].append(i["outpPatientNo"])
        return dicdata

    # @allure.title("次要的信息 门诊诊断信息 医嘱上面的信息")
    # @allure.story("门诊信息页面操作")
    # @pytest.mark.skip("这个版本没有这个功能")
    # def test_getClinicDiagnosisAssisDetail(self, login):
    #     response1, cook = login
    #     url = host + port_es + "/data/getClinicDiagnosisAssistDetail.json"
    #     outPatientNo = self.transfer_outPatientNo(response1, cook)["outPatientNo"]
    #     data = dict(reportName="clinicDiagnosis", patientNo="null",
    #                 outPatientNo=outPatientNo[0], hospitalCode=response1["hospitalCode"],
    #                 authUserId=response1["authUserId"], authToken=response1["authToken"])
    #     assert_get(url, data, cook)

    # @allure.title("门诊信息中的医嘱列表信息")
    # @allure.story("门诊信息页面操作")
    # @pytest.mark.skip("这个版本没有这个功能")
    # def test_getClinicOradersDetailAssisDetail(self, login):
    #     response1, cook = login
    #     url = host + port_es + "/data/getClinicOrdersDetailAssistDetail.json"
    #     outPatientNo = self.transfer_outPatientNo(response1, cook)["outPatientNo"]
    #     data = dict(reportName="clinicOrdersDetail", outPatientNo=outPatientNo[0],
    #                 # page=1, size=10,                # 这里的页数可以修改该10的整数倍
    #                 hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"],
    #                 authToken=response1["authToken"])
    #     overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证10")

    # @allure.title("全部案例首页列表")
    # @allure.story("住院信息-病案首页")
    # @pytest.mark.skip("这个版本没有这个接口")
    # def test_getInpmrFrontSheetAssistMaster(self, dlogin, login):
    #     response1, cook = login
    #     url = host + port_es + "/panorama/data/getInpMrFrontSheetAssistMaster.json"
    #     ids = self.transfer_patientList(response1, cook)["id"]
    #     header = {"cookie": dlogin}
    #     data = {
    #         "id": ids[0],
    #         "startDate": "",
    #         "endDate": "",
    #         "page": 1,
    #         "size": 10,  # 这里是固定的格式
    #         "authUserId": response1["authUserId"],
    #         "authToken": response1["authToken"]
    #     }
    #     assert_get_header(url, data, header)

    def transfer_front_assistMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getInpMrFrontSheetAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里是固定的格式
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultDic = json.loads(result.text)["responseData"]["content"]
            for i in resultDic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        else:  # 这里没有就给一个固定的值
            dicdata["inpatientNo"].append("ZY090000619374")
        return dicdata

    @allure.title("病案首页-详细信息")
    @allure.story("住院信息-病案首页")
    @allure.step("参数：login={0}")
    def test_getInpMrFrontSheetById(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getInpMrFrontSheetById.json"
        inpatientNo = self.transfer_front_assistMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = {
            "reportName": "inpMrFrontSheet",  # 固定格式
            "inpatientNo": inpatientNo[0],
            "hospitalCode": response1["hospitalCode"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, inpatientNo[0])

    @allure.title("入院记录列表")
    @allure.story("住院信息-入院记录")
    @allure.step("参数：login={0}")
    def test_getAdmissionMrAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getAdmissionMrAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_admission_assionMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getAdmissionMrAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("入院信息详情")
    @allure.story("住院信息-入院记录")
    @allure.step("参数：login={0}")
    def test_getAdminssionMrAssisDetail(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getAdmissionMrAssistDetail.json"
        inpatientNo = self.transfer_admission_assionMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = {
                "reportName": "admissionMr",
                "inpatientNo": inpatientNo[0],
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_get(url, data, cook, inpatientNo[0])

    @allure.title("出院记录列表")
    @allure.story("住院信息-出院记录")
    @allure.step("参数：login={0}")
    def test_getDischgedMrAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getDischgedMrAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_dischged_assionMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getDischgedMrAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                print(i)
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("出院信息详情")
    @allure.story("住院信息-出院记录")
    @allure.step("参数：login={0}")
    def test_getDischgedMrAssistDetail(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getDischgedMrAssistDetail.json"
        inpatientNo = self.transfer_dischged_assionMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = {
                "reportName": "dischgedMr",
                "inpatientNo": inpatientNo[0],
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_get(url, data, cook, inpatientNo[0])

    @allure.title("首次病程记录列表")
    @allure.story("住院信息-病程记录")
    @allure.step("参数：login={0}")
    def test_getProgressRecMaster(self, login):
        response1, cook = login
        url = host + port_es + "/progressRec/getProgressRecMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_progress_recMaster(self, response1, cook):
        url = host + port_es + "/progressRec/getProgressRecMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("首页病程信息详情")
    @allure.story("住院信息-病程记录")
    @allure.step("参数：login={0}")
    def test_getProgressRecDetail(self, login):
        response1, cook = login
        url = host + port_es + "/progressRec/getProgressRecDetail.json"
        inpatientNo = self.transfer_progress_recMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = dict(size=1, inpatientNo=inpatientNo[0],
                        type=1,  # 1：首次病程记录，2：日常查房记录，3：上级医师查房记录，4：抢救记录，5：转入记录
                        # 5：转入记录，6：转出记录，7：操作记录，8：会诊记录，9：输血记录，10阶段小结，11：疑难病例讨论记录，12：死亡病例讨论记录
                        hospitalCode=response1["hospitalCode"],
                        page=1, authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, inpatientNo[0])

    @allure.title("手术记录列表")
    @allure.story("住院信息-围手术期记录--手术记录")
    @allure.step("参数：login={0}")
    def test_perioperativeRecordMaster(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/perioperativeRecordMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_perioperative_recMaster(self, response1, cook):
        url = host + port_es + "/hospitalization/perioperativeRecordMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        print_json_multi_row(json.loads(result.text))
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("手术记录信息详情")
    @allure.story("住院信息-围手术期记录--手术记录")
    @allure.step("参数：login={0}")
    def test_perioperativeRecordDetail(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/perioperativeRecordDetail.json"
        inpatientNo = self.transfer_perioperative_recMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNO={inpatientNo}")
        if len(inpatientNo) > 0:
            data = dict(size=1, inpatientNo=inpatientNo[0],
                        reqType=1,  # 1：手术记录，2：术前小结，3：术前讨论，4：术后首次病程记录
                        hospitalCode=response1["hospitalCode"],
                        page=1, authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, inpatientNo[0])

    @allure.title("24小时出入院记录列表")
    @allure.story("住院信息-24小时出入院记录")
    @allure.step("参数：login={0}")
    def test_inAndOutHospitalForOneDayMaster(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/inAndOutHospitalForOneDayMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_inAndOutHospital_Master(self, response1, cook):
        url = host + port_es + "/hospitalization/inAndOutHospitalForOneDayMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                print(i)
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("出院信息详情")
    @allure.story("住院信息-出院")
    @allure.step("参数：login={0}")
    def test_inAndOutHospitalForOneDayDetail(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/inAndOutHospitalForOneDayDetail.json"
        inpatientNo = self.transfer_inAndOutHospital_Master(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = {
                "inpatientNo": inpatientNo[0],
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_get(url, data, cook, inpatientNo[0])

    @allure.title("急诊留观的列表信息")
    @allure.story("住院信息-急诊留观记录")
    @allure.step("参数：login={0}")
    def test_observationMaster(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/observationMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_observation_Master(self, response1, cook):
        url = host + port_es + "/hospitalization/observationMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                print(i)
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("急诊留观的信息详情")
    @allure.story("住院信息-急诊留观记录")
    @allure.step("参数：login={0}")
    def test_observationDetail(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/observationDetail.json"
        inpatientNo = self.transfer_observation_Master(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = {
                "inpatientNo": inpatientNo[0],  # ZY010008031671 这个有数据
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_get(url, data, cook, inpatientNo[0])

    @allure.title("医嘱列表")
    @allure.story("住院信息-医嘱")
    @allure.step("参数：login={0}")
    def test_hospitalizationInAndOutHospitalForOneDayMaster(self, login):
        response1, cook = login
        url = host + port_es + "/hospitalization/inAndOutHospitalForOneDayMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_inAndOutHospital_OneDayMaster(self, response1, cook):
        url = host + port_es + "/hospitalization/inAndOutHospitalForOneDayMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}

        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("医嘱信息详情")
    @allure.story("住院信息-医嘱")
    @allure.step("参数：login={0}")
    def test_getVisitOrderAssistDetail(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getVisitOrderAssistDetail.json"
        inpatientNo = self.transfer_inAndOutHospital_OneDayMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = dict(reportName="visitOrder",  # 在这里是固定的格式
                        inpatientNo=inpatientNo[0],
                        # typeName="临时医嘱",
                        startDate="", endDate="",
                        # itemClass="",
                        # moName="",
                        page=1, size=10,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "全景-住院-医嘱-查询医嘱")

    @allure.title("诊断记录列表")
    @allure.story("全景-诊断")
    @allure.step("参数：login={0}")
    def test_getDiagnosisAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/data/getDiagnosisAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook, ids[0])

    def transfer_Diagnosis_recMaster(self, response1, cook):
        url = host + port_es + "/data/getDiagnosisAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": [], "dataId": []}
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                # dicdata["inpatientNo"].append(i["inpatientNo"])
                dicdata["dataId"].append(i["dataId"])
        return dicdata

    @allure.title("诊断信息详情")
    @allure.story("全景-诊断")
    @allure.step("参数：login={0}")
    def test_getDiagnosisAssistDetail(self, login):
        response1, cook = login
        url = host + port_es + "/data/getDiagnosisAssistDetail.json"
        dataId = self.transfer_Diagnosis_recMaster(response1, cook)["dataId"]
        allure.attach(f"内部参数：dataId={dataId}")
        if len(dataId) > 0:
            data = dict(dataId=dataId[0],  # 19764184
                        type=2,
                        hospitalCode=response1["hospitalCode"],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, response1["hospitalCode"])

    @allure.title("肺功能检查列表")
    @allure.story("全景-肺功能检查")
    @allure.step("参数：login={0}")
    def test_getExamReportMasterAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getExamReportMasterAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(reportName="examReportMaster",
                    id=ids[0],
                    startDate="", endDate="", page=1, size=10,
                    sort="desc",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, ids[0])

    def transfer_ExamReport_AssistMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getExamReportMasterAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = dict(reportName="examReportMaster",
                    id="20ccec4f-39ab-41a1-b6ae-3ab3a435010d",  # 20ccec4f-39ab-41a1-b6ae-3ab3a435010d
                    startDate="", endDate="", page=1, size=10,
                    sort="desc",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        if type(json.loads(result.text)["responseData"]) is dict:
            resultdic = json.loads(result.text)["responseData"]["content"]
            dicdata1 = {"reportId": []}
            if len(resultdic) > 0:
                for i in resultdic:
                    for j in i["mapList"]:
                        dicdata1["reportId"].append(j["reportId"])
            return dicdata1

    @allure.title("肺功能检查项目列表")
    @allure.story("全景-肺功能检查")
    @allure.step("参数：login={0}")
    def test_getExamReportDetailPageAssistDetail(self, login):
        response1, cook = login
        url = host + port_es + "/data/getExamReportDetailPageAssistDetail.json"
        dicdata = self.transfer_ExamReport_AssistMaster(response1, cook)
        allure.attach(f"内部参数：dicdat={dicdata}")
        if dicdata is not None:
            if len(dicdata["reportId"]) > 0:
                data = dict(reportName="examReportDetail",
                            reportId=dicdata["reportId"][0],
                            reportType=1, hospitalCode=response1["hospitalCode"],
                            # page=1, size=10,
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证10")

    @allure.title("趋势分析-指标类型")
    @allure.story("全景-肺功能检查")
    @allure.step("参数：login={0}")
    def test_getReportTempList(self, login):
        response1, cook = login
        url = host + port_es + "/data/getReportTempList.json"
        data = dict(type=2,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("趋势分析-检索指标")
    @allure.story("全景-肺功能检查")
    def test_getReportTempDetailList(self, login):
        response1, cook = login
        url = host + port_es + "/data/getReportTempDetailList.json"
        data = dict(id=8, name="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("趋势分析-检索临时指标")
    @allure.story("全景-肺功能检查")
    @allure.step("参数：login={0}")
    def test_getReportTempListByName(self, login):
        response1, cook = login
        url = host + port_es + "/data/getReportTempListByName.json"
        data = dict(type=2, name="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("趋势分析-执行按钮")
    @allure.story("全景-肺功能检查")
    @allure.step("参数：login={0}")
    def test_getReportChartList(self, login):
        response1, cook = login
        url = host + port_es + "/data/getReportChartList.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        dicdata = self.transfer_ExamReport_AssistMaster(response1, cook)
        allure.attach(f"内部参数：ids={ids}\ndicdata={dicdata}")
        if dicdata is not None:
            if len(dicdata["reportId"]) > 0:
                print(dicdata["reportId"])
                data = dict(id=ids[0],  # 20ccec4f-39ab-41a1-b6ae-3ab3a435010d
                            tagNames="预计值--FVC",  # 这里是预填参数
                            reportIds=dicdata["reportId"][0],  # 990eb2864ff4447086808949a386ec4b
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                assert_get(url, data, cook, dicdata["reportId"][0])

    @allure.title("全部医嘱用药列表")
    @allure.story("全景-用药")
    @allure.step("参数：login={0}")
    def test_getDrugAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getDrugAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(sort="desc", id=ids[0],  # "20ccec4f-39ab-41a1-b6ae-3ab3a435010d"
                    startDate="", endDate="", page=1, size=10,  # 这几个参数没有必要使用xls
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, ids[0])

    def transfer_Drug_AssistMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getDrugAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = dict(sort="desc", id=ids[0],  # "20ccec4f-39ab-41a1-b6ae-3ab3a435010d"
                    startDate="", endDate="", page=1, size=10,  # 这几个参数没有必要使用xls
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        dicdata = {"inpatientNo": []}
        if len(resultdic) > 0:
            for i in resultdic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("医嘱用药详情")
    @allure.story("全景-用药")
    @allure.step("参数：login={0}")
    def test_getDrugAssistDetail(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getDrugAssistDetail.json"
        inpatientNo = self.transfer_Drug_AssistMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNO={inpatientNo}")
        if len(inpatientNo) > 0:  # 当有数据的时候
            data = dict(reportName="visitOrder",
                        inpatientNo=inpatientNo[0],
                        startDate="", endDate="",
                        # page=1, size=10,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证10")

    @allure.title("全部检验记录")
    @allure.story("全景-检验")
    @allure.step("参数：login={0}")
    def test_getVisitLabAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getVisitLabAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(reportName="visitLab", sort="desc", id=ids[0],  # "20ccec4f-39ab-41a1-b6ae-3ab3a435010d"
                    startDate="", endDate="", page=1, size=10,  # 这几个参数没有必要使用xls
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, ids[0])

    def transfer_VisitLab_AssistMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getVisitLabAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = dict(reportName="visitLab", sort="desc", id=ids[0],  # "20ccec4f-39ab-41a1-b6ae-3ab3a435010d"
                    startDate="", endDate="", page=1, size=10,  # 这几个参数没有必要使用xls
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        dicdata = {"labSerialNum": [], "packageItem": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                if len(i["mapList"]) > 0:
                    for j in i["mapList"]:
                        dicdata["labSerialNum"].append(j["labSerialNum"])
                        dicdata["packageItem"].append(j["packageItem"])
        return dicdata

    @allure.title("检验信息详情")
    @allure.story("全景-检验")
    @allure.step("参数：login={0}")
    def test_getVisitLabPageAssistDetail(self, login):  # 检验信息详情
        response1, cook = login
        url = host + port_es + "/data/getVisitLabPageAssistDetail.json"
        dicdata = self.transfer_VisitLab_AssistMaster(response1, cook)
        labSerialNum = dicdata["labSerialNum"]
        packageItem = dicdata["packageItem"]
        allure.attach(f"内部参数：dicdata={dicdata}")
        if len(packageItem) > 0:  # 当有数据的时候
            data = dict(reportName="visitLab",
                        labSerialNum=labSerialNum[0],  # "20180919XJ_KSTPT10"
                        packageItem=packageItem[0],  # "结核菌涂片检查"
                        hospitalCode=response1["hospitalCode"],
                        # page=1, size=10,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证10")

    def transfer_visitLab_AssistDetail(self, response1, cook):
        url = host + port_es + "/data/getVisitLabPageAssistDetail.json"
        dicdata = self.transfer_VisitLab_AssistMaster(response1, cook)
        labSerialNum = dicdata["labSerialNum"]
        packageItem = dicdata["packageItem"]
        dicdata2 = {"itemCode": [], "testItem": [], "patientNo": []}
        if len(packageItem) > 0:  # 当有数据的时候
            data = dict(reportName="visitLab",
                        labSerialNum=labSerialNum[0],  # "20180919XJ_KSTPT10"
                        packageItem=packageItem[0],  # "结核菌涂片检查"
                        hospitalCode=response1["hospitalCode"],
                        page=1, size=10,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            result = requests.get(url, data, cookies=cook)
            resultdic = json.loads(result.text)["responseData"]["content"]
            if len(resultdic) > 0:
                for i in resultdic:
                    dicdata2["itemCode"].append(i["itemCode"])
                    dicdata2["testItem"].append(i["testItem"])
                    dicdata2["patientNo"].append(i["patientNo"])
        return dicdata2

    @allure.title("检验信息详情中的数据进行-趋势分析")
    @allure.story("全景-检验")
    @allure.step("参数：login={0}")
    def test_getVisitLabDiagram(self, login):
        response1, cook = login
        url = host + port_es + "/data/getVisitLabDiagram.json"
        dicdata = self.transfer_visitLab_AssistDetail(response1, cook)
        itemCode = dicdata["itemCode"]
        testItem = dicdata["testItem"]
        patientNo = dicdata["patientNo"]
        allure.attach(f"内部参数：itemCode={itemCode}\ntestItem={testItem}\npatientNo={patientNo}")
        if len(testItem) > 0:
            data = dict(reportName="visitLab",
                        itemCode=itemCode[0],  # 17930
                        testItem=testItem[0],  # "TOTAL^AREA"
                        patientNo=patientNo[0],  # "4162A522F3F11A18A679A5A39205C1B2"
                        clinicId="",
                        hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"],
                        authToken=response1["authToken"])
            assert_get(url, data, cook, testItem[0])

    @allure.title("全景-检查列表")
    @allure.story("全景-检验")
    @allure.step("参数：login={0}")
    def test_getVisitCheckAssistMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getVisitCheckAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(reportName="visitCheck",
                    id=ids[0],
                    startDate="", endDate="", page=1, size=10,
                    sort="desc",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_Check_AssistMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getVisitCheckAssistMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = dict(reportName="visitCheck",
                    id=ids[0],  # 20ccec4f-39ab-41a1-b6ae-3ab3a435010d
                    startDate="", endDate="", page=1, size=10,
                    sort="desc",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        dicdata1 = {"checkserialnum": []}
        if type(json.loads(result.text)["responseData"]) is dict:
            resultdic = json.loads(result.text)["responseData"]["content"]
            if len(resultdic) > 0:
                for i in resultdic:
                    for j in i["mapList"]:
                        dicdata1["checkserialnum"].append(j["checkserialnum"])
        return dicdata1

    @allure.title("检查项目检查报告")
    @allure.story("全景-检验")
    @allure.step("参数：login={0}")
    def test_getVisitCheckAssistDetail(self, login):
        response1, cook = login
        url = host + port_es + "/data/getVisitCheckAssistDetail.json"
        checkserialnum = self.transfer_Check_AssistMaster(response1, cook)["checkserialnum"]
        allure.attach(f"内部参数：checkserialnum={checkserialnum}")
        if len(checkserialnum) > 0:
            data = dict(reportName="visitCheck",
                        checkserialnum=checkserialnum[0],  # 20160426001091
                        hospitalCode=response1["hospitalCode"],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, checkserialnum[0])

    @allure.title("全部住院记录列表信息")
    @allure.story("全景-治疗时间轴")
    @allure.step("参数：login={0}")
    def test_getTreatmentTimeAxisMaster(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getTreatmentTimeAxisMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "sort": "desc",
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    def transfer_TreatmentTime_AxisMaster(self, response1, cook):
        url = host + port_es + "/panorama/data/getTreatmentTimeAxisMaster.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        data = {
            "sort": "desc",
            "id": ids[0],
            "startDate": "",
            "endDate": "",
            "page": 1,
            "size": 10,  # 这里没有可选择的页数
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = requests.get(url, data, cookies=cook)
        dicdata = {"inpatientNo": []}
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            for i in resultdic:
                dicdata["inpatientNo"].append(i["inpatientNo"])
        return dicdata

    @allure.title("住院时间轴的数据显示")
    @allure.story("全景-治疗时间轴")
    @allure.step("参数：login={0}")
    def test_getTimeAxis(self, login):
        response1, cook = login
        url = host + port_es + "/similar/data/getTimeAxis.json"
        inpatientNo = self.transfer_TreatmentTime_AxisMaster(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        if len(inpatientNo) > 0:
            data = {
                "inpatientNo": inpatientNo[0],  # ZY010008031671 这个有数据
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]
            }
            assert_get(url, data, cook)

    @allure.title("患者的基本信息")
    @allure.story("右上角的-查看患者基本信息")
    @allure.step("参数：login={0}")
    def test_getPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/panorama/data/getPatientInfo.json"
        ids = self.transfer_patientList(response1, cook)["id"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(patiId=ids[0],
                    hospitalCode="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)


if __name__ == '__main__':
    pytest.main(["-s", "test_panorama.py", "--reruns=5"])
