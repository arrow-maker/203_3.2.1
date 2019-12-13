# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_fuzzySearch.py
    Time:    2019/12/6 17:27
    Author:  Arrow
"""
from public.overWrite_Assert import *
from public.Login_Cookies import login_cookies


@allure.feature("天塔筛选-模糊筛选")
class Test_TitanFuzzySearh():

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]

    @allure.story("筛选")
    @allure.title("筛选copt")
    def test_patientSuggest(self):
        url = host + port_patient + "/patient/suggest.json"
        data = dict(keyword="copd",
                    authUserId=self.authUserId, authToken=self.authToken)
        allure.attach(f"内部参数：url={url}\ndata={data}", name="筛选")
        assert_get(url, data, self.cook)

    @allure.story("添加筛选")
    @allure.title("筛选copt")
    def test_patientSearch(self):
        url = host + port_patient + "/patient/search.json"
        data = dict(authUserId=self.authUserId, authToken=self.authToken)
        allure.attach(f"内部参数：url={url}\ndata={data}", name="添加筛选")
        result = requests.options(url, params=data)
        assert result.status_code == 200

    @allure.story("筛选到数据")
    @allure.title("筛选copt")
    def test_patientSearch21(self):
        url = host + port_patient + "/patient/search.json"
        data = {"page": 1, "size": 10, "keyword": [{"relation": 1, "keyword": "copd", "nodes": []}],
                  "hospitalCode": [], "inpDDeptName": [], "inpInDeptName": [], "clinicInDeptName": [],
                  "sex": [], "age": [], "visitDateBegan": "", "visitDateEnd": "", "dTimeBegan": "",
                  "dTimeEnd": "", "clinicVisitDateBegan": "", "clinicVisitDateEnd": "", "sort": {},
                  "authUserId": self.authUserId, "authToken": self.authToken}
        param = {"authUserId": self.authUserId, "authToken": self.authToken}
        allure.attach(f"\n内部参数：url={url}\ndata={data}", name="筛选到数据")
        assert_post(url, json=data, cook=self.cook, params=param)

    @allure.story("保存数据")
    @allure.title("筛选copt")
    def test_saveDataTemplate(self):
        url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
        data = dict(type=0, collect=0, status=2, version=5, groupId=101, operatorId=self.authUserId,
                    templateName="模糊搜索1575621761148",
                    resultVariables='{"baseCondition":{"treeData":[],"show":false,"value":"copd","treeValue":"",'
                                    '"selected":[],"nodeIds":[],"isDate":false,"dateValue":"Invalid date"},'
                                    '"otherCondition":[],"patient":{"total":150362,"hit":91962,"percent":"61.16"},'
                                    '"cases":{"total":617330,"hit":359713,"percent":"58.27"}}',
                    authUserId=self.authUserId, authToken=self.authToken)
        allure.attach(f"内部参数：url={url}\ndata={data}", name="保存数据")
        assert_post(url, data, self.cook, "模糊搜索1575621761148")

if __name__ == '__main__':
    pytest.main()