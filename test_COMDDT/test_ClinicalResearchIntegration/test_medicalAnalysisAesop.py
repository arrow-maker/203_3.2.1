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
    这里还有几个功能没有写：探索分析中还有一点点的功能----算法帮助手册，
    和菜单的选取（好像每一个的菜单的数据都是不一样的-呵呵），
    上传数据集，
    """

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.title("python统计")
    @allure.severity(A3)
    @allure.story("数据集管理")
    def test_findCodeItem(self):
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("查询数据")
    @allure.severity(A3)
    @allure.story("数据集管理")
    def test_getDataTemplateList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = dict(templateName="", type=20, status=1,
                    timeStamp=time_up, page=1, size=10,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("显示Titan筛选")
    @allure.severity(A3)
    @allure.story("创建数据集-筛选患者")
    def test_getDataIndexValueTreeList(self):
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="选择住院类型")

    """ 
        上面少了一个天塔筛选功能, 这个写到公共模块里了
        下面的是添加数据集的功能
    """
    @allure.title("天塔筛选-最开始的模板Id")
    @allure.severity(A3)
    @allure.story("创建数据集-筛选患者")
    @allure.step("这里的是添加数据集-先筛选用户-来添加数据集")
    def test_saveDataTemplate_1(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        yamdata = congyaml["医索分析"]["天塔筛选"]
        data = dict(status=2, version=5, groupId=100, dataScope=1, timeScope=0,
                    patientQueryWhere=yamdata["patientQueryWhere"],
                    type=0, operatorId=self.authUserId, templateName=f"初始版本{time_up}", indexRule=0,
                    dataIds="2887,248,249,2884,462,463,15524,15523,",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data, self.cook)
        global TitanId
        TitanId = result[1]["responseData"]["templateId"]
        allure.attach(f"输出数据templateId={TitanId}", name="天塔筛选中创建的模板的Id")

    @allure.title("保存数据到数据库")
    @allure.severity(A2)
    @allure.story("创建数据集-筛选患者")
    def test_updateDataTemplate(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateDataTemplate.json"
        yamdata = congyaml["医索分析"]["保存数据到数据库"]
        data = dict(templateId=TitanId,
                    resultVariables=yamdata["resultVariables"],
                    collect=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("保存数据临模板")
    @allure.severity(A2)
    @allure.story("创建数据集-保存数据集")
    def test_saveDataTemplate2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        yamdata = congyaml["医索分析"]["天塔筛选"]
        data = dict(version=5, templateName=f"新增数据集3.0+{num}",
                    dataIds="2887,248,249,2884,462,463,15524,15523,", dataScope=1,
                    patientQueryWhere=yamdata["patientQueryWhere"],
                    operatorId=self.authUserId, type=20, status=1, remark=f"测试流程{num}", timeScope=0, indexRule=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data=data, cook=self.cook)
        global templateId
        templateId = result[1]["responseData"]["templateId"]
        allure.attach(f"传出的数据Id{templateId}")

    @allure.title("保存数据分析结果")
    @allure.severity(A2)
    @allure.story("创建数据集-保存数据集")
    def test_saveDataAnalysisResult(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataAnalysisResult.json"
        allure.attach(f"内部传参：tmplateId={templateId}")
        data = dict(templateId=templateId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("修改数据库中的模板Id")
    @allure.severity(A3)
    @allure.story("创建数据集-保存数据集")
    def test_updateDataTemplate2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateDataTemplate.json"
        yamdata = congyaml["医索分析"]["保存数据到数据库"]
        data = dict(templateId=templateId,
                    resultVariables=yamdata["resultVariables"],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("修改数据集名称")
    @allure.severity(A3)
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
    @allure.severity(A3)
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
    @allure.severity(A2)
    @allure.story("探索性分析")
    def test_saveDataTemplate5(self):
        global tempId
        tempId = self.keyId(f"原始数据{time_up}")

    @allure.title("帮助菜单")
    @allure.severity(A3)
    @allure.story("探索性分析")
    def test_helpManual(self):
        url = host + port_python + "/Algorithm/helpManual"
        assert_get(url, cook=self.cook)

    @allure.title("保存Oracle数据到mongo")
    @allure.severity(A2)
    @allure.story("探索性分析")
    def test_save_oracle_to_mongo(self):
        url = host + port_python + "/save_oracle_to_mongo"
        allure.attach(f"内部传参：tmplateId={templateId}\n key={tempId}")
        data = dict(templateId=templateId, key=tempId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("数据结构-菜单")
    @allure.severity(A3)
    @allure.story("探索性分析")
    def test_getDataTemplateResultColumnList(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateResultColumnList.json"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("显示患者数据详情")
    @allure.severity(A3)
    @allure.story("探索性分析")
    def test_getDataAnalysisResultList2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId, page=1, size=10, resultType=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("缺失个案统计")
    @allure.severity(A3)
    @allure.story("探索性分析")
    def test_deal_with_null(self):
        url = host + port_python + "/deal_with_null"
        allure.attach(f"内部传参：tmplateId={tempId}")
        data = dict(templateId=tempId, stats_na="True",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "normal_table")

    @allure.title("数据分类分析")
    @allure.severity(A3)
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
    @allure.severity(A3)
    @allure.step("患者病例跳转到患者全景")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getTimeAxisList(self, start, end):
        url = host + port_es + "/panorama/data/getTimeAxisList.json"
        data = dict(patiId="YS00017a47a493-3690-4009-8646-491cfd666670",
                    startDate=start, endDate=end,
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
        resultId = [x[2:9] for x in resultId]
        return resultId

    @allure.title("异常值处理-处理结果")
    @allure.severity(A3)
    @allure.story("探索性分析")
    @allure.step("探索性分析中-修改菜单的选择、")
    def test_deal_with_outliers(self):
        keyId = self.keyId("异常值处理/2")
        global tempId
        url = host + port_python + "/deal_with_outliers"
        subsets = self.resultList(tempId)
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
        tempId = keyId

    @allure.title("数据转换-处理结果")
    @allure.severity(A3)
    @allure.story("探索性分析")
    @allure.step("探索性分析中-修改菜单的选择、")
    def test_Descriptive_analysis_continuous_cut_data(self):
        keyId = self.keyId("数据转换-连续/2")
        global tempId
        url = host + port_python + "/Descriptive_analysis_continuous_cut_data"
        subsets = self.resultList(tempId)
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
        tempId = keyId
    """
    这里只写了两个的数据的选择，没有写别的，这个模块没有开发完全，别的数据还不能选取(只能看，不能操作)，
    """
    @allure.title("可选的主题")
    @allure.severity(A2)
    @allure.story("探索-主题分析保存")
    def test_getAllValueByCate(self):
        url = host + port_sourcedata + "/topic/getAllValueByCate.json"
        data = {
            "propCate": "课题信息",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "研究目的")

    @allure.title("主题刷新并保存")
    @allure.severity(A2)
    @allure.story("探索-主题分析保存")
    def test_saveAndFlush(self):
        url = host + port_sourcedata + "/topic/saveAndFlush.json"
        adddic = {"authUserId": self.authUserId, "authToken": self.authToken}
        data = dict(congyaml["医索分析"]['主题刷新并保存'], **adddic)
        print(f"data={data}")
        result = assert_post(url, data, self.cook)
        global responseData
        responseData = result[1]["responseData"]

    @allure.title("主题扩大保存")
    @allure.severity(A3)
    @allure.story("探索-主题分析保存")
    def test_ktExtendInfoSave(self):
        url = host + port_sourcedata + "/topic/ktExtendInfoSave.json"
        yamdata = congyaml["医索分析"]['扩大保存']
        data = dict(mainInfoId=responseData, reportGroupName="异常值处理,异常值处理,异常值处理",
                    reportItemMapJson=yamdata["reportItemMapJson"],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)

    @allure.title("数据集删除")
    @allure.severity(A3)
    @allure.story("创建数据集")
    def test_updateStatusBatch(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateStatusBatch.json"
        allure.attach(f"内部传参：tmplateId={templateId}")
        data = dict(status=9, templateIds=templateId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)


if __name__ == '__main__':
    pytest.main()