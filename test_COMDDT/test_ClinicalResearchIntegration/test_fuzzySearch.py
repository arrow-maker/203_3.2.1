# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_fuzzySearch.py
    Time:    2019/12/6 17:27
    Author:  Arrow
"""
from public.overWrite_Assert import *
from public.Login_Cookies import login_cookies
#   筛选使用的word
wordchech = ("白", "咳嗽 or 咯血", "干燥综合征", "咳嗽 and 咯血", "咳嗽 or not 咯血"
             "CA620FF036544199B056F77D48AEA9BD", "C112EB45E13A346CB982E6A8ABF2D387",
             "002E00DB360298BA6FF7FD2C5D698BD5", "20159683", "ZY020000625214",
             "干燥综合征 C112EB45E13A346CB982E6A8ABF2D387")

wordSave = ("白", "咳嗽", "干燥综合征", "咯血",
            "CA620FF036544199B056F77D48AEA9BD", "C112EB45E13A346CB982E6A8ABF2D387",
            "002E00DB360298BA6FF7FD2C5D698BD5", "20159683", "ZY020000625214",
            "干燥综合征 C112EB45E13A346CB982E6A8ABF2D387")


@allure.feature("天塔筛选-模糊筛选")
class Test_TitanFuzzySearh():

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.story("筛选-字段")
    @allure.title("模糊搜索")
    def test_nodeGetTree(self):
        url = host + port_patient + "/node/getTree.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "病案首页")

    @allure.story("筛选-来源")
    @allure.title("模糊搜索")
    def test_patientTotal(self):
        url = host + port_patient + "/patient/total.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "操作成功")

    @allure.story("筛选-联想")
    @allure.title("模糊搜索")
    def test_patientSuggest1(self):
        url = host + port_patient + "/patient/suggest.json"
        data = {
            "keyword": "白",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook, "白")

    @allure.story("筛选-收藏")
    @allure.title("模糊搜索")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getDataTemplateList(self, start, end):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = dict(groupId=101, collect=1, page=1, size=5,
                    keyword="", startDate=start, endDate=end,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, "操作成功")

    @allure.story("筛选")
    @allure.title("筛选字段")
    @pytest.mark.parametrize("keyword", wordchech)
    def test_patientSuggest(self, keyword):
        url = host + port_patient + "/patient/suggest.json"
        data = dict(keyword=keyword,
                    authUserId=self.authUserId, authToken=self.authToken)
        allure.attach(f"内部参数：url={url}\ndata={data}", name="筛选")
        hint = "操作成功"
        if keyword == "白":
            hint = "白"
        assert_get(url, data, self.cook, hint)

    @allure.story("添加筛选")
    @allure.title("筛选字段")
    def test_patientSearch(self):
        url = host + port_patient + "/patient/search.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        allure.attach(f"内部参数：url={url}\ndata={data}", name="添加筛选")
        result = requests.options(url, params=data)
        assert result.status_code == 200

    @allure.story("筛选到数据")
    @allure.title("筛选字段")
    @pytest.mark.parametrize("keyword", wordchech)
    def test_patientSearch21(self, keyword):
        url = host + port_patient + "/patient/search.json"
        data = {"page": 1, "size": 10, "keyword": [{"relation": 1, "keyword": keyword, "nodes": []}],
                  "hospitalCode": [], "inpDDeptName": [], "inpInDeptName": [], "clinicInDeptName": [],
                  "sex": [], "age": [], "visitDateBegan": "", "visitDateEnd": "", "dTimeBegan": "",
                  "dTimeEnd": "", "clinicVisitDateBegan": "", "clinicVisitDateEnd": "", "sort": {},
                  "authUserId": self.authUserId, "authToken": self.authToken}
        param = {"authUserId": self.authUserId, "authToken": self.authToken}
        allure.attach(f"\n内部参数：url={url}\ndata={data}", name="筛选到数据")
        hint = keyword
        if " " in keyword:
            hint = keyword[:3]
        result = assert_post(url, json=data, cook=self.cook, params=param, hint=hint)
        #   下面的断言的top 10
        #   疾病top 10
        diseaseList = []
        for i in result[1]["responseData"]["diseaseAggregation"].values():
            diseaseList.append(i["percent"])
        diseaseList = [float(x) for x in diseaseList]
        assert diseaseList == sorted(diseaseList, reverse=True), "疾病"
        #   用药top 10
        medicineList = []
        for i in result[1]["responseData"]["medicineAggregation"].values():
            medicineList.append(i["percent"])
        medicineList = [float(x) for x in medicineList]
        assert medicineList == sorted(medicineList, reverse=True), "用药"
        #   检验top 10
        labList = []
        for i in result[1]["responseData"]["labAggregation"].values():
            labList.append(i["percent"])
        labList = [float(x) for x in labList]
        assert labList == sorted(labList, reverse=True), "检验"
        #   检查top 10
        checkList = []
        for i in result[1]["responseData"]["checkAggregation"].values():
            checkList.append(i["percent"])
        checkList = [float(x) for x in checkList]
        assert checkList == sorted(checkList, reverse=True), "检查"
        #   断言年龄分组
        ageHint = ["[10,20)", "[20,30)", "[30,40)", "[40,50)", "[50,60)", "[60,70)", "[70,80)", "[80,90)", "[90,100)"]
        for i in result[1]["responseData"]["ageAggregation"].keys():
            assert i in ageHint
        #   断言筛选的患者的信息
        for i in result[1]["responseData"]["patientData"]["content"]:
            assert "casesText" in i.keys()      # 患者 主诉
            assert "name" in i.keys()           # 患者 姓名
            assert "sex" in i.keys()            # 患者 性别
            assert "age" in i.keys()            # 患者 年龄
            assert "cases" in i.keys()          # 患者 维度
            twotimelist =[]                     # 二层数据的
            for k in i["cases"]:                # 二层数据
                twotimelist.append(k["dTime"])
                assert "hospital" in k.keys()   # 门诊医院
                assert "dDeptName" in k.keys()  # 门诊科室
                assert "visitDate" in k.keys()  # 入院时间
                assert "dTime" in k.keys()      # 出院时间
                assert "dMainDia" in k.keys()   # 主要诊断
                assert "age" in k.keys()        # 年龄
                for j in k["sourceData"]:
                    assert "value" in j.keys()  # 主要诊断或者出院情况
            # 这个的是二层的时间顺序断言---有点问题
            # twotimelist = [int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))) for x in twotimelist]    # 转化为时间戳
            # assert twotimelist == sorted(twotimelist),    "二层的数据排序"

    @allure.story("保存数据")
    @allure.title("筛选字段")
    @pytest.mark.parametrize("keyword", wordSave)
    def test_saveDataTemplate(self, keyword):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        yamdata = congyaml["模糊搜索"]["保存筛选数据"]
        data = dict(type=0, collect=0, status=2, version=5, groupId=101, operatorId=self.authUserId,
                    templateName=f"模糊搜索{time_up}",
                    resultVariables=yamdata["resultVariables"] % keyword,
                    authUserId=self.authUserId, authToken=self.authToken)
        allure.attach(f"内部参数：url={url}\ndata={data}", name="保存数据")
        assert_post(url, data, self.cook, self.authToken)

    def templateId(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = dict(groupId=101, status=2, page=1, size=5, keyword="",
                    startDate="", endDate="", orderByColumn="createdTime",
                    orderBy="desc", collect=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_get(url, data, self.cook, "操作成功")
        ids = []
        for i in result[1]["responseData"]["content"]:
            ids.append(i["TEMPLATE_ID"])
        return ids

    @allure.story("筛选-历史")
    @allure.title("模糊搜索")
    @pytest.mark.parametrize("keyword", wordSave)
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getDataTemplateList1(self, keyword, start, end):
        url = host + port_dataindex + "/dataIndex/dataTemplate/getDataTemplateList.json"
        data = dict(groupId=101, status=2, page=1, size=5, keyword=keyword,
                    startDate=start, endDate=end, orderByColumn="createdTime",
                    orderBy="desc", collect=0,
                    authUserId=self.authUserId, authToken=self.authToken)
        hint = keyword
        if " " in keyword:
            hint = keyword[:3]
        result = assert_get(url, data, self.cook, hint)
        assert timelocal == result[1]["responseData"]["content"][0]["CREATED_TIME"], "筛选时间"

    @allure.story("筛选-搜索添加收藏")
    @allure.title("模糊搜索")
    @pytest.mark.parametrize("status", (1, 0))
    def test_updateStatus(self, status):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateStatus.json"
        templateId = self.templateId()
        data = dict(templateId=templateId[0], collect=status,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, "操作成功")

    @allure.story("筛选-删除历史")
    @allure.title("筛选历史")
    def test_updateStatus2(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/updateStatus.json"
        templateId = self.templateId()
        data = dict(templateId=templateId[0], status=9,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, templateId[0])


if __name__ == '__main__':
    pytest.main()