# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_scientificResearchShow.py
    Time:    2019/12/17 10:43
    Author:  Arrow
"""
from public.overWrite_Assert import *
from public.Login_Cookies import login_cookies


@allure.feature("科研成果展示")
class Test_scintificShow():

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.loginName = response["responseData"]["loginName"]

    @allure.title("课题列表和-数据展示")
    @allure.story("科研成果-展示")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getAllTopicDTO(self, start, end):
        url = host + port_sourcedata + "/topic/getAllTopicDTO.json"
        data = {
            "page": 1,
            "size": 10,
            "sort": "desc",
            "startDate": start,
            "endDate": end,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    def DTOList(self):
        url = host + port_sourcedata + "/topic/getAllTopicDTO.json"
        data = {
            "page": 1,
            "size": 10,
            "sort": "desc",
            "startDate": "2019-01-01",
            "endDate": "2019-12-31",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]["content"]
        for i in resultdic:
            ids.append((str(i["ktMainInfo"]["id"]), i["ktMainInfo"]["dataId"]))
        return ids

    """
        这里的新增的科研成果的过程是在AESOP中进行的操作，已经执行过了，
        这里就不重复执行。
    """

    @allure.title("查看课题详情-标记")
    @allure.story("课题数据操作")
    @allure.step("添加科研成果是在医索分析中进行的，已经操作过，这里不重复")
    def test_getHavingNoValueCountByCate(self):
        url = host + port_sourcedata + "/topic/getHavingNoValueCountByCate.json"
        ids = self.DTOList()
        data = {
            "mainInfoId": ids[0][0],
            "propCate": "研究结论",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "操作成功")

    @allure.title("课题信息-课题的详细的数据")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_getAllValueByCate(self):
        url = host + port_sourcedata + "/topic/getAllValueByCate.json"
        ids = self.DTOList()
        data = {
            "mainInfoId": ids[0][0],
            "propCate": "课题信息",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "研究目的")

    @allure.title("课题信息-课题的详细的修改")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_saveAndFlush(self):
        url = host + port_sourcedata + "/topic/saveAndFlush.json"
        ids = self.DTOList()
        kdata = congyaml["科研成果_课题信息编辑"]
        data = {
            "ktMainInfoJson": kdata["ktMainInfoJson1"] % (ids[0][0], self.authUserId, self.loginName, ids[0][1]),
            "propDTOListJson": kdata["propDTOListJson"].__format__(ids[0][0]),
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("数据视图-python数据统计")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_findCodeItem(self):
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = {
            "code": "SYS_DOMAIN",
            "itemCode": "PYTHON_STATISTIC_DOMAIN",
            "authUserId": self.authUserId,
            "authToken": self.authToken,
        }
        assert_get(url, data, self.cook, "SYS_DOMAIN")

    @allure.title("数据视图-查看数据集")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_getDataAnalysisResultList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        ids = self.DTOList()
        data = {
            "templateId": ids[0][1],
            "page": 1,
            "size": 10,
            "resultType": 0,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "全部诊断")

    @allure.title("数据视图-数据概况")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_NewVariableView(self):
        url = host + port_python + "/NewVariableView"
        ids = self.DTOList()
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        param = {"templateId": ids[0][1]}
        assert_post(url, data, self.cook, hint="columns", params=param)

    def variableId(self):
        url = host + port_python + "/NewVariableView"
        ids = self.DTOList()
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        param = {"templateId": ids[0][1]}
        result = requests.post(url, data=data, cookies=self.cook, params=param)
        ids = []
        resultdic = json.loads(result.text)["table"]["content"]
        for i in resultdic:
            ids.append(i["id"])
        return ids

    @allure.title("数据视图-数据概况中的数据分布")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_changeVariable(self):
        url = host + port_python + "/changeVariable"
        ids1 = self.DTOList()
        ids = self.variableId()
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        param = {
            "subset": ids[1],
            "method": 11,
            "templateId": ids1[0][1],
        }
        assert_post(url, data, self.cook, "BarPlot", params=param)

    @allure.title("数据视图-数据处理")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_queryDataProcessByMainInfoId(self):
        url = host + port_sourcedata + "/topic/queryDataProcessByMainInfoId.json"
        ids = self.DTOList()
        data = {
            "mainInfoId": ids[0][0],
            "page": 1,
            "size": 10,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("分析结果-数据展示")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_queryKtExtendInfo(self):
        url = host + port_sourcedata + "/topic/queryKtExtendInfo.json"
        ids = self.DTOList()
        data = {
            "mainInfoId": ids[0][0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "异常值处理")

    def extendId(self):
        url = host + port_sourcedata + "/topic/queryKtExtendInfo.json"
        ids = self.DTOList()
        allure.attach(f"传递接口中的传值{ids}")
        data = {
            "mainInfoId": ids[0][0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"][0]["异常值处理"]
        ids = []
        for i in resultdic:
            ids.append(i["id"])
        return ids

    @allure.title("分析结果-添加图表说明")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_queryKtExtendInfo1(self):
        url = host + port_sourcedata + "/topic/updateTitleNameById.json"
        ids = self.extendId()
        allure.attach(f"\n传值{ids}", name="分析结果-添加图表说明")
        data = {
            "extendInfoId": ids[0],
            "explain": "添加异常处理说明",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("研究结论-数据展示")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_getAllValueByCate1(self):
        url = host + port_sourcedata + "/topic/getAllValueByCate.json"
        ids = self.DTOList()
        data = {
            "mainInfoId": ids[0][0],
            "propCate": "研究结论",
            "authUserId": self.authToken,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "本研究主要发现")

    @allure.title("研究结论-数据编辑修改")
    @allure.story("课题数据操作")
    @allure.step("在有数据的前提下，对科研数据的查看")
    def test_saveAndFlush1(self):
        url = host + port_sourcedata + "/topic/saveAndFlush.json"
        ids = self.DTOList()
        prorjson = congyaml["科研成果_研究结论编辑"]["propDTOListJson"]
        data = {
            "propDTOListJson": prorjson.__format__(ids[0][0]),
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("课题详情-置顶与取消")
    @allure.story("课题数据操作")
    @pytest.mark.parametrize("ontop", (1, 0))
    def test_ontop(self, ontop):
        url = host + port_sourcedata + "/topic/ontop.json"
        ids = self.DTOList()
        data = {
            "mainInfoId": ids[0][0],
            "ontop": ontop,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("课题详情-删除课题")
    @allure.story("课题数据操作")
    # @pytest.mark.skip("这里没有创建，所以关闭了删除")
    def test_deleteByMainInfoId(self):
        url = host + port_sourcedata + "/topic/deleteByMainInfoId.json"
        ids = self.DTOList()
        data = {
            "mainInfoIds": ids[0][0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

if __name__ == '__main__':
    pytest.main()