# -*- coding: utf-8 -*-
# encoding=utf-8
from public.overWrite_Assert import *


@allure.feature("患者主索引")
class Test_patientMasterIndex:

    @allure.title("患者主索引 平台主患者 列表")
    @allure.story("平台主患者")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_findAllPage(self, login, start, end):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/findAllPage.json"
        data = dict(page=1, size=15, status=1, idCard="", mobilePhone="", name="",
                    operatorId=response1["authUserId"], startDate=start, endDate=end,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, "content")

    @allure.title("患者主索引 平台主患者 列表")
    @allure.story("平台主患者")
    def transfer_AllPage(self, response1, cook):
        url = host + port_primaryIndex + "/identifier/findAllPage.json"
        data = dict(page=1, size=15,
                    status=1, idCard="", mobilePhone="", name="",
                    operatorId=response1["authUserId"], startDate="", endDate="",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultDic = json.loads(result.text)["responseData"]["content"]
        dicdata = {"ids": []}
        if "SUCCESS" in result.text:
            if len(resultDic) > 0:
                for i in resultDic:
                    dicdata["ids"].append(i["id"])
        return dicdata

    @allure.title("患者详情-基本信息")
    @allure.story("平台主患者")
    def test_findManualMergeList(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/findManualMergeList.json"
        dicdata = self.transfer_AllPage(response1, cook)["ids"]
        allure.attach(f"内部参数：identifierId={dicdata}")
        data = dict(identifierId=dicdata[1],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, str(dicdata))

    @allure.title("患者详情-合并记录-源记录")
    @allure.story("平台主患者")
    def test_getManualSourceData(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/getManualSourceData.json"
        ids = self.transfer_AllPage(response1, cook)["ids"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(identifierId=ids[2],
                    mergeId="",
                    # page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath,"分页验证5")

    @allure.title("患者详情-近似记录列表")
    @allure.story("平台主患者")
    def test_findWaitList(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/findWaitMergeList.json"
        ids = self.transfer_AllPage(response1, cook)["ids"]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(identifierId=ids[2],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook, str(ids))

    @allure.title("患者详情-近似记录列表")
    @allure.story("平台主患者")
    def transfer_WaitList(self,response1, cook):
        url = host + port_primaryIndex + "/identifier/findWaitMergeList.json"
        ids = self.transfer_AllPage(response1, cook)["ids"][2]
        allure.attach(f"内部参数：ids={ids}")
        data = dict(identifierId=ids,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultDic = json.loads(result.text)["responseData"]
        dicData = {"compareId": [], "mergeId": []}
        if "SUCCESS" in result.text:
            if len(resultDic) > 0:
                for i in resultDic:
                    if "mergeId" in i and "compareId" in i:
                        dicData["compareId"].append(i["compareId"])
                        dicData["mergeId"].append(i["mergeId"])
        return dicData

    @allure.title("患者详情-近似记录-源记录")
    @allure.story("平台主患者")
    def test_getWaitSourceData(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/getWaitSourceData.json"
        dicdata = self.transfer_WaitList(response1, cook)
        if len(dicdata["compareId"]) > 0:
            identifierId = dicdata["compareId"][0]
            mergeId = dicdata["mergeId"][0]
        else:
            identifierId = 1099792
            mergeId = 194045
        allure.attach(f"内部参数：mergeId={mergeId}\n identifierId={identifierId} \n dicdata={dicdata}")
        data = dict(identifierId=identifierId,
                    mergeId=mergeId,
                    # page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证5")

    @allure.title("患者详情-近似记录-合并")
    @allure.story("平台主患者")
    def test_empiMerge(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/empi/merge.json"
        dicdata = self.transfer_WaitList(response1, cook)
        if len(dicdata["compareId"]) > 0:
            identifierId = dicdata["compareId"][0]
            mergeId = dicdata["mergeId"][0]
        else:
            identifierId = 1099792
            mergeId = 194045
        allure.attach(f"内部参数：identifierId={identifierId}\n mergeId={mergeId}\n dicdata={dicdata}")
        data = dict(identifierId=identifierId,
                    mergeId=mergeId,
                    operatorId=response1["userId"],
                    operatorName=response1["roleName"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者详情-近似记录-解除与患者的近似关系")
    @allure.story("平台主患者")
    def test_empBreakAllMerge(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/empi/breakAllMerge.json"
        dicdata = self.transfer_WaitList(response1, cook)
        if len(dicdata["compareId"]) > 0:
            identifierId = dicdata["compareId"][0]
            mergeId = dicdata["mergeId"][0]
        else:
            identifierId = 1102613
            mergeId = 194045
        allure.attach(f"内部参数：identifierId={identifierId}\n docdata={dicdata}")
        data = dict(identifierId=identifierId,  # 1102613
                    operatorId=response1["userId"],
                    operatorName=response1["roleName"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者详情-合并记录-解除合并")
    @allure.story("平台主患者")
    def test_empiUnmerge(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/empi/unmerge.json"
        dicdata = self.transfer_WaitList(response1, cook)
        if len(dicdata["compareId"]) > 0:
            identifierId = dicdata["compareId"][0]
            mergeId = dicdata["mergeId"][0]
        else:
            identifierId = 1102613
            mergeId = 194045
        allure.attach(f"内部参数：mergeId={mergeId}\n dicdata={dicdata}")
        data = dict(mergeId=mergeId,
                    operatorId=response1["userId"],
                    operatorName=response1["roleName"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者主索引 近似记录")
    @allure.story("近似记录")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_findProcessPage(self, login, start, end):
        response1, cook = login
        url = host + port_primaryIndex + "/identifier/findProcessPage.json"
        data = dict(status=1,
                    operatorId=response1["authUserId"],
                    idCard="", name="",
                    startDate=start, endDate=end,
                    # page=1, size=15,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证5")

    @allure.title("患者主索引 主索引配置 数据展示")
    @allure.story("患者主索引配置")
    def test_index_findIndexScoreDetailList(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/index/findIndexScoreDetailList.json"
        data = dict(status=1,
                    # page=1, size=10,
                    name="", hospitalCode="default",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        overWrite_assert_get_xls_hint(url, data, cook, researchCatePath, "分页验证5")

    @allure.title("主索引配置 新增主索引")
    @allure.story("患者主索引配置")
    def test_index_saveIndexScoreDetail(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/index/saveIndexScoreDetail.json"
        data = dict(status="", configId=14,
                    score=5, hospitalCode="default",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook, "唯一标识已经存在！")

    @allure.title("主索引配置 主索引删除")
    @allure.story("患者主索引配置")
    def test_index_deleteScoreDetail(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/index/deleteScoreDetail.json"
        data = dict(id=14,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.title("患者主索引  合并原则")
    @allure.story("患者主索引配置")
    def test_index_findIndexScoreRangeList(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/index/findIndexScoreRangeList.json"
        data = dict(status=1, hospitalCode="default",
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.title("患者主索引  合并原则保存")
    @allure.story("患者主索引配置")
    def test_index_upDataScoreRange(self, login):
        response1, cook = login
        url = host + port_primaryIndex + "/index/updateScoreRange.json"
        data = dict(min=45, max=80,
                    runDate="13:12", id=1,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)


if __name__ == '__main__':
    pytest.main()