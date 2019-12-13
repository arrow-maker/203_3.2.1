# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_medicalAnalysisAesop.py
    Time:    2019/12/10 14:06
    Author:  Arrow
"""
from public.overWrite_Assert import *
from public.Login_Cookies import login_cookies
TitanId = 13587     # 这里是天塔筛选的模板的Id
templateId = 13439  # 模板Id
tempId = 13439      # 探索分析中的变动的Id(keyId 和 templateId)
responseData = 1243

@allure.feature("医索分析Aesop")
class Test_Assop():
    """
    这里还有几个功能没有写：探索分析中还有一点点的功能----算法帮助手册，和菜单的选取（好像每一个的菜单的数据都是不一样的-呵呵），
    上传数据集，
    """

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.title("codeItem")
    @allure.story("数据集管理")
    def test_findCodeItem(self):
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("查询数据")
    @allure.story("数据集管理")
    def test_getDataTemplateList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = dict(templateName="", type=20, status=1,
                    timeStamp=time_up, page=1, size=10,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("显示Titan筛选")
    @allure.story("创建数据集")
    def test_getDataIndexValueTreeList(self):
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="选择住院类型")

    """ 
        上面少了一个天塔筛选功能
        下面的是添加数据集的功能
    """
    @allure.title("天塔筛选-最开始的模板Id")
    @allure.story("创建数据集")
    @allure.step("这里的是添加数据集-先筛选用户-来添加数据集")
    def test_saveDataTemplate_1(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        data = dict(status=2, version=5, groupId=100, dataScope=1, timeScope=0,
                    patientQueryWhere='{"logicSymbol":"and","whereList":[{"logicSymbol":"or","whereType":1,'
                                      '"whereList":[{"logicSymbol":"or","whereList":[{"symbol":"=",'
                                      '"dataValueType":"1","dataId":"462","dataRId":"484","columnValue":"2018-12-11,'
                                      '2019-12-11","columnName":"VISIT_DATE","columnTitle":"入院时间",'
                                      '"columnType":"date","dataName":"入院时间"}]}]}]}',
                    type=0, operatorId=self.authUserId, templateName=f"初始版本{time_up}", indexRule=0,
                    dataIds="2887,248,249,2884,462,463,15524,15523,",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data, self.cook)
        global TitanId
        TitanId = result[1]["responseData"]["templateId"]
        allure.attach(f"输出数据templateId={TitanId}", name="天塔筛选中创建的模板的Id")

    @allure.title("保存数据到数据库")
    @allure.story("创建数据集")
    def test_updateDataTemplate(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateDataTemplate.json"
        data = dict(templateId=TitanId,
                    resultVariables='{"backData":true,"dataWhereVo":{"whereSql":null,"whereDescribe":" ('
                                    '入院时间=2018-12-11 至 2019-12-11 )","includeDescribe":"[\"入院时间=2018-12-11 至 '
                                    '2019-12-11\"]","excludeDescribe":"[]","dataDescribe":"患者姓名,性别,年龄,唯一标识,住院流水号,'
                                    '入院时间,出院时间,主诊断,全部诊断","dataIdList":null,"dataIdRList":null,'
                                    '"dataStoreCountVoList":null,"dataMap":null,"dataRScopeList":null},'
                                    '"isUpdate":true,"inCount":[{"list":[{"total":25874,"count":4093,'
                                    '"changeNum":21781,"scale":"15.82%","whereType":"1","whereSql":"",'
                                    '"countType":"1"},{"total":47026,"count":5820,"changeNum":41206,"scale":"12.38%",'
                                    '"whereType":"1","whereSql":"","countType":"2"}],"whereType":"1",'
                                    '"isActive":false}],"exCount":[],"excludeArr":[],"includeArr":[{'
                                    '"data":"入院时间=2018-12-11 至 2019-12-11","isActive":false}],"description":[{'
                                    '"data":"患者姓名","isActive":false},{"data":"性别","isActive":false},{"data":"年龄",'
                                    '"isActive":false},{"data":"唯一标识","isActive":false},{"data":"住院流水号",'
                                    '"isActive":false},{"data":"入院时间","isActive":false},{"data":"出院时间",'
                                    '"isActive":false},{"data":"主诊断","isActive":false},{"data":"全部诊断",'
                                    '"isActive":false}],"backDataCount":true,"count":[{"list":[{"total":25874,'
                                    '"count":4093,"changeNum":null,"scale":"15.82%","whereType":"0","whereSql":null,'
                                    '"countType":"1"},{"total":47026,"count":5820,"changeNum":null,"scale":"12.38%",'
                                    '"whereType":"0","whereSql":null,"countType":"2"}],"whereType":"0"},'
                                    '{"list":[{"total":25874,"count":4093,"changeNum":21781,"scale":"15.82%",'
                                    '"whereType":"1","whereSql":"","countType":"1"},{"total":47026,"count":5820,'
                                    '"changeNum":41206,"scale":"12.38%","whereType":"1","whereSql":"",'
                                    '"countType":"2"}],"whereType":"1","isActive":false}],"filterData":{"a":{'
                                    '"total":47026,"count":5820,"changeNum":null,"scale":"12.38%","whereType":"0",'
                                    '"whereSql":null,"countType":"2"},"b":{"total":25874,"count":4093,'
                                    '"changeNum":null,"scale":"15.82%","whereType":"0","whereSql":null,'
                                    '"countType":"1"}},"inclusion":[],"exclusion":[],"output":[],"dataScope":"1",'
                                    '"date":{"start":"2018-12-10T16:00:00.000Z","end":"2019-12-10T16:00:00.000Z"},'
                                    '"inHospitalTime":true,"indexRule":0,"paramsData":{"dataIds":"2887,248,249,2884,'
                                    '462,463,15524,15523,","patientQueryWhere":"{\"logicSymbol\":\"and\",'
                                    '\"whereList\":[{\"logicSymbol\":\"or\",\"whereType\":1,\"whereList\":[{'
                                    '\"logicSymbol\":\"or\",\"whereList\":[{\"symbol\":\"=\",\"dataValueType\":\"1\",'
                                    '\"dataId\":\"462\",\"dataRId\":\"484\",\"columnValue\":\"2018-12-11,'
                                    '2019-12-11\",\"columnName\":\"VISIT_DATE\",\"columnTitle\":\"入院时间\",'
                                    '\"columnType\":\"date\",\"dataName\":\"入院时间\"}]}]}]}","dataScope":"1",'
                                    '"operatorId":4467558,"type":0,"timeScope":0,"indexRule":0},'
                                    '"activeDefaultOutput":[{"title":"姓名","isActive":true,"isInHospital":true,'
                                    '"public":true,"dataId":2887},{"title":"性别","isActive":true,"isInHospital":true,'
                                    '"public":true,"dataId":248},{"title":"年龄","isActive":true,"isInHospital":true,'
                                    '"public":true,"dataId":249},{"title":"流水号","isActive":true,"isInHospital":true,'
                                    '"public":true,"dataId":"2884,1379"},{"title":"入院时间","isActive":true,'
                                    '"isInHospital":true,"public":false,"dataId":462},{"title":"出院时间",'
                                    '"isActive":true,"isInHospital":true,"public":false,"dataId":463},{"title":"主诊断",'
                                    '"isActive":true,"isInHospital":true,"public":true,"dataId":15524},'
                                    '{"title":"全部诊断","isActive":true,"isInHospital":true,"public":true,'
                                    '"dataId":15523}]}',    # 这个东西一个版本中可以复用的
                    collect=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("保存数据临模板")
    @allure.story("创建数据集")
    def test_saveDataTemplate(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        data = dict(version=5, templateName="新增数据集3.0",
                    dataIds="2887,248,249,2884,462,463,15524,15523,", dataScope=1,
                    patientQueryWhere='{"logicSymbol":"and","whereList":[{"logicSymbol":"or",'
                                      '"whereType":1,"whereList":[{"logicSymbol":"or","whereList":'
                                      '[{"symbol":"=","dataValueType":"1","dataId":"462","dataRId":"484",'
                                      '"columnValue":"2018-12-10,2019-12-10","columnName":"VISIT_DATE",'
                                      '"columnTitle":"入院时间","columnType":"date","dataName":"入院时间"}]}]}]}',
                    operatorId=self.authUserId, type=20, status=1, remark="实验添加数据", timeScope=0, indexRule=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data=data, cook=self.cook)
        global templateId
        templateId = result[1]["responseData"]["templateId"]
        allure.attach(f"传出的数据Id{templateId}")

    @allure.title("保存数据分析结果")
    @allure.story("创建数据集")
    def test_saveDataAnalysisResult2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataAnalysisResult.json"
        allure.attach(f"内部传参：tmplateId={templateId}")
        data = dict(templateId=templateId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("修改数据库中的模板Id")
    @allure.story("创建数据集")
    def test_updateDataTemplate2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateDataTemplate.json"
        data = dict(templateId=templateId,
                    resultVariables='{"includeDescribe":"入院时间=2018-12-12 至 2019-12-12","excludeDescribe":"",'
                                    '"dataDescribe":"患者姓名,性别,年龄,唯一标识,住院流水号,入院时间,出院时间,主诊断,全部诊断"}',
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("修改数据集名称")
    @allure.story("创建数据集")
    def test_saveDataTemplate3(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        allure.attach(f"内部传参：tmplateId={templateId}")
        data = dict(templateName="新增数据集2.0.1", templateId=templateId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("数据集置顶")
    @allure.story("创建数据集")
    @pytest.mark.parametrize("sequence", (1, 0))
    def test_saveDataTemplate4(self, sequence):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        allure.attach(f"内部传参：tmplateId={templateId}\nswquence={sequence}")
        data = dict(templateId=templateId, sequence=sequence,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("数据集详情")
    @allure.story("创建数据集")
    def test_getDataAnalysisResultList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        allure.attach(f"内部传参：tmplateId={templateId}")
        data = dict(templateId=templateId, page=1, size=10,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def keyId(self, templateName):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        data = dict(type=20, status=2, dataScope=3, templateName=templateName,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data, self.cook)
        tempId = result[1]["responseData"]["templateId"]
        allure.attach(f"传出的数据Id{tempId}")
        return tempId

    @allure.title("保存原始数据集")
    @allure.story("探索性分析")
    def test_saveDataTemplate5(self):
        global tempId
        tempId = self.keyId(f"原始数据{time_up}")

    @allure.title("帮助菜单")
    @allure.story("探索性分析")
    def test_helpManual(self):
        url = host + port_python + "/Algorithm/helpManual"
        assert_get(url, cook=self.cook)

    @allure.title("保存Oracle数据到mongo")
    @allure.story("探索性分析")
    def test_save_oracle_to_mongo(self):
        url = host + port_python + "/save_oracle_to_mongo"
        allure.attach(f"内部传参：tmplateId={templateId}\n key={tempId}")
        data = dict(templateId=templateId, key=tempId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("数据结构-菜单")
    @allure.story("探索性分析")
    def test_getDataTemplateResultColumnList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateResultColumnList.json"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("显示患者数据详情")
    @allure.story("探索性分析")
    def test_getDataAnalysisResultList2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId, page=1, size=10, resultType=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("缺失个案统计")
    @allure.story("探索性分析")
    def test_getDataAnalysisResultList2(self):
        url = host + port_python + "/deal_with_null"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId, stats_na="True",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "normal_table")

    @allure.title("数据分类分析")
    @allure.story("探索性分析")
    def test_Perspective_data(self):
        url = host + port_python + "/Perspective_data"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId, timeStamp=time_up,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="分类指标值转换")

    @allure.title("变量视图")
    @allure.story("探索性分析")
    def test_VariableView(self):
        url = host + port_python + "/VariableView"
        allure.attach(f"内部传参：tmplateId={tempId}")
        param = {"templateId": tempId}
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint="normal_table", params=param)

    """
    下面的是链接到患者全景：应为有全景，这里使用一个接口代替
    """
    @allure.title("患者病例")
    @allure.story("探索性分析")
    @allure.step("患者病例跳转到患者全景")
    def test_getTimeAxisList(self):
        url = host + port_es + "/panorama/data/getTimeAxisList.json"
        data = dict(patiId="YS00017a47a493-3690-4009-8646-491cfd666670",
                    startDate="2013-12-18", endDate="2018-12-26",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    """
    这里面的是菜单栏的选择，有的不能选取所以只写可以写的部分·······
    下面有一个问题：所有的templateId和keyId都是变动的请思考修改数据
    """
    @allure.step("这里是结果分析列表-用于传递结果")
    def resultList(self, dataId):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        allure.attach(f"内部传参：tmplateId={dataId}", name="结果分析中的传值函数")
        data = dict(templateId=dataId, page=1, size=10, resultType=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook)
        resultId = result[1]["responseData"][0]["fieldList"]
        allure.attach(f"中间值resultId={resultId}")
        print(f"\n中间值resultId={resultId}")
        resultId = [x[2:9] for x in resultId]
        return resultId

    @allure.title("异常值处理")
    @allure.story("探索性分析")
    @allure.step("探索性分析中-修改菜单的选择、")
    def test_saveDataTemplate6(self):
        # self.keyId("异常值处理/2")
        pass

    @allure.title("异常值处理-处理结果")
    @allure.story("探索性分析")
    @allure.step("探索性分析中-修改菜单的选择、")
    def test_deal_with_outliers(self):
        keyId = self.keyId("异常值处理/2")           # 数据模板保存
        global tempId
        url = host + port_python + "/deal_with_outliers"
        subsets = self.resultList(tempId)       # 这里是上一次的操作的数据结果
        allure.attach(f"内部传参：tmplateId={tempId}\n key={keyId}\n subsets={subsets}")
        data = {
            "subsets": subsets[2],
            "deal_three_quantile": "True",
            "fillna_type": 0,
            "templateId": tempId,
            "key": keyId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)
        tempId = keyId          # 这里的templateId每经过一次的saveDataTemplate.json接口就改变一次数值

    @allure.title("异常值处理")
    @allure.story("探索性分析")
    @allure.step("探索性分析中-修改菜单的选择、")
    def test_saveDataTemplate6(self):
        # self.keyId("数据转换-连续/2")
        pass

    @allure.title("数据转换-处理结果")
    @allure.story("探索性分析")
    @allure.step("探索性分析中-修改菜单的选择、")
    def test_Descriptive_analysis_continuous_cut_data(self):
        keyId = self.keyId("数据转换-连续/2")    # 修改数据模板
        global tempId
        url = host + port_python + "/Descriptive_analysis_continuous_cut_data"
        subsets = self.resultList(tempId)               # 这里是上一次操作的数据的结果
        allure.attach(f"内部传参：tmplateId={tempId}\n key={keyId}\n subsets={subsets}")
        data = {
            "cut_type": "cut_equwid",
            "cut_k": 4,
            "method": "auto_discrete",
            "subset": subsets[2],
            "templateId": tempId,
            "key": keyId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)
        tempId = keyId                  # 这里的templateId每经过一次的saveDataTemplate.json接口就改变一次数值
    """
    这里只写了两个的数据的选择，没有写别的，这个模块没有开发完全，别的数据还不能选取(只能看，不能操作)，
    """
    @allure.title("可选的主题")
    @allure.story("探索-主题分析保存")
    def test_getAllValueByCate(self):
        url = host + port_sourcedata + "/topic/getAllValueByCate.json"
        data = {
            "propCate": "课题信息",         # 这里是固定的
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "研究目的")

    @allure.title("主题分析并保存")
    @allure.story("探索-主题分析保存")
    def test_saveAndFlush(self):
        url = host + port_sourcedata + "/topic/saveAndFlush.json"
        adddic = {"authUserId": self.authUserId, "authToken": self.authToken}
        data = dict(congyaml['医索分析_主题分析并保存'], **adddic)
        print(f"data={data}")
        result = assert_post(url, data, self.cook)
        global responseData
        responseData = result[1]["responseData"]

    @allure.title("主题分析并保存")
    @allure.story("探索-主题分析保存")
    def test_ktExtendInfoSave(self):
        url = host + port_sourcedata + "/topic/ktExtendInfoSave.json"
        data = dict(mainInfoId=responseData, reportGroupName="异常值处理,异常值处理,异常值处理",
                    reportItemMapJson='[{"chartType":"normal_table","title":"异常值处理记录表","table":{"columns":["变量",'
                                      '"异常个案数","个案异常率","异常值识别方式","异常值处理方式"],"content":[{"变量":"年龄","异常个案数":0,'
                                      '"个案异常率":0,"异常值识别方式":"3倍标准差","异常值处理方式":"删除"}]},"check":true,"isEdit":"false",'
                                      '"desc":"","explain":"","resIndex":0},{"chartType":"hist_figure",'
                                      '"title":"年龄异常值处理前直方图","x-label":"年龄","y-label":"频数","HistData":[{"x":[26,'
                                      '34.111111,42.222222,50.333333,58.444444,66.555556,74.666667,82.777778,'
                                      '90.888889,99],"y":[2,7,9,14,24,17,22,3,2]}],"check":true,"isEdit":"false",'
                                      '"desc":"","explain":"","resIndex":1},{"chartType":"hist_figure",'
                                      '"title":"年龄异常值处理后直方图","x-label":"年龄","y-label":"频数","HistData":[{"x":[26,'
                                      '34.111111,42.222222,50.333333,58.444444,66.555556,74.666667,82.777778,'
                                      '90.888889,99],"y":[2,7,9,14,24,17,22,3,2]}],"check":true,"isEdit":"false",'
                                      '"desc":"","explain":"","resIndex":2}]',
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("数据集删除")
    @allure.story("创建数据集")
    def test_updateStatusBatch(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateStatusBatch.json"
        allure.attach(f"内部传参：tmplateId={templateId}")
        data = dict(status=9, templateIds=templateId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)
