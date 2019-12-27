#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_similarityMeasure.py
@time: 2019/9/10  11:43
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("相似病例智能分析")
class Test_similarityMeasure:

    # ------------------------------选择与新建患者-----------------------------
    @allure.title("数据库患者列表展示")
    @allure.story("数据库患者列表")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getPatientList(self, login, start, end):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getPatientList.json"
        data = dict(userId=response1["authUserId"],
                    page=1, size=10,
                    key="", startDate=start, endDate=end,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_getPatientList(self, response1, cook):
        url = host + port_es + "/similarnew/data/getPatientList.json"
        data = dict(userId=response1["authUserId"],
                    page=1, size=10,
                    key="", startDate="", endDate="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        datadic = {"ids": [], "data": []}
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                datadic["ids"].append(i["INPATIENT_NO"])
                datadic["data"].append(i)
        return datadic

    @allure.title("患者详细信息展示")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_getNewPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getPatientInfo.json"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0], hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "人口学信息")

    @allure.title("数据库患者相似分析设置-权重展示")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_showWeightTemplate(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/showWeightTemplate"
        data = dict(ptType=1,
                    default=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("数据库患者相似分析设置-权重保存修改")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_saveWeightTemplate(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/saveWeightTemplate"
        yamdata = congyaml["相似病例智能分析"]["保存权重修改"]
        data = dict(ptType=1,
                    data=yamdata["data"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, "权重配置保存成功")

    @allure.title("数据库相似病例智能分析记录-数据展示")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_getSimilarPatientRecord(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/getSimilarPatientRecord"
        data = dict(ptType=1, page=1, size=10, name="similar",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("相似病例智能分析记录-患者的检查指标数据")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_dataGetPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getPatientInfo.json"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0], hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, inpatientNo[0])

    @allure.title("相似病例智能分析记录-患者信息添加到数据库中")
    @allure.story("数据库患者列表")
    @allure.description("这个接口是必须的，要插入的数据库的-临时表中，下一个接口是要使用，以用于查找相似患者")
    def test_generalSimilarityInsertSimilarRecord(self, login, dlogin):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/insertSimilarRecord"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        yamdata = congyaml["相似病例智能分析"]["患者信息添加到数据库"]
        data1 = dict(name="similar", ptType=1, inpatientNo=inpatientNo[0],
                     data=yamdata["data"],
                     authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data1, cook, inpatientNo[0])

    @allure.title("由权重找患者--")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_generalSimilartyMathWeight(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/matchWeight"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        yamdata = congyaml["相似病例智能分析"]["权重查找患者"]
        data = dict(inpatientNo=inpatientNo[-1],
                    data=yamdata["data"],
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, response1["hospitalCode"])

    @allure.title("相似患者个数配置")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @pytest.mark.parametrize("size", (10, 15, 20, 25))
    def test_patientPage1(self, login, size):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/patientPage"
        scoreData = congyaml["相似病例智能分析"]["当前相似患者"]["scoreData"]
        data = {
            "page": 1,
            "size": size,
            "sort": 0,
            "number": 100,
            "scoreData": scoreData,
            "hospitalCode": response1["hospitalCode"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("导出相似患者列表")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_downloadFile(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/downloadFile"
        scoreData = congyaml["相似病例智能分析"]["当前相似患者"]["scoreData"]
        data = {
            "scoreData": scoreData
        }
        result = requests.post(url, data, cookies=cook)
        assert result.status_code == 200

    @allure.title("相似患者信息菜单配置")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @pytest.mark.parametrize("groupNo", ("XSG01", "XSG02", "XSG03", "XSG04", "XSG05", "XSG07"))
    def test_getReportGroupList(self, login, groupNo):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo=groupNo,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def inpatient_NO(self, response1, cook):
        url = host + port_python + "/generalSimilarity/matchWeight"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        yamdata = congyaml["相似病例智能分析"]["权重查找患者"]
        data = dict(inpatientNo=inpatientNo[-1],
                    data=yamdata["data"],
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.post(url, data, cookies=cook)
        ids = {"key": [], "data": [], "inpatientNo": []}
        if "patientList" in result.text:
            resultdic = json.loads(result.text)["resultData"]
            resultdic1 = resultdic["patientList"]
            resultdic2 = resultdic["localData"]
            for i in resultdic1:
                ids["data"].append(i)
                for k in i.keys():
                    ids["key"].append(k)
            for i in resultdic2:
                ids["inpatientNo"].append(i["inpatient_no"])
        return ids

    def reportNo(self, response1, cook):
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo="XSG01",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        if "reportNo" in result.text:
            resultdic = json.loads(result.text)["responseData"]
            for i in resultdic:
                ids.append(i["reportNo"])
        return ids

    @allure.title("相似患者信息菜单详细的信息设置")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @allure.step("参数：login={0}")
    def test_getReportDatas(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        report = self.reportNo(login[0], login[1])
        reportNo = ""
        for i in report:
            reportNo += i + ","
        inpatient = self.inpatient_NO(login[0], login[1])["key"]
        inpatientNo = ""
        for i in inpatient:
            inpatientNo += i + ","
        allure.attach(f"内部参数：report={report},\ninpatient={inpatient}")
        data = dict(reportNos=reportNo,
                    inPatientNos=inpatientNo,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("相似患者信息菜单详细的信息排序-相似度，转归，入院时间")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @pytest.mark.parametrize("sort", (0, 1, 2))
    def test_patientPage(self, login, sort):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/patientPage"
        socre = self.inpatient_NO(login[0], login[1])["data"]
        socredata = {}
        for i in range(20):
            socredata.update(socre[i])
        sdata = json.dumps(socredata)
        allure.attach(f"内部参数：socre={socre}")
        data = dict(page=1, size=20, sort=sort, number=20,
                    scoreData=sdata,
                    hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("相似患者信息菜单详细的信息排序-治疗路径")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("drugName", (0, 1, 2, 3, 4))
    def test_treatmentPathway(self, login, drugName):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/treatmentPathway"
        inpatient = self.inpatient_NO(login[0], login[1])["key"]
        inpatientNo = ""
        for i in inpatient:
            inpatientNo += i + ","
        allure.attach(f"内部参数：inpatent={inpatient}")
        data = dict(
            ptList=inpatientNo,
            drugName=drugName,
            hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("相似患者信息菜单详细的信息排序-患者诊疗时间轴")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_dataGetTimeAxis(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getTimeAxis.json"
        inpatientNo = self.inpatient_NO(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatentNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0],
                    hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, inpatientNo[0])

    @allure.title("相似患者信息菜单详细的信息排序-患者对比")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @allure.step("参数：login={0}")
    def test_patientContrast(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/patientContrast"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        socre = self.inpatient_NO(login[0], login[1])["data"]
        socredata = {}
        for i in range(2):
            socredata.update(socre[i])
        sdata = json.dumps(socredata)
        allure.attach(f"内部参数：ninpatient={inpatientNo}\nsocre={socre}")
        data = dict(inpatientNo=inpatientNo[1],
                    scoreData=sdata,
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    # @allure.story("患者查询记录-数据展示")
    # @pytest.mark.skip("这个版本没有这个功能")
    # def test_getSimilarRecordDataValue(self, login):
    #     response1, cook = login
    #     url = port_model + "/patient_similar/getSimilarRecordDataValue"
    #     data = dict(startDate="", endDate="",
    #                 # page=1, size=10,
    #                 authUserId=response1["authUserId"], authToken=response1["authToken"])
    #     overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证  10")

    # ----------------------------新建患者----------------------------------------

    @allure.title("新建患者列表展示-；列表数据")
    @allure.story("新建患者列表")
    @allure.step("参数：login={0}")
    def test_showPatientList(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/showPatientList"
        data = dict(patientName="", name="similar",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def newPatient(self, response1, cook):
        url = host + port_python + "/generalSimilarity/showPatientList"
        data = dict(patientName="", name="similar",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["resultData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                pass

    @allure.title("新建患者列表展示-；显示要增加的数据")
    @allure.story("新建患者列表")
    @allure.step("参数：login={0}")
    def test_showBuiltTemplate(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/showBuiltTemplate"
        data = dict(name="similar", inpatientNo="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "基本信息")

    @allure.title("新建患者列表展示-；添加患者信息")
    @allure.story("新建患者列表")
    @allure.step("参数：login={0}")
    def test_insertSimilarRecord(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/insertSimilarRecord"
        data = dict(name="similar", ptType=0, inpatientNo="",
                    data='{"基本信息":{"姓名":"荀·阿斯蒂","年龄":55,"性别":"男","入院方式":"其他机构转入","居住地":"安徽省","身高":177,"是否有ICU转科":0,'
                         '"住院时长":20,"住院总费用":500,"病例分型":"一般","转归":"治愈"}}',
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.story("写入新建患者数据")
    @allure.step("参数：login={0}")
    def test_insert_simm_record(self, login):
        response1, cook = login
        url = port_model + "/patient_similar/insert_simm_record"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatentNO={inpatientNo}")
        data = dict(record_type=2, data=inpatientNo[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.story("去用python统计")
    @allure.step("参数：login={0}")
    def test_findCodeItem(self, login):
        response1, cook = login
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "PYTHON统计")

    def transfer_hostAndPort(self, response1, cook):
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["href"]
        return resultdic

    @allure.story("指标的权重值模板")
    @allure.step("参数：login={0}")
    def test_base_template(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/patient_similar/base_template"
        data = dict(type=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("获取相似指标值列表")
    @allure.step("参数：login={0}")
    def test_getDataIndexValueTreeList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(topCategoryId=3127,
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

if __name__ == '__main__':
    pytest.main(["test_similarityMeasure.py", "-s"])
