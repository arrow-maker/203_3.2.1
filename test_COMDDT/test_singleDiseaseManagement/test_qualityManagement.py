# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_qualityManagement.py
    Time:    2019/12/18 15:17
    Author:  Arrow
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *
templateId = 15027  # 这里是本次质控中的搜索患者列表的模板ID
batchId = [223]  # 这里是历史记录中的图表类型ID


@allure.feature("质控部门")
class Test_qualityDepartment:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.hospitalCode = response1["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = response1["responseData"]["roleList"][0]["orgId"]
        self.itemOrgId = response1["responseData"]["itemOrgId"]

    @allure.title("医院和科室信息")
    @allure.story("本次质控")
    def test_getOrgInfoTreeList(self):
        url = host + portlogin + "/org/orgInfo/getOrgInfoTreeList.json"
        data = {
            "listType": 2,
            "status": 1,
            "orgTypeIds": "35, 38",
            "path": 400,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("患者数据")
    @allure.story("本次质控")
    def test_tableList(self):
        url = host + port_dataindex + "/qc/table/list.json"
        data = {
            "type": 1,
            "checkFlag": 0,
            "initiatorId": self.authUserId,
            "page": 1,
            "size": 1,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("保存临时数据模板")
    @allure.story("本次质控-抽取患者列表")
    def test_saveDataTemplate(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        data = {
            "status": 2,
            "version": 3,
            "dataIds": "248, 249, 258, 3502, 724, 893, 2852, 2909, 2781, 4310, 1516, 1519, 1523, 1544, 1560, 1548, "
                       "5771, 5772, 15140, 15141, 2884, 2887, 2898, 2908, 1555, 3294, 5638, 5639, 5640, 5641, 5642, "
                       "5643, 5644, 5645, 5646, 5647, 5648, 5649, 5650, 5292, 4161, 4316, 5774, 14968, 1513, 909, "
                       "3445, 1171, 3163, 15070, 15071, 15072, 15073, 3530, 3531, 3532, 3533, 3534, 3535, 3536",
            "patientQueryWhere": '{"logicSymbol": "and", "whereList": [{"logicSymbol": "or", "whereType": 1, '
                                 '"whereList": [{"logicSymbol": "or", "whereList": [{"symbol": "=", "dataValueType": '
                                 '"1", "dataId": "463", "dataRId": "415", "columnValue": "2017-12-01,2020-01-01", '
                                 '"columnName": "INDEX_TIME", "columnTitle": "住院", "columnType": "date", "dataName": '
                                 '"出院时间"}], "nextLogicSymbol": "and"}, {"logicSymbol": "or", "whereList": [{"symbol": '
                                 '"=", "dataValueType": "2", "dataId": "1519", "dataRId": "1433", "columnValue": "是", '
                                 '"columnName": "AECOPD", "columnTitle": "慢性阻塞性肺疾病急性加重期", "columnType": "string", '
                                 '"dataName": "是否AECOPD患者"}]}]}]}',
            "dataScope": 1,
            "operatorId": self.authUserId,
            "type": 20,
            "templateName": f"初始版本{time_up}",
            "timeScope": 2,
            "indexRule": 1,
            "randomNum": 10,
            "businessVariables": '{"dataType": "5", "dataId": "5"}',
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_post(url, data, self.cook)
        global templateId
        templateId = result[1]["responseData"]["templateId"]

    @allure.title("保存临时数据分析")
    @allure.story("本次质控-抽取患者列表")
    def test_saveDataAnalysisResult(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataAnalysisResult.json"
        data = {
            "templateId": templateId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("获取数据列表")
    @allure.story("本次质控-抽取患者列表")
    def test_getDataAnalysisResultList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        data = {
            "templateId": templateId,
            "page": 1,
            "size": 10,
            "resultType": 0,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("获取数据总数")
    @allure.story("本次质控-抽取患者列表")
    def test_getDataAnalyzeCount(self):
        url = host + port_dataindex + "/dataIndex/dataStore/getDataAnalyzeCount.json"
        data = {
            "templateId": templateId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("图表类型-数据展示")
    @allure.story("历史记录")
    def test_batchList(self):
        url = host + port_dataindex + "/qc/batch/list.json"
        data = {
            "types": 1,
            "initiatorId": self.authUserId,
            "operatorId": self.authUserId,
            "page": 1,
            "size": 10000,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        global batchId
        for i in result[1]["responseData"]["content"]:
            batchId.append(i["ID"])

    @allure.title("患者列表-数据展示")
    @allure.story("历史记录")
    def test_batchPatientList(self):
        url = host + port_dataindex + "/qc/batch/patient/list.json"
        print(f"batchId={batchId}")
        data = {
            "batchId": batchId[0],
            "taskFlag": 1,
            "page": 1,
            "size": 5,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    """
        这里的生成简表没有添加
    """
    @allure.title("生成简表")
    @allure.story("本次质控")
    def test_batchCreate(self):
        url = host + port_dataindex + "/qc/batch/create.json"
        ids = congyaml["医疗质量管理"]["质控部门"]["生成简表"]["ids"]
        data = {
            "type": 1,
            "ids": ids,
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

if __name__ == '__main__':
    pytest.main()