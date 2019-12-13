#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_modelDisease.py
@time: 2019/9/9  16:52
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("临床科研一体化- 典型病例库")
class Test_modelDisease:

    @allure.title("输入患者流水号-患者列表，数据列表展示")
    @allure.story("典型病例库操作--输入患者流水号")
    @allure.step("参数：login={0}")
    def test_getPatientList(self, login):
        response1, cook = login
        url = host + port_es + "/similar/data/getPatientList.json"
        data = {"startDate": "", "endDate": "",
                # "page": 1, "size": 10, "key": "",
                "userId": response1["authUserId"], "authUserId": response1["authUserId"], "authToken": response1["authToken"]}
        overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "典型病例库-患者列表")

    def transfer_getPatientList(self, response1, cook):
        url = host + port_es + "/similar/data/getPatientList.json"
        data = {"key": "", "startDate": "", "endDate": "",
                "page": 1, "size": 10,
                "userId": response1["authUserId"], "authUserId": response1["authUserId"], "authToken": response1["authToken"]}
        reslut = requests.get(url, data, cookies=cook)
        ids = []
        reslutdic = json.loads(reslut.text)["responseData"]["content"]
        if len(reslutdic) > 0:
            for i in reslutdic:
                ids.append(i["INPATIENT_NO"])
        return ids

    @allure.title("输入患者流水号-患者列表 病人的详细 诊断")
    @allure.story("典型病例库操作--输入患者流水号")
    @allure.step("参数：login={0}")
    def test_getPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/similar/data/getPatientInfo.json"
        inpatientNo = self.transfer_getPatientList(response1, cook)
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = {"inpatientNo": inpatientNo[0],
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]}
        assert_get(url, data, cook, "获取相似度患者信息操作成功！")

    @allure.title("患者查询记录 记录列表")
    @allure.story("典型病例库操作--患者查询记录")
    @allure.step("参数：login={0}")
    def test_getSimilarRecordDataValue(self, login):
        response1, cook = login
        url = port_model + "/patient_similar/getSimilarRecordDataValue"
        data = dict(startDate="", endDate="",
                    # page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证  10")

    @allure.title("患者查询记录 记录列表")
    @allure.story("典型病例库操作--患者查询记录")
    def transfer_getSimilarRecordDataValue(self, response1, cook):
        url = port_model + "/patient_similar/getSimilarRecordDataValue"
        data = dict(startDate="", endDate="",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["INPATIENT_NO"])
        return ids

    @allure.title("患者的查询记录 详细的信息")
    @allure.story("典型病例库操作--患者查询记录")
    @allure.step("参数：login={0}")
    def test_getNewPatientInfo(self, login):
        response1, cook = login
        url = port_model + "/patient_similar/getNewPatientInfo"
        inpatientNo = self.transfer_getSimilarRecordDataValue(response1, cook)
        if len(inpatientNo) > 0:
            data = dict(inpatientNo=inpatientNo[0],
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_get(url, data, cook, "人口学信息")
