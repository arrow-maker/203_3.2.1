#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_wordCloudAnalysis.py
@time: 2019/9/10  10:17
@Author:Terence
"""

from public.overWrite_Assert import *


@allure.feature("数据挖掘-词云分析")
class Test_wordCloudAnalysis:

    @allure.title("调用python接口，为下面的接口调取资源")
    @allure.story("词云分析")
    @allure.severity(A3)
    @allure.step("参数：login={0}")
    def test_findCodeItem(self, login):
        response1, cook = login
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"],authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_hostAndPort(self, response1, cook):
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        hrt = resultdic["href"]
        return hrt

    @allure.title("请求查询的下拉框 的资源")
    @allure.story("词云分析")
    @allure.severity(A3)
    @allure.step("参数：login={0}")
    def test_worldCloudTop(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/worldCloudTop"
        allure.attach(f"内部参数：hosts={hosts}")
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("词云 文献 信息")
    @allure.story("词云分析")
    @allure.severity(A3)
    @allure.step("参数：login={0}")
    def test_worldCloud(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/worldCloud"
        allure.attach(f"内部参数：host={hosts}")
        data = dict(
            page=1, pagesize=20,
            timeFilter=0,
            query="",
            queryType="",
            jourName="BMJ.",
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("词云频率")
    @allure.story("词云分析")
    @allure.severity(A3)
    @allure.step("参数：login={0}")
    def test_worldCloudFrequency(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/worldCloudFrequency"
        allure.attach(f"内部参数：host={hosts}")
        data = dict(page=1, pagesize=200,
                    timeFilter=0, query="", queryType="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("词云 作者")
    @allure.story("词云分析")
    @allure.step("参数：login={0}")
    def test_worldCloudAuthor(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/worldCloudAuthor"
        allure.attach(f"内部参数：host={hosts}")
        data = dict(top=20,
                    timeFilter=0, query="", queryType="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("词云 作者单位")
    @allure.story("词云分析")
    @allure.step("参数：login={0}")
    def test_worldCloudAuthor_info(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/worldCloudAuthor_info"
        allure.attach(f"内部参数：host={hosts}")
        data = dict(top=20,
                    timeFilter=0, query="", queryType="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)