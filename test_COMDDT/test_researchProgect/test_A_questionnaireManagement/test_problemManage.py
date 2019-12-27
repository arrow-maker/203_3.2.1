from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("科研项目管理->问题管理类")
class Test_problemManage:

    def setup_class(self):
        self.response, self.cook = login_cookies()
        self.authUserId = self.response["responseData"]["roleList"][0]["orgUserId"]  # 用户的id
        self.authToken = self.response["responseData"]["roleList"][0]["orgUserIdToken"]  # 用户的token值
        self.hospitalCode = self.response["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = self.response["responseData"]["roleList"][0]["orgId"]
        self.userName = self.response["responseData"]["userName"]

    @allure.title("系统预设问题菜单展示")
    @allure.story("问题管理")
    def test_systemDefaultProblemMenu(self):
        url = host + port_qt + "/qtItemCategory/findQtItemCategory"
        params = {
            # "name": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, params, self.cook, researchCatePath, "问题管理-题库查询")

    def parentId(self):
        url = host + port_qt + "/qtItemCategory/findQtItemCategory"
        params = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, params, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]
        ids = []
        for i in resultdic:
            if i["id"] > 10000:
                ids.append(i["id"])
        return ids

    @allure.title("系统预设问题菜单新增题库")
    @allure.story("问题管理")
    def test_systemDefaultProblemMenuAdd(self):
        url = host + port_qt + "/qtItemCategory/saveQtItemCategory"
        data = {  # （必填项，）
            # "name":"新增题库1",
            # "parentId": parentId,
            # "rank":1,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "问题管理-新增题库")

    @allure.title("系统预设问题菜单新增题库的子题库")
    @allure.story("问题管理")
    def test_systemDefaultProblemMenuAdd2(self):
        url = host + port_qt + "/qtItemCategory/saveQtItemCategory"
        parentId = self.parentId()
        if len(parentId) > 0:
            data = {
                "name":"新增题库001-2",
                "parentId": parentId[0],
                "rank": 2,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook, str(parentId[0]))

    @allure.title("系统预设问题展示")
    @allure.story("问题管理")
    def test_findQtItem(self):
        url = host + port_qt + "/qtItem/findQtItemPage"
        param = {
            # "categoryId": 10005000900040000901,
            # "rank": 1,
            # "text":"",
            # "page":1,
            # "size":15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, param, self.cook, researchCatePath, "问题管理-问题展示")

    @allure.title("问卷列表")
    @allure.story("问题管理")
    def transfer_QtItem(self):
        url = host + port_qt + "/qtItem/findQtItemPage"
        param = {
            "categoryId": 0,
            "rank": 1,
            "text": "",
            "page": 1,
            "size": 15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, param, cookies=self.cook)
        resultDic = json.loads(result.text)["responseData"]["content"]
        ids = []
        if "SUCCESS" in result.text:
            for i in resultDic:
                ids.append(i["id"])
        return ids

    @allure.title("系统问题菜单展示（类的方法）")
    @allure.story("问题管理")
    def transfer_problemMenu(self):
        url = host + port_qt + "/qtItemCategory/findQtItemCategory"
        params = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, params, cookies=self.cook)
        resultDic = json.loads(result.text)["responseData"]
        dicData = {"id": [], "rank": []}
        for i in resultDic:
            if i["id"] > 100000:
                dicData["id"].append(i["id"])
                dicData["rank"].append(i["rank"])
                for j in i["childList"]:
                    dicData["id"].append(j["id"])
                    dicData["rank"].append(j["rank"])
        return dicData

    @allure.title("问题管路->问题分类->添加问题")
    @allure.story("问题管理")
    def test_addquestion(self):
        url = host + port_qt + "/qtItem/saveItem.json"
        yamdata = congyaml["问题管理"]["添加问题分类"]
        data = {
            "content": yamdata["content"],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问卷管理->问题模板->问题预览")
    @allure.story("问题管理")
    def test_questionPreview(self):
        url = host + port_qt + "/qtItemRegex/findQtItemRegex"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("问题移动，不同的问题库")
    @allure.story("问题管理")
    def test_questionMove(self):
        url = host + port_qt + "/qtItem/addToNewCategory"
        dicData = self.transfer_problemMenu()
        ids = self.transfer_QtItem()
        allure.attach(f"内部参数：dicdata={dicData}\n ids={ids}")
        data = {
            "categoryId": dicData["id"][0],
            "id": ids[0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问题管理->验证规则-规则列表（查询接口）")
    @allure.story("验证规则")
    def test_RuleSearch(self):
        url = host + port_qt + "/regexCategory/findRegexCategory"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, data, self.cook, researchCatePath, "问题管理-规则分类展示")

    @allure.title("验证规则 规则列表")
    @allure.story("验证规则")
    def transfer_ruleSearch(self):
        url = host + port_qt + "/regexCategory/findRegexCategory"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        resultDic = json.loads(result.text)["responseData"]
        ids = []
        if "SUCCESS" in result.text:
            for i in resultDic:
                ids.append(i["id"])
        return ids

    @allure.title("问题管理->验证规则-规则列表-新增验证规则")
    @allure.story("验证规则")
    def test_manageRule_verifyAddNew(self):
        url = host + port_qt + "/regexCategory/saveRegexCategory"
        data = {
            # "name":"姥姥拉拉",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "问题管理-规则列表-新增验证规则")

    @allure.title("问题管理->验证规则-规则列表 删除验证规则")
    @allure.story("验证规则")
    def test_manageRule_verifyDelectNew(self):
        url = host + port_qt + "/regexCategory/removeRegexCategory"
        ids = self.transfer_ruleSearch()
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[1],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问题管理->规则列表")
    @allure.story("验证规则")
    def test_ruleName(self):
        url = host + port_qt + "/regexCategory/findRegexCategory"
        data = {
            # "name":"",
            # "categoryId":1000001,
            # "page":1,
            # "size":15,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_get_xls_hint(url, data, self.cook, researchCatePath, "问题管理-详细规则展示")

    @allure.title("规则目录中的详细的规则")
    @allure.story("验证规则")
    def transfer_QtItemRegex(self):
        url = host + port_qt + "/regexCategory/findRegexCategory"
        data = {
            "name": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = requests.get(url, data, cookies=self.cook)
        ids = []
        resultDic = json.loads(result.text)["responseData"]
        if "SUCCESS" in result.text:
            for i in resultDic:
                print(i["id"])
                ids.append(i["id"])
        return ids

    @allure.title("问题管理->规则列表 新增规则（修改规则）")
    @allure.story("验证规则")
    def test_ruleName_addNew(self):
        url = host + port_qt + "/regexCategory/saveRegexCategory"
        data = {
            # "name":"热特热他的12343特热他的光和热1",
            # "description":"描述",
            # "regex":"正则式",
            # "msg":"验证不通过弹出文字",
            # "categoryId":1000001,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "问题管理-规则列表-新增规则")

    @allure.title(" 删除问题")
    @allure.story("问题管理")
    def test_questionDelect(self):
        url = host + port_qt + "/qtItem/removeItem"
        ids = self.transfer_QtItem()
        allure.attach(f"内部参数：ids={ids}")
        data = {
            "id": ids[0],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问题模板->题库删除")
    @allure.story("问题管理")
    def test_delectQuestion(self):
        url = host + port_qt + "/qtItemCategory/removeQtItemCategory"
        firstQuestion = self.transfer_problemMenu()
        ids = firstQuestion["id"]
        rank = firstQuestion["rank"]
        allure.attach(f"内部参数：ids={ids} \n   rank={rank}")
        for i in range(len(ids)):
            data = {
                "id": ids[i],
                "rank": rank[i],
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook)

    @allure.title("问题管理->规则列表 删除规则")
    @allure.story("验证规则")
    def test_ruleName_delectNew(self):
        url = host + port_qt + "/regexCategory/removeRegexCategory"
        ids = self.transfer_QtItemRegex()
        allure.attach(f"内部参数： ids={ids}")
        for i in ids:
            if i > 1000000:
                data = {
                    "id": i,
                    "authUserId": self.authUserId,
                    "authToken": self.authToken
                }
                assert_post(url, data, self.cook)


if __name__ == '__main__':
    pytest.main()