# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    logToFile.py
    Time:    2019/11/20 17:12
    Author:  Arrow
"""
from public.overWrite_Assert import *
from public.Login_Cookies import login_cookies


@allure.feature("天塔筛选")
class Test_TitanFiltrateClass():

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.title("天塔筛选的总人数和病例-数据来源")
    @allure.story("天塔筛选-通用指标")
    def test_getSourceNum(self):
        url = host + port_dataindex + "/dataIndex/dataStore/getSourceNum.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    """
    这两个是最复杂的设计(第二个有七个for循环：伤心)：是使用的pandas(利用行与行之间的关系，行和列之间的关系)
        设计思路是找到所有的行中的某一列值是给定的，这样逐级的筛选找到需要的那一行
        xlrd 这个行之间没有关系，或者找总的行数，非常的不方便
    这里的数据经常会变，一定会用的到，希望会对你有用
    """
    def grayAssert(self, datadic, pandas12):  # 置灰断言
        if list(pandas12["hint"])[0] == "gray":
            assert datadic["isExclude"] is None and datadic["isExport"] is None \
                   and datadic["isInclude"] is None or \
                   datadic["isExclude"] == "0" or datadic["isExport"] == "0" \
                   or datadic["isInclude"] == "0", print("没有-置灰", pandas12)
        else:
            assert datadic["isExclude"] == "1" or datadic["isExport"] == "1" \
                   or datadic["isInclude"] == "1", print("置灰", pandas12)

    @allure.title("天塔筛选的通用指标数据")
    @allure.story("天塔筛选-通用指标")
    def test_getDataIndexValueTreeList(self):
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(topCategoryId=15723,
                    authUserId=self.authUserId, authToken=self.authToken)
        result, resultdic = assert_get(url, data, self.cook)
        resultFrame = resultdic["responseData"][0]["children"]
        ff = pandas_excel("临床指标筛选所有指标.xls", "通用指标")
        for i in resultFrame:
            assert i["title"] in list(ff["case_name"]), print(f'一级指标:{i["title"]}\n{list(ff["case_name"])}')  # 一级断言
            ff2 = ff.copy()
            ff2 = ff2[ff2["case_name"].isin([i["title"]])]
            for j in i["children"]:
                assert j["title"] in list(ff2["data"]), print(f'二级指标:{j["title"]}\n{list(ff2["data"])}', ff2)  # 二级断言
                ff3 = ff2.copy()
                if j["title"] == "肺功能基本信息" or j["title"] == "泌尿系B超检查":
                    for k in j["children"]:
                        ff3 = ff2[ff2["data"].isin([k["title"]])]
                        for m in range(len(k["children"])):
                            try:
                                assert k["children"][m]["title"] == list(ff3["assert"])[m], print(
                                    f'指标{j["title"]}-断言失误', ff3[m:m + 1])  # 三级断言
                            except Exception as e:
                                print(f"数据位置有变动{e}")
                            finally:
                                assert k["children"][m]["title"] in list(ff3["assert"]), print(
                                    f'{j["title"]}\n{list(ff3["assert"])}', ff3[m:m + 2])  # 三级断言
                                self.grayAssert(k["children"][m], ff3[m:m + 1])

                elif j["title"] == "药物使用" or j["title"] == "神经系统疾病":
                    for k in j["children"]:
                        if k["title"] is None:  # 有一个为空的数据
                            k["title"] = "None"
                        elif k["title"] == "脑卒中":
                            k["title"] = "神经系统疾病"
                        ff3 = ff2[ff2["data"].isin([k["title"]])]
                        for m in range(len(k["children"])):
                            try:
                                assert k["children"][m]["title"] == list(ff3["assert"])[m], print(
                                    f'{j["title"]}-断言失误', ff3[m:m + 1])  # 三级断言
                            except Exception as e:
                                print(f"数据位置有变动{e}")
                            finally:
                                assert k["children"][m]["title"] in list(ff3["assert"]), print(
                                    f'{list(ff3["assert"])}-断言失误\n {k["children"][m]["title"]}', ff3[m:m + 1])  # 三级断言
                                self.grayAssert(k["children"][m], ff3[m:m + 1])
                else:
                    ff3 = ff3[ff3["data"].isin([j["title"]])]
                    for k in range(len(j["children"])):
                        assert j["children"][k]["title"] in list(ff3["assert"]), \
                            print(f'{j["children"][k]["title"]}\n三级指标目录断言失误\n{list(ff3["assert"])[k]}', ff3[k:k + 1])  # 三级断言
                        self.grayAssert(j["children"][k], ff3[k:k + 1])

    @allure.title("天塔筛选的专病指标数据")
    @allure.story("天塔筛选-通用指标")
    def test_getDataIndexValueTreeList2(self):
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(type=6,  # 这里好像是固定的
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        resultdic = result[1]["responseData"]
        pandas_data = pandas_excel("临床指标筛选所有指标.xls", "专病指标")
        pandas_data = pandas_data.fillna(value="None")
        for i in range(len(resultdic)):
            assert resultdic[i]["title"] in list(pandas_data["first"])
            pdd1 = pandas_data.copy()
            pdd1 = pdd1[pdd1["first"].isin([resultdic[i]["title"]])]
            idata = resultdic[i]["children"]
            for j in range(len(idata)):
                assert idata[j]["title"] in list(pdd1["second"]), \
                    print(f'二级指标断言:{idata[j]["title"]}\n{list(pdd1["second"])}', pdd1[j: j + 1])  # 二级断言
                # self.grayAssert(idata[j], pdd1[j: j+1])
                pdd2 = pdd1.copy()
                pdd2 = pdd2[pdd2["second"].isin([idata[j]["title"]])]
                jdata = idata[j]["children"]
                for k in range(len(jdata)):
                    assert jdata[k]["title"] in list(pdd2["third"]), \
                        print(f'三级指标断言:{jdata[k]["title"]}\n{list(pdd2["third"])}', pdd2[k: k + 1])  # 三级断言
                    pdd3 = pdd2.copy()
                    pdd3 = pdd3[pdd3["third"].isin([jdata[k]["title"]])]
                    kdata = jdata[k]["children"]
                    if len(kdata) > 0:
                        for l in range(len(kdata)):
                            if kdata[l]["title"] is not None:
                                assert kdata[l]["title"] in list(pdd3["fourth"]), \
                                    print(f'四级指标断言:{kdata[l]["title"]}\n{list(pdd3["fourth"])}', pdd3[l:l + 1])  # 四级断言
                            else:
                                kdata[l]["title"] = "None"
                            pdd4 = pdd3.copy()
                            pdd4 = pdd4[pdd4["fourth"].isin([kdata[l]["title"]])]
                            ldata = kdata[l]["children"]
                            if len(ldata) > 0:
                                for m in range(len(ldata)):
                                    if ldata[m]["title"] is not None:
                                        assert ldata[m]["title"] in list(pdd4["fifth"]),\
                                            print(f'五级指标断言:{ldata[m]["title"]}\n{list(pdd4["fifth"])}', pdd4[m:m + 1])  # 五级断言
                                    else:
                                        ldata[m]["title"] = "None"
                                    pdd5 = pdd4.copy()
                                    pdd5 = pdd5[pdd5["fifth"].isin([ldata[m]["title"]])]
                                    mdata = ldata[m]["children"]
                                    if len(mdata) > 0:
                                        for n in range(len(mdata)):
                                            if mdata[n]["title"] is not None:
                                                assert mdata[n]["title"] in list(pdd5["sixth"]), \
                                                    print(f'六级指标断言:{mdata[n]["title"]}\n{list(pdd5["sixth"])}', pdd5[n:n + 1])  # 六级断言
                                            else:
                                                mdata[n]["title"] = "None"
                                            pdd6 = pdd5.copy()
                                            pdd6 = pdd6[pdd6["sixth"].isin([mdata[n]["title"]])]
                                            ndata = mdata[n]["children"]
                                            if len(ndata) > 0:
                                                for o in range(len(ndata)):
                                                    if ndata[o]["title"] is not None:
                                                        assert ndata[o]["title"] in list(pdd6["seventh"]), \
                                                            print(f'七级指标目录断言:', pdd6[o:o + 1])  # 七级断言
                                                    else:
                                                        ndata[o]["title"] = "None"
                                                    odata = ndata[o]["children"]
                                                    if len(odata) <= 0:
                                                        self.grayAssert(ndata[o], pdd6[o:o + 1])  # 第七级 非目录 置灰
                                            else:
                                                self.grayAssert(mdata[n], pdd5[n:n + 1])  # 第六级 非目录 置灰
                                    else:
                                        self.grayAssert(ldata[m], pdd4[m:m + 1])  # 第五级 非目录 置灰
                            else:
                                self.grayAssert(kdata[l], pdd3[l:l + 1])  # 第四级 非目录 置灰
                    else:
                        self.grayAssert(jdata[k], pdd2[k: k + 1])  # 第三级 非目录 置灰

    @allure.title("查看疾病ICD编码")
    @allure.story("天塔筛选-通用指标")
    @pytest.mark.parametrize("dataId", (4162, 3294, 1565))
    def test_saveDataTemplate(self, dataId):
        url = host + port_dataindex + "/dataIndex/synonym/geSynonymTreeList.json"
        data = {
            "dataId": dataId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)


    # 用于保存临时数据的Id，筛选的
    global templateId
    templateId = 12632

    @allure.title("保存筛选数据")
    @allure.story("天塔筛选-通用指标")
    def test_saveDataTemplate(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        yamdata = congyaml["天塔筛选"]["保存筛选数据"]
        data = dict(status=2, version=5, groupId=100, dataScope=1, timeScope=0,
                    patientQueryWhere=yamdata["patientQueryWhere"],
                    type=0, operatorId=self.authUserId, templateName=f"初始版本{time_up}", indexRule=0,
                    dataIds="2887,248,249,2884,462,463,15524,15523,",
                    authUserId=self.authUserId, authToken=self.authToken)
        result, resultdic = assert_post(url, data, self.cook)
        global templateId
        templateId = resultdic["responseData"]["templateId"]

    @allure.title("保存筛选数据的数据统计分析")
    @allure.story("天塔筛选-通用指标")
    def test_getDataAnalyzeCount(self):
        url = host + port_dataindex + "/dataIndex/dataStore/getDataAnalyzeCount.json"
        global templateId
        allure.step(f"内部参数：templateId={templateId}")
        data = dict(templateId=templateId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "list")

    @allure.title("保存筛选数据")
    @allure.story("天塔筛选-通用指标")
    def test_getDataAnalysisResultList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        global templateId
        allure.step(f"内部参数：templateId={templateId}")
        data = dict(templateId=templateId, page=1, size=10, resultType=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("筛选收藏")
    @allure.story("天塔筛选-通用指标")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getDataTemplateList(self, start, end):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = {
            "groupId": 100,
            "collect": 1,
            "page": 1,
            "size": 5,
            "keyword": "",
            "startDate": "",
            "endDate": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("筛选历史")
    @allure.story("天塔筛选-通用指标")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getDataTemplateList2(self, start, end):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = {
            "groupId": 100,
            "status": 2,
            "page": 1,
            "size": 5,
            "keyword": "",
            "startDate": start,
            "endDate": end,
            "orderByColumn": "createdTime",
            "orderBy": "desc",
            "collect": 0,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("筛选添加收藏指标")
    @allure.story("天塔筛选-通用指标")
    def test_saveDataQueryGroup2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataQueryGroup.json"
        patientQuery = congyaml["天塔筛选"]["收藏指标"]["patientQueryWhere"]
        data = {
            "operatorId": self.authUserId,
            "groupName": "性别指标",
            "whereType": 1,
            "patientQueryWhere": patientQuery,
            "categoryId": 15723,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, "性别指标")

    @allure.title("筛选结果导出")
    @allure.story("天塔筛选-通用指标")
    def test_exportDataAnalysisResult(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/exportDataAnalysisResult.json"
        data = {
            "templateId": templateId,
            "resultType": 0,
            "dataScope": 1,
            "operatorId": self.authUserId,
            "operatorFunction": "54246-exportLungvalue",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        assert result.status_code == 200


if __name__ == '__main__':
    pytest.main()
