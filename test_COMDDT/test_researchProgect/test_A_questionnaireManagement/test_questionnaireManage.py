from public.Login_Cookies import *
from public.overWrite_Assert import *


@allure.feature("科研项目管理->问卷管理类")
class Test_questionManage:

    def setup_class(self):
        self.response, self.cook = login_cookies()
        self.authUserId = self.response["responseData"]["roleList"][0]["orgUserId"]  # 用户的id
        self.authToken = self.response["responseData"]["roleList"][0]["orgUserIdToken"]  # 用户的token值
        self.hospitalCode = self.response["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
        self.orgId = self.response["responseData"]["roleList"][0]["orgId"]
        self.userName = self.response["responseData"]["userName"]

    @allure.title("问卷列表 展示")
    @allure.story("问卷管理")
    def test_questionlist(self):
        url = host + port_qt + "/qtInfo/findQtInfoList.json"
        data = {
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("问卷展示列表")
    @allure.story("问卷管理")
    def transfer_questionlist(self):
        url = host + port_qt + "/qtInfo/findQtInfoList.json"
        data = {
            "operatorId": self.authUserId,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        result = assert_get(url, data, self.cook)
        resultDic = result[1]["responseData"]
        dicData = {"myself":  [[]], "share":  []}
        for i in resultDic["myself"]:
            if "qtInfoList" not in i.keys():
                dicData["myself"].append(i["id"])
            else:
                for k in i["qtInfoList"]:
                    dicData["myself"][0].append(k["qtId"])
        for i in resultDic["share"]:
            dicData["share"].append(i["qtId"])
        return dicData

    @allure.title("问卷列表->新增模块")
    @allure.story("问卷管理")
    def test_addNewMy(self):
        url = host + port_qt + "/qtInfoCategory/saveQtInfoCategory"
        data = {
            # "name":"系统预设模块三",
            "hospitalCode": self.hospitalCode,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "问卷列表->新增模块")

    @allure.title("问卷列表->新增问卷")
    @allure.story("问卷管理")
    def test_addNewQuestionnaire(self):
        url = host + port_qt + "/qtInfo/saveQtInfo.json"
        data = {
            "orgId": self.orgId,
            # "categoryId":1000048,
            # "title":"天热一天给电饭锅韩国123452",
            "operatorId": self.authUserId,
            "hospitalCode": self.hospitalCode,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        overWrite_assert_post_xls_hint(url, data, self.cook, researchCatePath, "问卷列表->新增问卷")

    @allure.title("问卷列表->新增问卷->问卷新增题库 保存")
    @allure.story("问卷管理")
    def test001_addQuestionModel(self):
        url = host + port_qt + "/qtInfo/saveQtContent.json"
        ids = self.transfer_questionlist()["myself"]
        allure.attach(f"内部参数：ids={ids}")
        yamdata = congyaml["问卷管理"]["新增题库保存"]
        data = {
            "id": ids[0][0],
            "serialize": yamdata["serialize"],
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问卷列表->新增问卷->问卷新增题库 发布")
    @allure.story("问卷管理")
    def test_releaseQuestionModel(self):
        url = host + port_qt + "/qtInfo/release.json"
        ids = self.transfer_questionlist()["myself"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = {
                "id": ids[0][0],
                "reason": "发布原因",
                "userName": self.userName,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook)

    @allure.title("问卷设置  适应App的没有做 -点击分享")
    @allure.story("问卷管理")
    def test_share(self):
        url = host + port_qt + "/qt/share/saveInfo.json"
        ids = self.transfer_questionlist()["share"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = {
                "qtId": ids[0],
                "shareScope": 3,
                "shareOrg": '[]',
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook)

    @allure.title("问卷管理->题库列表搜索-》问题的种类")
    @allure.story("问卷管理")
    def test_information(self):
        url = host + port_qt + "/qtItem/findAllShowType"
        data = {
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("问卷的详细内容")
    @allure.story("问卷管理")
    def test_informationDetails(self):
        url = host + port_qt + "/qtInfo/getQtContent.json"
        ids = self.transfer_questionlist()["share"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 0:
            data = {
                "id": ids[0],
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_get(url, data, self.cook, "text")

    @allure.title("查找医院的信息")
    @allure.story("问卷管理")
    def test_findHistoryList(self):
        url = host + port_qt + "/qtInfo/findHistoryList.json"
        ids = self.transfer_questionlist()["share"]
        if len(ids) > 0:
            data = {
                "qtId": ids[0],
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_get(url, data, self.cook)

    @allure.title("问卷模板->问卷列表->删除")
    @allure.story("问卷管理")
    def test_deleteNewMy(self):
        url = host + port_qt + "/qtInfoCategory/removeQtInfoCategory"
        ids = self.transfer_questionlist()["myself"]
        allure.attach(f"内部参数：ids={ids}")
        if len(ids) > 1:
            for i in ids:
                if type(i) is not list:
                    data = {
                        "id": i,
                        "authUserId": self.authUserId,
                        "authToken": self.authToken
                    }
                    assert_post(url, data, self.cook)


if __name__ == '__main__':
    pytest.main()