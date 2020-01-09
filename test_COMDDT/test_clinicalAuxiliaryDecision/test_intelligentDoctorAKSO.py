# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_intelligentDoctorAKSO.py
    Time:    2019/12/9 13:37
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *

index_search = {}                                       # 临床指标保存可以筛选的数据
muti_search = {"支气管或肺恶性肿瘤": "C34.900"}            # 完善的条件保存可以筛选的数据
patient_search = {"间质性肺病,其他特指的": "J84.800"}      # 患者列表保存可以筛选的数据


@allure.feature("智医AKSO")
class Test_AKSO:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]

    @allure.title("历史记录")
    @allure.story("临床诊断决策支持")
    def test_getSearchRecord(self):
        url = host + port_sourcedata + "/diagPredict/getSearchRecord.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("可选指标数据")
    @allure.story("临床诊断决策支持")
    def test_getSymptomClassify(self):
        url = host + port_sourcedata + "/diagPredict/getSymptomClassify.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="临床表现")

    @allure.title("可选指标数据-筛选")
    @allure.story("临床诊断决策支持")
    def test_diagPredictSearch2(self):
        url = host + port_sourcedata + "/diagPredict/search.json"
        data = {"data": '[{"type": "admission", "items": [{"dataId": 1, "name": "临床表现", "value": "咳嗽"}]}]'}
        result = assert_post(url, data=data, cook=self.cook)
        global index_search
        for i in result[1]["responseData"]:
            index_search[i["name"]] = i["icd10"]

    @allure.title("可选指标数据-进行保存")
    @allure.story("临床诊断决策支持")
    def test_saveSearchRecord(self):
        url = host + port_sourcedata + "/diagPredict/saveSearchRecord.json"
        data = dict(authUserId=self.authUserId, record="咳嗽", authToken=self.authToken)
        assert_get(url, data, self.cook, hint="保存成功")

    @allure.title("可选指标数据-得到筛选的结果")
    @allure.story("临床诊断决策支持")
    def test_getSearchRecord1(self):
        url = host + port_sourcedata + "/diagPredict/getSearchRecord.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="咳嗽")

    @allure.title("筛选结果的详细的数据")
    @allure.story("筛选结果")
    def test_getMetaData(self):
        url = host + port_sourcedata + "/diagPredict/getMetaData.json"
        icdname = list(index_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(name="疾病概述,临床表现,推荐检查,推荐检验,推荐治疗方案",
                    icd10=icdname,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="咳嗽变异性哮喘")

    @allure.title("筛选结果的详细的数据-同诊断患者")
    @allure.story("筛选结果")
    def test_getMetaData2(self):
        url = host + port_es + "/diagPredict/getAllPatientByICD.json"
        icdname = list(muti_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        icdcode = muti_search[icdname[0]]
        data = dict(maxSize=1000, icdCode=icdcode, size=10, page=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("筛选结果的详细的数据-参考指南")
    @allure.story("筛选结果")
    def test_getGuide(self):
        url = host + port_sourcedata + "/diagPredict/getGuide.json"
        icdname = list(index_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(icd10=icdname, page=1, size=5,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("筛选结果的详细的数据-相关文献")
    @allure.story("筛选结果")
    def test_getLiterature(self):
        url = host + port_sourcedata + "/diagPredict/getLiterature.json"
        icdname = list(index_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(icd10=icdname, page=1, size=5,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("更完善的筛选条件-数据展示")
    @allure.story("临床诊断决策支持")
    def test_showBuiltTemplate(self):
        url = host + port_python + "/generalSimilarity/showBuiltTemplate"
        data = dict(name="diagnosis", inpatientNo="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="基本信息")

    @allure.title("患者姓名查询-保存")
    @allure.story("更完善的筛选条件")
    def test_insertSimilarRecord(self):
        url = host + port_python + "/generalSimilarity/insertSimilarRecord"
        data = dict(name="insertSimilarRecord", data='{"基本信息":{"姓名":"74614296E1D9FFAFCC3197E17C81221E"}}',
                    ptType=2, inpatientNo="", authUserId=self.authUserId)
        assert_post(url, data, self.cook, hint="患者记录保存成功")

    @allure.title("患者姓名查询-检查结果筛选")
    @allure.story("更完善的筛选条件")
    def test_search(self):
        url = host + port_sourcedata + "/diagPredict/search.json"
        data = dict(data='[{"type":"baseInfo","items":[{"dataId":0,"name":"姓名",'
                         '"value":"74614296E1D9FFAFCC3197E17C81221E"}]},{"type":"admission","items":[]},'
                         '{"type":"inspection","items":[]},{"type":"check","items":[]}]')
        result = assert_post(url, data, self.cook)
        global muti_search
        for i in result[1]["responseData"]:
            muti_search[i["name"]] = i["icd10"]

    @allure.title("患者姓名查询-检查数据显示")
    @allure.story("更完善的筛选条件")
    def test_showBuiltTemplate2(self):
        url = host + port_python + "/generalSimilarity/showBuiltTemplate"
        data = dict(name="diagnosis", inpatientNo="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="基本信息")

    @allure.title("多条件筛选结果的详细的数据")
    @allure.story("筛选结果")
    def test_getMetaData3(self):
        url = host + port_sourcedata + "/diagPredict/getMetaData.json"
        icdname = list(muti_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(name="疾病概述,临床表现,推荐检查,推荐检验,推荐治疗方案",
                    icd10=icdname[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="支气管或肺恶性肿瘤")

    @allure.title("多条件筛选结果的详细的数据-同诊断患者")
    @allure.story("筛选结果")
    def test_getMetaData4(self):
        url = host + port_es + "/diagPredict/getAllPatientByICD.json"
        icdname = list(muti_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        icdcode = muti_search[icdname[0]]
        data = dict(maxSize=1000, icdCode=icdcode, size=10, page=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("多条件筛选结果的详细的数据-参考指南")
    @allure.story("筛选结果")
    def test_getGuide2(self):
        url = host + port_sourcedata + "/diagPredict/getGuide.json"
        icdname = list(muti_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(icd10=icdname[0], page=1, size=5,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("多条件筛选结果的详细的数据-相关文献")
    @allure.story("筛选结果")
    def test_getLiterature2(self):
        url = host + port_sourcedata + "/diagPredict/getLiterature.json"
        icdname = list(muti_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(icd10=icdname[0], page=1, size=5,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    """
    下面是患者列表
    """

    @allure.title("患者数据列表的展示")
    @allure.story("患者列表")
    def test_showPatientList(self):
        url = host + port_python + "/generalSimilarity/showPatientList"
        data = dict(ptType=2, name="diagnosis", size=10, page=1, patientName="",
                    sex="", clinical="", createTime="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def inpatientNo(self):
        url = host + port_python + "/generalSimilarity/showPatientList"
        data = dict(ptType=2, name="diagnosis", size=10, page=1, patientName="",
                    sex="", clinical="", createTime="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        ids = []
        for i in result[1]["resultData"]["content"]:
            ids.append((i["inpatient_no"], i["姓名"]))
        return ids

    @allure.title("患者详情数据展示")
    @allure.story("患者列表")
    def test_showBuiltTemplate3(self):
        url = host + port_python + "/generalSimilarity/showBuiltTemplate"
        inpatientNo = self.inpatientNo()
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(name="diagnosis", inpatientNo=inpatientNo[0][0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("患者详情数据-保存")
    @allure.story("患者列表")
    def test_insertSimilarRecord2(self):
        url = host + port_python + "/generalSimilarity/insertSimilarRecord"
        inpatientNo = self.inpatientNo()
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = {
            "name": "diagnosis",
            "data": '{"基本信息": {"姓名": "%s", "吸烟史": "无"}}' % inpatientNo[0][1],
            "ptType": 2,
            "authUserId": self.authUserId,
            "inpatientNo": inpatientNo[0][0],
        }
        assert_post(url, data, self.cook, hint="患者记录保存成功")

    @allure.title("患者诊断预测")
    @allure.story("患者列表")
    def test_searchByInpatientNo2(self):
        url = host + port_sourcedata + "/diagPredict/searchByInpatientNo"
        inpatientNo = self.inpatientNo()
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0][0],
                    authUserId=self.authUserId, authToken=self.authToken)
        print(f"\nurl={url}\ndata={data}")
        result = assert_get(url, data, self.cook)
        global patient_search
        for i in result[1]["responseData"]:
            patient_search[i["name"]] = i["icd10"]

    @allure.title("患者列表筛选结果的详细的数据")
    @allure.story("患者列表")
    def test_getMetaData5(self):
        url = host + port_sourcedata + "/diagPredict/getMetaData.json"
        icdname = list(patient_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(name="疾病概述,临床表现,推荐检查,推荐检验,推荐治疗方案",
                    icd10=icdname,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="支气管或肺恶性肿瘤")

    @allure.title("患者列表筛选结果的详细的数据-同诊断患者")
    @allure.story("患者列表")
    def test_getMetaData6(self):
        url = host + port_es + "/diagPredict/getAllPatientByICD.json"
        icdname = list(muti_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        icdcode = muti_search[icdname[0]]
        data = dict(maxSize=1000, icdCode=icdcode, size=10, page=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("患者列表筛选结果的详细的数据-参考指南")
    @allure.story("患者列表")
    def test_getGuide3(self):
        url = host + port_sourcedata + "/diagPredict/getGuide.json"
        icdname = list(patient_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(icd10=icdname, page=1, size=5,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("患者列表筛选结果的详细的数据-相关文献")
    @allure.story("患者列表")
    def test_getLiterature3(self):
        url = host + port_sourcedata + "/diagPredict/getLiterature.json"
        icdname = list(patient_search.keys())
        allure.attach(f"内部参数：icdName={icdname}")
        data = dict(icd10=icdname, page=1, size=5,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)


if __name__ == '__main__':
    pytest.main()
