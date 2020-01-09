#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file: test_indexDataManege.py
@time: 2019/10/15 10:25
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("指标数据管理")
class Test_indexDataManege:

    @allure.title("指标分类列表")
    @allure.story("数据加载显示-指标分类列表")
    @allure.step("参数：login={0}")
    def test_getDataCategoryTreeList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/getDataCategoryTreeList.json"
        data = dict(type=1, categoryName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def indexList(self,response1, cook):
        url = host + port_dataindex + "/dataIndex/dataCategory/getDataCategoryTreeList.json"
        data = dict(type=1, categoryName="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        ids ={"path": [[]], "id": []}
        if len(resultdic) > 0:
            for i in resultdic:
                if len(i["children"]) > 0:
                    ids["path"].append(i["path"])
                    for k in i["children"]:
                        ids["id"].append(k["path"])
                else:
                    ids["path"][0].append(i["path"])
        return ids

    @allure.title("新增-指标分类")
    @allure.story("数据加载显示-指标分类列表")
    @allure.step("参数：login={0}")
    def test_saveDataCategory(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/saveDataCategory.json"
        data = dict(categoryName="添加药物治疗", categoryNameEng="",
                    type=1, note="新增", parentCategoryId="",
                    sequence=0, abbr="qw",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("修改-指标分类")
    @allure.story("数据加载显示-指标分类列表")
    @allure.step("参数：login={0}")
    def test_saveDataCategory1(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/saveDataCategory.json"
        path = self.indexList(response1, cook)["id"]
        allure.attach(f"内部参数：path={path}")
        data = dict(categoryId=path[0][0], categoryName="添加药物治疗1",
                    type=1, note="新增", status=1, sequence=0, abbr="qw",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("指标数据列表查询")
    @allure.story("指标数据操作")
    @allure.step("参数：login={0}")
    def test_getDataIndexList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/getDataIndexList.json"
        path = self.indexList(response1, cook)["id"]
        allure.attach(f"内部参数：path={path}")
        data = dict(
            page=1, size=10,
            path=path[0][1],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("指标列表")
    @allure.step("参数：login={0}")
    def dataIndexList(self,response1, cook):
        url = host + port_dataindex + "/dataIndex/getDataIndexList.json"
        path = self.indexList(response1, cook)["id"]
        allure.attach(f"内部参数：path={path}")
        data = dict(
            page=1, size=10,
            path=path[0][1],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        if "content" in result.text:
            resultdic = json.loads(result.text)["responseData"]["content"]
            if len(resultdic) > 0:
                for i in resultdic:
                    ids.append((i["ID"], i["DATA_CATEGORY"]))
        return ids

    def dataids(self, response1, cook):
        path = self.indexList(response1, cook)["id"]
        url = host + port_dataindex + "/dataIndex/getDataIndexList.json"
        data = dict(
            page=1, size=10,
            path=path[0][1],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["ID"])
        return ids

    @allure.title("新增-指标分类-子分类")
    @allure.story("指标数据操作")
    @allure.step("参数：login={0}")
    def test_saveDataCategory2(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/saveDataCategory.json"
        path = self.indexList(response1, cook)["id"]
        data = dict(
            dataType=1, dataValueType=1, isQuestionaire=0, isDerived=0,
            schemaId=1, dataName="药片一", dataDefinition="新增2",
            valueRange="2-9", formulas="x+y", dataCategory=path[0][1],
            valueType="",
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    # @allure.title("新增-指标数据-")
    # @allure.story("指标数据操作")
    # @pytest.mark.skip("这个版本没有这个功能")
    # def test_saveDataIndex(self, login):
    #     response1, cook = login
    #     url = host + port_dataindex + "/dataIndex/saveDataIndex.json"
    #     path = self.indexList(response1, cook)["id"]
    #     data = dict(categoryName="使用药片", categoryNameEng="", type=1,
    #                 note="分类说明不能为空", status="",
    #                 parentCategoryId=path[0][0], sequence=0,
    #                 authUserId=response1["authUserId"], authToken=response1["authToken"])
    #     assert_post(url, data, cook)

    @allure.title("查重权重-展示")
    @allure.story("指标数据操作")
    @allure.step("参数：login={0}")
    def test_show_index_merge_template(self, login):
        response1, cook = login
        url = host + ":5100/patient_similar/show_index_merge_template"
        data = dict(type=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("配置权重")
    @allure.story("指标数据操作")
    @allure.step("参数：login={0}")
    def test_save_merge_template(self, login):
        response1, cook = login
        url = host + ":5100/patient_similar/save_merge_template"
        yamdata = congyaml["指标数据管理"]["配置权重"]
        data = dict(value=yamdata["value"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("所有的指标数据")
    @allure.story("查重处理")
    @allure.step("参数：login={0}")
    def test_getDataSchemaList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataSchema/getDataSchemaList.json"
        data = dict(status=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("相似的指标")
    @allure.story("查重处理")
    @allure.step("参数：login={0}")
    def test_getDataCheckList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/getDataCheckList.json"
        data = dict(page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("删除-指标")
    @allure.story("指标操作")
    @allure.step("参数：login={0}")
    def test_updateStatusBatch(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/updateStatusBatch.json"
        dataIds = self.dataids(response1, cook)
        allure.attach(f"内部参数：dataIds={dataIds}")
        data = dict(dataIds=dataIds[0], status=0, type=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("删除-指标分类-子分类")
    @allure.story("数据加载显示-指标分类列表")
    @allure.step("参数： login={0}")
    def test_updateStatus(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/updateStatus.json"
        path = self.indexList(response1, cook)["id"]
        allure.attach(f"内部参数：path={path}")
        data = dict(categoryName="使用药片", categoryNameEng="", type=1,
                    note="分类说明不能为空", status="",
                    parentCategoryId=path[0][0], sequence=0,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("删除-指标分类-主分类")
    @allure.story("数据加载显示-指标分类列表")
    @allure.step("参数： login={0}")
    def test_updateStatus1(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/updateStatus.json"
        path = self.indexList(response1, cook)["id"]
        allure.attach(f"内部参数：path={path}")
        data = dict(categoryId=path[0][0], status=9,
                    type=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("修改指定的指标")
    @allure.story("指标分类列表")
    @allure.step("参数：login={0}")
    def test_saveDataIndex1(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/saveDataIndex.json"
        path = self.dataIndexList(response1, cook)
        allure.attach(f"内部参数：path={path}")
        if len(path) > 0:
            data = dict(dataType=1, dataValueType=1,
                        isQuestionaire=0, isDerived=0, dataName="入院时间",
                        dataDefinition="/", id=path[0][0],
                        dataCategory=path[0][1],
                        valueType="date",
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            assert_post(url, data, cook)


if __name__ == '__main__':
    pytest.main()
