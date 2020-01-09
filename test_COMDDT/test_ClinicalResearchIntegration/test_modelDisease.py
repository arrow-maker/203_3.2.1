#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_modelDisease.py
@time: 2019/9/9  16:52
@Author:Terence
"""
from public.overWrite_Assert import *

templateId = 15316  # 典型病例库智能搜索模板Id
w_Id = "ZY020000507548_238"  # 患者相似权重分析Id
responseid = [35]  # 保存相似分析的添加到历史记录的节点Id


@allure.feature("临床科研一体化- 典型病例库")
class Test_modelDisease:

    @allure.title("输入患者流水号-患者列表，数据列表展示")
    @allure.story("典型病例库操作--输入患者流水号")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getPatientList(self, login, start, end):
        response1, cook = login
        url = host + port_es + "/similar/data/getPatientList.json"
        data = {"startDate": start, "endDate": end,
                # "page": 1, "size": 10, "key": "",
                "userId": response1["authUserId"], "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]}
        overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "典型病例库-患者列表")

    def patientList(self, response1, cook):
        url = host + port_es + "/similar/data/getPatientList.json"
        data = {"key": "", "startDate": "", "endDate": "",
                "page": 1, "size": 10,
                "userId": response1["authUserId"], "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]}
        reslut = requests.get(url, data, cookies=cook)
        ids = {"inpatientNo": [], "patientId": [], "patientName": []}
        reslutdic = json.loads(reslut.text)["responseData"]["content"]
        if len(reslutdic) > 0:
            for i in reslutdic:
                ids["inpatientNo"].append(i["INPATIENT_NO"])
                ids["patientId"].append(i["PATI_ID"])
                ids["patientName"].append(i["PATIENTNAME"])
        return ids

    @allure.title("输入患者流水号-患者列表 病人的详细 诊断")
    @allure.story("典型病例库操作--输入患者流水号")
    @allure.step("参数：login={0}")
    def test_getPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/similar/data/getPatientInfo.json"
        inpatientNo = self.patientList(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = {"inpatientNo": inpatientNo[0],
                "hospitalCode": response1["hospitalCode"],
                "authUserId": response1["authUserId"],
                "authToken": response1["authToken"]}
        assert_get(url, data, cook, "获取相似度患者信息操作成功！")

    @allure.title("患者查询记录 记录列表")
    @allure.story("典型病例库操作--患者查询记录")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getSimilarRecordDataValue(self, login, start, end):
        response1, cook = login
        url = port_model + "/patient_similar/getSimilarRecordDataValue"
        data = dict(startDate=start, endDate=end,
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

    @allure.title("插入患者数据")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similarInsert_simm_record(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/insert_simm_record"
        data = {
            "record_type": 1,
            "data": congyaml["典型病例库"]["智能分析插入数据"]["data"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("python统计")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_codeItemFindCodeItem(self, login):
        response1, cook = login
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = {
            "code": "SYS_DOMAIN",
            "itemCode": "PYTHON_STATISTIC_DOMAIN",
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    @allure.title("患者的基本信息")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similarbase_template(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/base_template"
        data = {
            "type": 1,
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_post(url, data, cook)

    @allure.title("患者的相似值分析")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_getDataIndexValueTreeList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = {
            "topCategoryId": 3127,
            "operatorId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    @allure.title("保存临时模板")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_dataTemplatesaveDataTemplate(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        data = {
            "type": 40, "status": 1, "dataScope": 1, "timeScope": 2, "version": 3,
            "indexRule": 1, "resultStore": 2, "operatorId": response1["authUserId"],
            "patientQueryWhere": congyaml["典型病例库"]["保存临时模板"]["patientQueryWhere"],
            "templateName": "临时版本1577087716583", "dataIds": congyaml["典型病例库"]["保存临时模板"]["dataIds"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        result = assert_post(url, data, cook)
        global templateId
        templateId = result[1]["responseData"]["templateId"]

    @allure.title("保存临时数据分析结果")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_saveDataAnalysisResult(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataAnalysisResult.json"
        data = dict(templateId=templateId,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("获取相似患者列表数据")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similarMatch_weight(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/match_weight"
        inpatientNo = self.patientList(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(db_type="m", req_number=20, w_name="临时版本", t_id=templateId,
                    patient_id=inpatientNo[0],
                    w_defined=0, patient_msg=f"new,{response1['authUserId']},{response1['itemOrgId']}",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = assert_post(url, data, cook)
        global w_Id
        w_Id = result[1]["resultData"]["w_id"]

    @allure.title("获取相似患者列表数据统计")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similarCount_proportion(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/count_proportion"
        data = dict(w_id=w_Id,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    """
    下面的数据操作是基于有患者的前提之下。操作
    """

    @allure.title("患者分析结果列表")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_resourceFindList(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/findList.json"
        data = dict(moduleType=1, dirType=1, operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("患者相似分析后得到的列表")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_patient_page(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/patient_page"
        data = dict(timestamp=time_up, w_id=w_Id, s_id="",
                    page=1, page_size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者相似分析后得到的指标权重值")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_count_proportion(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/count_proportion"
        data = dict(w_id=w_Id,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者相似分析后得到的分组路径")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_treatment_pathway(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/treatment_pathway"
        data = dict(pt_list="ZY010008021765,ZY360000220499,ZY010008029272,ZY110000535730,ZY010000596937,"
                            "ZY130000291153,ZY020000604676,ZY010000618576,ZY070000398216,ZY020000618244,",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者相似分析后得到的时间轴路径")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_getTimeAxis(self, login):
        response1, cook = login
        url = host + port_es + "/similar/data/getTimeAxis.json"
        inpatientNo = self.patientList(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0], hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("患者相似分析后得到的病例统计数据比例")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_copd_charts(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/copd_charts"
        data = dict(w_id=w_Id,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者相似分析后得到的患者相似对比数据比例")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_patient_contrast(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/patient_contrast"
        inpatientNo = self.patientList(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(pt_list=inpatientNo[0], w_id=w_Id,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者相似分析后得到的数据导出")
    @allure.story("智能搜索相似患者")
    @allure.step("参数：login={0}")
    def test_patient_similar_download_file(self, login):
        response1, cook = login
        url = host + port_python + "/patient_similar/download_file"
        inpatientNo = self.patientList(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(w_Id=w_Id, pt_list=inpatientNo[0])
        result = requests.post(url, data, cookies=cook)
        assert result.status_code == 200

    """
        下面的是保存到历史的记录中
    """

    @allure.title("添加节点")
    @allure.story("保存到历史记录")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("Name", ("新增节点1.0", "新增节点@2.0"))
    def test_resource_save(self, login, Name):
        response1, cook = login
        url = host + port_resource + "/resource/dir/save.json"
        data = dict(dirType=1, moduleType=1, id="", type=1, name=Name,
                    orgId="", operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("节点列表展示")
    @allure.story("保存到历史记录")
    @allure.step("参数：login={0}")
    def test_resource_findList(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/findList.json"
        param = dict(moduleType=1, dirType=1, operatorId=response1["authUserId"],
                     authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = assert_get(url, param, cook)
        global responseid
        for i in result[1]["responseData"]:
            responseid.append(i["id"])

    @allure.title("添加节点")
    @allure.story("保存到历史记录")
    @allure.step("参数：login={0}")
    def test_resource_save1(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/save.json"
        data = dict(dirType=1, moduleType=1, id=responseid, type=1,
                    name="新节点1.1", operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("保存到历史的记录")
    @allure.story("保存到历史记录")
    @allure.step("参数：login={0}")
    def test_resource_save2(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/save.json"
        datadic = self.patientList(response1, cook)
        origPatientId = datadic["patientId"]
        origPatientName = datadic["patientName"]
        allure.attach(f"内部参数：datadic={datadic}")
        data = dict(dirType=1, moduleType=1, id="", parentId=40,
                    type=2, name="数据搜集", wId=w_Id,
                    tId=templateId, origPatientId=origPatientId,
                    origPatientName=origPatientName, operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("删除节点")
    @allure.story("保存到历史记录")
    @allure.step("参数：login={0}")
    def test_resource_delete(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/delete.json"
        data = dict(id=responseid, type=1, operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    """
        下面的是对历史记录的操作·····
    """

    @allure.title("个人历史记录列表")
    @allure.story("历史记录")
    @allure.step("参数：login={0}")
    def test_resource_findList1(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/findList.json"
        data = {
            "moduleType": 1,
            "dirType": 1,
            "operatorId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)

    @allure.title("科室目录")
    @allure.story("历史记录")
    @allure.step("参数：login={0}")
    def test_resource_findList2(self, login):
        response1, cook = login
        url = host + port_resource + "/resource/dir/findList.json"
        data = {
            "moduleType": 1,
            "dirType": 2,
            "orgId": response1["orgId"],
            "operatorId": response1["authUserId"],
            "authUserId": response1["authUserId"],
            "authToken": response1["authToken"]
        }
        assert_get(url, data, cook)


if __name__ == '__main__':
    pytest.main()
