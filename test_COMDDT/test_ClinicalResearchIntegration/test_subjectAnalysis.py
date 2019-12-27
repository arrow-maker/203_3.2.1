#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_subjectAnalysis.py
@time: 2019/9/9  9:16
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("临床科研一体化- 主题分析")
class Test_subjectAnalysis:

    @allure.title("找到python中的代码item")
    @allure.step("参数：login={0}")
    def test_findCodeItem(self, login):
        response1, cook = login
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "SYS_DOMAIN")

    @allure.title("看板列表数据列表")
    @allure.story("看板")
    @allure.step("参数：login={0}")
    def test_mytemplates(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/report/ztfx/mytemplates.json"
        data = dict(orgUserId=response1["authUserId"], templateType="单中心",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "单中心")

    def transfer_mytemplates(self, response1, cook):
        url = host + port_sourcedata + "/report/ztfx/mytemplates.json"
        data = dict(orgUserId=response1["authUserId"], templateType="单中心",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append(i["id"])
        return ids

    @allure.title("默认看板的详细框架的情况")
    @allure.story("看板")
    @allure.step("参数：login={0}")
    def test_templateReports(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/report/ztfx/templateReports.json"
        templateId = self.transfer_mytemplates(response1, cook)
        allure.attach(f"内部参数：templateId={templateId}")
        data = dict(orgUserId=response1["authUserId"], templateId=templateId[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, str(templateId[0]))

    def transfer_template_reports(self, response1, cook):
        url = host + port_sourcedata + "/report/ztfx/templateReports.json"
        templateId = self.transfer_mytemplates(response1, cook)
        data = dict(orgUserId=response1["authUserId"], templateId=templateId[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        ids = []
        if len(resultdic) > 0:
            for i in resultdic:
                # 用于传值的字符串
                idsStr = ""
                if len(i["reports"]) > 0:
                    for j in i["reports"]:
                        idsStr += f'{j["reportNo"]},'  # 数据以字符串的形式转递
                ids.append(idsStr)
        return ids

    @allure.title("默认看板 所有框架 的详细 数据显示 的情况")
    @allure.story("看板")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getReportDatas(self, login, start, end):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        reportNos = self.transfer_template_reports(response1, cook)
        templateId = self.transfer_mytemplates(response1, cook)
        allure.attach(f"内部参数：reportNos={reportNos}\ntemplateId={templateId}")
        if len(reportNos) > 0:
            for i in reportNos:
                reportNosList = re.findall("\\d+", i)  # 这里是 正则表达式 来取出 这一组 中的 数值，用来做断言使用的
                data = dict(hospitalCode=response1["hospitalCode"], reportNos=i,  # 这里默认的是第一个
                            indexTimeStart=start, indexTimeEnd=end, reportIds=templateId[0],
                            authUserId=response1["authUserId"], authToken=response1["authToken"])
                assert_get(url, data, cook, reportNosList[0])

if __name__ == '__main__':
    pytest.main(["-s","-q","--alluredir","./report/test_0909_9"])
