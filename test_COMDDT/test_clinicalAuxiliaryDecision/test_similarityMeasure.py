#!/usr/bin/env python
# --coding:utf-8--
"""
@file: test_similarityMeasure.py
@time: 2019/9/10  11:43
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("相似病例智能分析")
class Test_similarityMeasure:

    # ------------------------------选择与新建患者-----------------------------
    @allure.title("数据库患者列表展示")
    @allure.story("数据库患者列表")
    def test_getPatientList(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getPatientList.json"
        data = dict(userId=response1["authUserId"],
                    page=1, size=10,
                    key="", startDate="", endDate="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_getPatientList(self, response1, cook):
        url = host + port_es + "/similarnew/data/getPatientList.json"
        data = dict(userId=response1["authUserId"],
                    page=1, size=10,
                    key="", startDate="", endDate="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        datadic = {"ids": [], "data": []}
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                datadic["ids"].append(i["INPATIENT_NO"])
                datadic["data"].append(i)
        return datadic

    @allure.title("患者详细信息展示")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_getNewPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getPatientInfo.json"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0], hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "人口学信息")

    @allure.title("数据库患者相似分析设置-权重展示")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_showWeightTemplate(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/showWeightTemplate"
        data = dict(ptType=1,
                    default=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("数据库患者相似分析设置-权重保存修改")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_saveWeightTemplate(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/saveWeightTemplate"
        data = dict(ptType=1,
                    data='{"基本信息":{"num":1,"status":1},"全部诊断":{"num":7,"status":1},"主要诊断":{"num":9,"status":1},'
                         '"临床表现":{"num":9,"status":1},"主诉":{"num":8,"status":1},"现病史":{"num":0,"status":0},"家族史":'
                         '{"num":0,"status":0},"既往史":{"num":0,"status":0},"个人史":{"num":0,"status":0},"检查":'
                         '{"num":0,"status":0},"检验":{"num":0,"status":0}}',
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, "权重配置保存成功")

    @allure.title("数据库相似病例智能分析记录-数据展示")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_getSimilarPatientRecord(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/getSimilarPatientRecord"
        data = dict(ptType=1, page=1, size=10, name="similar",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("相似病例智能分析记录-患者的检查指标数据")
    @allure.story("数据库患者列表")
    @allure.step("参数：login={0}")
    def test_dataGetPatientInfo(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getPatientInfo.json"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0], hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, inpatientNo[0])

    @allure.title("相似病例智能分析记录-患者信息添加到数据库中")
    @allure.story("数据库患者列表")
    @allure.description("这个接口是必须的，要插入的数据库的-临时表中，下一个接口是要使用，以用于查找相似患者")
    def test_generalSimilarityInsertSimilarRecord(self, login, dlogin):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/insertSimilarRecord"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data1 = dict(name="similar", ptType=1, inpatientNo=inpatientNo[0],
                     data='{"基本信息":{"pati_id":"73c80db4-733e-4fd1-894f-34a4896bc134",'
                          '"patient_id":"43B48141A4880976ABBEFFC93AE3A7C5","hospital_code":"12440100455344205E",'
                          '"姓名":"C15D0771741833C9A1BA790818077F60","年龄":64,"性别":"男","居住地":"山西省","是否有ICU转科":0,'
                          '"住院时长":"6","住院总费用":"10328.66","手术费用":"0","病例分型":"疑难","转归":"好转","吸烟史":"有","已戒烟":"有",'
                          '"吸烟持续时间":"20年","吸烟包年":"20"},"诊断":{"主要诊断":"1.双肺肺炎","全部诊断":"1.双肺肺炎 2.慢性阻塞性肺疾病"},'
                          '"入院记录":{"影像描述":"   '
                          '两肺肺纹理增多、紊乱，右中叶、左上肺舌段、两下肺散在斑片、条索影。左上肺尖后段可见条索影及高密度结节影，边界尚清。余两肺透亮度增高，见广泛小叶结构简化改变，两肺弥漫多发无壁、壁薄透亮影；气管、各大支气管通畅。两侧肺门不大，左肺门及纵隔可见多发钙化淋巴结。心影不大。两侧胸腔未见积液，胸膜未见增厚。所见胸廓骨骼未见骨质异常。胸廓软组织未见异常。   扫及胆囊窝见高密度结节影。","入院日期":"2017-02-03","出院日期":"2017-02-09","临床表现":"白痰,发热,寒颤,咳嗽,气促,全身肌肉酸痛","主诉":"发热、气促4天。","现病史":"缘患者4天前无明显诱因下出现发热症状，伴寒颤，最高38.7℃，伴全身肌肉酸痛，伴咳嗽、咳白痰，无黄脓痰，伴活动后气促，无夜间阵发性呼吸困难，无头晕头痛，无恶心呕吐，到东莞市塘厦医院行胸片提示：两肺感染，予静脉滴注“左氧氟沙星0.3g bid”症状无明显缓解，今到我院门诊就诊，门诊拟“肺部感染”收入我科治疗，患者起病后精神、胃纳一般，睡眠尚可，大小便正常，体重无明显变化。","家族史":"家庭成员中无类似疾病、遗传病、传染病等患者","个人史":"无疫区接触史，曾吸烟20余年，20支/日，已戒烟3年。无饮酒史。"},"检验":{"血常规":{"红细胞计数":"正常","血小板计数":"正常","血小板分布宽度":"正常","血小板压积":"正常","淋巴细胞计数":"正常","红细胞分布宽度变异系数":"正常","嗜碱性粒细胞计数":"正常","红细胞平均Hb含量":"正常","红细胞比积":"正常","单核细胞比率":"正常","白细胞总数":"正常","中性粒细胞比率":"正常","血红蛋白":"正常","嗜碱性粒细胞比率":"正常","嗜酸性粒细胞计数":"正常","红细胞平均体积":"升高","嗜酸性粒细胞比率":"正常","红细胞平均Hb浓度":"正常","血小板平均体积":"正常","淋巴细胞比率":"正常","中性粒细胞计数":"正常","单核细胞计数":"正常"},"肝功能检查":{"血清α-L-岩藻糖苷酶测定":"正常","血清白蛋白测定":"正常","血清直接胆红素测定":"正常","血清总胆汁酸测定":"正常","血清总胆红素测定":"正常","血清天门冬氨酸氨基转移酶测定":"正常","血清丙氨酸氨基转移酶测定":"正常","血清γ-谷氨酰基转移酶测定":"正常","血清总蛋白测定":"降低"},"血气分析":{"氧分压（体温）":"降低","二氧化碳分压(体温)":"正常","HCO3-":"降低","氧分压（测定）":"升高","pH值（测定）":"正常","pH值(体温)":"正常","标准碱剩余":"降低","标准碳酸氢根浓度":"正常","氧饱和度（测量）":"降低","二氧化碳分压（测定）":"正常","氧合血红蛋白浓度（测定）":"降低"},"粪便检查":{"粪便白细胞检查":"正常","粪便性状检查":"正常","粪便红细胞检查":"正常"},"糖及其代谢物测定":{"血葡萄糖测定":"正常"},"心肌疾病的实验诊断":{"B型钠尿肽前体（PRO-BNP）测定":"正常","血清肌钙蛋白Ⅰ测定":"正常","血清肌红蛋白测定":"正常"},"凝血及抗凝血检查":{"血清凝血酶原时间测定(PT)":"正常","国际标准化比值(INR)":"正常","凝血酶原时间活动度(PTTA)":"正常","活化部分凝血活酶时间测定(APTT)":"升高","凝血酶时间测定(TT)":"正常"},"酶类检查":{"血清肌酸激酶同工酶测定":"正常"},"肿瘤相关抗原测定":{"糖类抗原测定CA15－3":"正常","糖类抗原测定CA-125":"正常","癌胚抗原测定(CEA)":"正常","神经元特异性烯醇化酶测定(NSE)":"升高"},"无机元素测定（血液样本）":{"钾测定":"正常","氯测定":"正常","钠测定":"正常","钙测定":"正常"},"红细胞沉降率测定(ESR)":{"红细胞沉降率测定(ESR)":"正常"},"纤溶系统检查":{"血浆D-二聚体测定(D-Dimer)-各种免疫学方法":"正常"},"肾脏疾病的实验诊断":{"血肌酐测定":"正常"},"激素测定":{"降钙素原检测(荧光定量法)":"升高"}}}',
                     authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data1, cook, inpatientNo[0])

    @allure.title("由权重找患者--")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_generalSimilartyMathWeight(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/matchWeight"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatientNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[-1],
                    data='{"基本信息":{"num":1,"status":1},"全部诊断":{"num":7,"status":1},"主要诊断":{"num":9,"status":1},'
                         '"临床表现":{"num":9,"status":1},"主诉":{"num":8,"status":1},"现病史":{"num":0,"status":0},'
                         '"家族史":{"num":0,"status":0},"既往史":{"num":0,"status":0},"个人史":{"num":0,"status":0},'
                         '"检查":{"num":0,"status":0},"检验":{"num":0,"status":0}}',
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, response1["hospitalCode"])

    @allure.title("相似患者个数配置")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @pytest.mark.parametrize("size", (10, 20))
    def test_patientPage1(self, login, size):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/patientPage"
        scoreData = congyaml["相似病例分析"]["当前相似患者"]["scoreData"]
        data = {
            "page": 1,
            "size": size,
            "sort": 0,
            "number": 100,
            "scoreData": scoreData,
            "hospitalCode": "YS0001",
            "authUserId": 4400143,
            "authToken": "57be66d24a251449e49ceeaf68c7653d"
        }
        assert_post(url, data, cook)

    @allure.title("导出相似患者列表")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_downloadFile(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/downloadFile"
        scoreData = congyaml["相似病例分析"]["当前相似患者"]["scoreData"]
        data = {
            "scoreData": scoreData
        }
        result = requests.post(url, data, cookies=cook)
        assert result.status_code == 200

    @allure.title("相似患者信息菜单配置")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_getReportGroupList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo="XSG01",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def inpatient_NO(self, response1, cook):
        url = host + port_python + "/generalSimilarity/matchWeight"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        data = dict(inpatientNo=inpatientNo[-1],
                    data='{"基本信息":{"num":1,"status":1},"全部诊断":{"num":7,"status":1},"主要诊断":{"num":9,"status":1},'
                         '"临床表现":{"num":9,"status":1},"主诉":{"num":8,"status":1},"现病史":{"num":0,"status":0},'
                         '"家族史":{"num":0,"status":0},"既往史":{"num":0,"status":0},"个人史":{"num":0,"status":0},'
                         '"检查":{"num":0,"status":0},"检验":{"num":0,"status":0}}',
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.post(url, data, cookies=cook)
        ids = {"key": [], "data": [], "inpatientNo": []}
        if "patientList" in result.text:

            resultdic = json.loads(result.text)["resultData"]
            resultdic1 = resultdic["patientList"]
            resultdic2 = resultdic["localData"]
            for i in resultdic1:
                ids["data"].append(i)
                for k in i.keys():
                    ids["key"].append(k)
            for i in resultdic2:
                ids["inpatientNo"].append(i["inpatient_no"])
        return ids

    def reportNo(self, response1, cook):
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo="XSG01",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        if "reportNo" in result.text:
            resultdic = json.loads(result.text)["responseData"]
            for i in resultdic:
                ids.append(i["reportNo"])
        return ids

    @allure.title("相似患者信息菜单详细的信息设置")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @allure.step("参数：login={0}")
    @pytest.mark.parametrize()
    def test_getReportDatas(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        report = self.reportNo(login[0], login[1])
        reportNo = ""
        for i in report:
            reportNo += i + ","
        inpatient = self.inpatient_NO(login[0], login[1])["key"]
        inpatientNo = ""
        for i in inpatient:
            inpatientNo += i + ","
        allure.attach(f"内部参数：report={report},\ninpatient={inpatient}")
        data = dict(reportNos=reportNo,
                    inPatientNos=inpatientNo,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("相似患者信息菜单详细的信息排序-相似度，转归，入院时间")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @pytest.mark.parametrize("sort", (0, 1, 2))
    def test_patientPage(self, login, sort):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/patientPage"
        socre = self.inpatient_NO(login[0], login[1])["data"]
        socredata = {}
        for i in range(20):
            socredata.update(socre[i])
        sdata = json.dumps(socredata)
        allure.attach(f"内部参数：socre={socre}")
        data = dict(page=1, size=20, sort=sort, number=20,
                    scoreData=sdata,
                    hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("相似患者信息菜单详细的信息排序-治疗路径")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @allure.step("参数：login={0}")
    def test_treatmentPathway(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/treatmentPathway"
        inpatient = self.inpatient_NO(login[0], login[1])["key"]
        inpatientNo = ""
        for i in inpatient:
            inpatientNo += i + ","
        allure.attach(f"内部参数：inpatent={inpatient}")
        data = dict(
            ptList=inpatientNo,
            drugName=2,
            hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("相似患者信息菜单详细的信息排序-患者诊疗时间轴")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    def test_dataGetTimeAxis(self, login):
        response1, cook = login
        url = host + port_es + "/similarnew/data/getTimeAxis.json"
        inpatientNo = self.inpatient_NO(response1, cook)["inpatientNo"]
        allure.attach(f"内部参数：inpatentNo={inpatientNo}")
        data = dict(inpatientNo=inpatientNo[0],
                    hospitalCode=response1["hospitalCode"], authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, inpatientNo[0])

    @allure.title("相似患者信息菜单详细的信息排序-患者对比")
    @allure.story("数据库患者列表")
    @allure.description("这个接口必须要和添加的接口联用")
    @allure.step("参数：login={0}")
    def test_patientContrast(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/patientContrast"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        socre = self.inpatient_NO(login[0], login[1])["data"]
        socredata = {}
        for i in range(2):
            socredata.update(socre[i])
        sdata = json.dumps(socredata)
        allure.attach(f"内部参数：ninpatient={inpatientNo}\nsocre={socre}")
        data = dict(inpatientNo=inpatientNo[1],
                    scoreData=sdata,
                    hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    # @allure.story("患者查询记录-数据展示")
    # @pytest.mark.skip("这个版本没有这个功能")
    # def test_getSimilarRecordDataValue(self, login):
    #     response1, cook = login
    #     url = port_model + "/patient_similar/getSimilarRecordDataValue"
    #     data = dict(startDate="", endDate="",
    #                 # page=1, size=10,
    #                 authUserId=response1["authUserId"], authToken=response1["authToken"])
    #     overWrite_assert_get_xls_hint(url, data, cook, clincalPath, "分页验证  10")

    # ----------------------------新建患者----------------------------------------

    @allure.title("新建患者列表展示-；列表数据")
    @allure.story("新建患者列表")
    @allure.step("参数：login={0}")
    def test_showPatientList(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/showPatientList"
        data = dict(patientName="", name="similar",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def newPatient(self, response1, cook):
        url = host + port_python + "/generalSimilarity/showPatientList"
        data = dict(patientName="", name="similar",
                    page=1, size=10,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["resultData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                pass

    @allure.title("新建患者列表展示-；显示要增加的数据")
    @allure.story("新建患者列表")
    @allure.step("参数：login={0}")
    def test_showBuiltTemplate(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/showBuiltTemplate"
        data = dict(name="similar", inpatientNo="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "基本信息")

    @allure.title("新建患者列表展示-；添加患者信息")
    @allure.story("新建患者列表")
    @allure.step("参数：login={0}")
    def test_insertSimilarRecord(self, login):
        response1, cook = login
        url = host + port_python + "/generalSimilarity/insertSimilarRecord"
        data = dict(name="similar", ptType=0, inpatientNo="",
                    data='{"基本信息":{"姓名":"荀·阿斯蒂","年龄":55,"性别":"男","入院方式":"其他机构转入","居住地":"安徽省","身高":177,"是否有ICU转科":0,'
                         '"住院时长":20,"住院总费用":500,"病例分型":"一般","转归":"治愈"}}',
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.story("写入新建患者数据")
    @allure.step("参数：login={0}")
    def test_insert_simm_record(self, login):
        response1, cook = login
        url = port_model + "/patient_similar/insert_simm_record"
        inpatientNo = self.transfer_getPatientList(response1, cook)["ids"]
        allure.attach(f"内部参数：inpatentNO={inpatientNo}")
        data = dict(record_type=2, data=inpatientNo[0],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.story("去用python统计")
    @allure.step("参数：login={0}")
    def test_findCodeItem(self, login):
        response1, cook = login
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "PYTHON统计")

    def transfer_hostAndPort(self, response1, cook):
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN", itemCode="PYTHON_STATISTIC_DOMAIN",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]["href"]
        return resultdic

    @allure.story("指标的权重值模板")
    @allure.step("参数：login={0}")
    def test_base_template(self, login):
        response1, cook = login
        hosts = self.transfer_hostAndPort(response1, cook)
        url = hosts + "/patient_similar/base_template"
        data = dict(type=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("获取相似指标值列表")
    @allure.step("参数：login={0}")
    def test_getDataIndexValueTreeList(self, login):
        response1, cook = login
        url = host + port_dataindex + "/dataIndex/dataIndexValue/getDataIndexValueTreeList.json"
        data = dict(topCategoryId=3127,
                    operatorId=response1["authUserId"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

if __name__ == '__main__':
    pytest.main(["test_similarityMeasure.py", "-s"])
