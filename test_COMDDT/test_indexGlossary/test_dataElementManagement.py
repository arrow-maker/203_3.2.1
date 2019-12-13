#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_dataElementManagement.py
@time: 2019/9/19  14:24
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("数据元管理")
class Test_dataElementManagement:

    @allure.title("获取")
    @allure.step("参数：login={0}")
    def test_getDataCategoryTreeList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/getDataCategoryTreeList.json"
        data = dict(type=2, topCategory="true", neCategoryId="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_getDataCateoryTreeList(self, response1, cook):
        url = host + port_dataindex + "/dataIndex/dataCategory/getDataCategoryTreeList.json"
        data = dict(type=2, topCategory="true", neCategoryId="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        path12 = []
        if len(resultdic) > 0:
            for i in resultdic:
                path12.append(i["categoryId"])
        return path12

    @allure.title("数据的种类列表")
    @allure.step("参数：login={0}")
    def test_getDataCategoryList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/getDataCategoryList.json"
        data = dict(type=2,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("数据元分类对应的数据元名称列表")
    @allure.step("参数：login={0}")
    def test_getDataSchemaList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataSchema/getDataSchemaList.json"
        paths = self.transfer_getDataCateoryTreeList(response1, cook)
        allure.attach(f"内部参数：paths={paths}")
        data = dict(
            page=1, size=10, path=paths[0],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_getDataSchemalList(self, response1, cook):
        url = host + port_dataindex + "/dataIndex/dataSchema/getDataSchemaList.json"
        paths = self.transfer_getDataCateoryTreeList(response1, cook)
        data = dict(
            page=1, size=10, path=paths[0],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        time.sleep(3)
        dicdata = {"dataCategory": []}
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                dicdata["dataCategory"].append(i["DATA_CATEGORY"])
        return dicdata

    @allure.title("新增 数据元分类")
    @allure.step("参数：login={0}")
    def test_saveDataCategory(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/saveDataCategory.json"
        data = dict(
            categoryName="",  # 分类名称
            categoryNameEng="news",  # 英文名称
            type=2,
            note="实验使用",  # 说明
            status=0,  # 状态
            parentCategoryId="",  # 上级
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("删除数据元分类")
    @allure.step("参数：login={0}")
    def test_updateStatus(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataCategory/updateStatus.json"
        categoryId = self.transfer_getDataCateoryTreeList(response1, cook)
        allure.attach(f"内部参数：category={categoryId}")
        if len(categoryId) > 1:
            data = dict(categoryId=categoryId[1], status=9, type=2,
                        authUserId=response1["authUserId"], authToken=response1["authToken"])
            result = requests.post(url, data, cookies=cook)
            print(result.text)
            assert categoryId[1] in result.text

    @allure.title("指标对应列表")
    @allure.story("数据元对应的数据")
    @allure.step("参数：login={0}")
    def test_getDataIndexList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/getDataIndexList.json"
        data = dict(
            page=1, size=10,
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("新增")
    @allure.story("数据元对应的数据")
    @allure.step("参数：login={0}")
    def test_saveDataSchema(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataSchema/saveDataSchema.json"
        dataCategory = self.transfer_getDataSchemalList(response1, cook)["dataCategory"]
        allure.attach(f"内部参数：dataCategory={dataCategory}")
        data = dict(
            dataId=1,  # 用于修改
            dataName="数据元名称",  # 数据元名称
            dataNameEng="324",  # 英文名
            dataType=1,  # 1：修改，3：新增
            dataSource="国家卫生行业标准WS 445.1-2014 电子病历基本数据集　第1部分：病历概要",  # 数据来源
            dataCategory=3099,
            status=1,  # 无效：0，有效：1
            dataValueType=3,
            valueRange=100,  # 数值范围
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("删除新增数据元关联性")
    @allure.story("数据元对应的数据")
    @allure.step("参数：login={0}")
    def test_updateStatusBatch(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataSchema/updateStatusBatch.json"
        data = dict(dataIds=1, status=9,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("删除 数据元")
    @allure.story("数据元对应的数据")
    @allure.step("参数：login={0}")
    def test_updateStatus2(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataSchema/updateStatus.json"
        data = dict(status=9,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

if __name__ == '__main__':
    pytest.main()