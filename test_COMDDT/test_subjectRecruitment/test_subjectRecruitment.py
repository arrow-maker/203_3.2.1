#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: test_subjectRecruitment.py
@time: 2019/9/30 13:51
@Author:Terence
"""
from public.Login_Cookies import *
from public.overWrite_Assert import *
potoPath = ""       # 添加图片的路径

@allure.feature("受试者招募")
class Test_subjectRecruitment:

    def setup_class(self):
        response1, self.cook = login_cookies()
        self.authUserId = response1["responseData"]["roleList"][0]["orgUserId"]
        self.authToken = response1["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response1["responseData"]["userName"]

    @allure.story("招募患者列表")
    def test_findPage(self):
        url = host + port_project + "/recruit/project/findPage.json"
        data = dict(
            # page=1, size=10, companyName="", projectName="", createUserName="",     # 创始人
            # cndaNo="",  # CNDA编号
            # drugName="",    # 药物商品名称
            # createDateStart="", createDateEnd="",
            authUserId=self.authUserId, authToken=self.authToken)
        overWrite_assert_get_xls_hint(url, data, self.cook, recrutmentPath, "招募系统查询")

    def transfer_project(self):
        url = host + port_project + "/recruit/project/findPage.json"
        data = dict(
            page=1, size=30, companyName="", projectName="", createUserName="",
            cndaNo="", drugName="", createDateStart="", createDateEnd="",
            authUserId=self.authUserId, authToken=self.authToken)
        ids = []
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        if len(resultdic) > 0:
            for i in resultdic:
                if i["cndaNo"] == "tag":
                    ids.append((i["id"], i["projectName"]))
        return ids

    @allure.story('创建受试者招募系统添加图片')
    def test_uploadFileattachment(self):
        url = host + portlogin + "/common/fileattachment/uploadFileattachment.json"
        file = {'file': open(uploadpath1,'rb')}
        result = assert_post(url, files=file, cook=self.cook)
        global potoPath
        potoPath = result[1]["responseData"]["path"] + result[1]["responseData"]["name"]

    @allure.story('新增招募系统')
    def test_save(self):
        url = host + port_project + "/recruit/project/save.json"
        data = {
            # "companyName": "awerwaer",
            # "projectName": "阿尔瓦若",
            "undefined": "",
            # "projectBeginDate": "2019-09-30",   # 项目的时间
            # "projectEndDate": "2019-10-10",
            # "cndaNo": "",                       # 这个是标记
            # "mobilePhone": 13324245544,         # 手机号
            "qq": "",                           #
            "wechat": "",                       #
            "telephone": "",                    # 座机
            "address": "",                      #
            "patientProvince": "",              # 省市村
            "patientCity": "",                  #
            "patientCounty": "",                #
            # "drugName": "3凤飞飞",               # 商品名称
            "drugAdr": "",                      # 不良反应
            "drugIndication": "",               # 适应症
            "drugUsageDosage": "",              # 用法用量
            "drugContraindication": "",         # 禁忌
            "drugSupplier": "",                 # 厂商
            "drugIngredient": "",               # 成分
            # "projectSubsidy": "法撒旦3432",      # 项目补助情况
            "drugGroupState": "",               # 分组
            "drugMemberState": "",               # 人员
            # "drugTotalMember": 50000,           # 总人数
            # "projectIntroduction": "确认项目",   # 项目简介
            "agreementTemplate": potoPath,    # 上传参数
            "agreementFileName": "生成图片.png",
            # "includeRule": "鹅鹅鹅",           # 纳入规则说明
            "excludeRule": "",                 # 排除规则说明
            "createUserId": self.authUserId,
            "id": "",                           # 当最后两个存在时是修改项目
            "createUserName": ""}
        overWrite_assert_post_xls_hint(url, data, self.cook, recrutmentPath, "新增招募系统")

    @allure.story("项目修改")
    @pytest.mark.parametrize("start,end", searchdate)
    def test_projectChange(self, start, end):
        url = host + port_project + "/recruit/project/save.json"
        data = {
            "companyName": "awerwaer",
            "projectName": "阿尔瓦若",
            "undefined": "",
            "projectBeginDate": start,
            "projectEndDate": end,
            "cndaNo": "",
            "mobilePhone": 13324245544,
            "qq": "",
            "wechat": "",
            "telephone": "",
            "address": "",
            "patientProvince": "",
            "patientCity": "",
            "patientCounty": "",
            "drugName": "3凤飞飞",
            "drugAdr": "",
            "drugIndication": "",
            "drugUsageDosage": "",
            "drugContraindication": "",
            "drugSupplier": "",  # 厂商
            "drugIngredient": "",  # 成分
            "projectSubsidy": "法撒旦3432",      # 项目补助情况
            "drugGroupState": "",  # 分组
            "drugMemberState": "",  # 人员
            "drugTotalMember": 50000,           # 总人数
            "projectIntroduction": "确认项目",   # 项目简介
            "agreementTemplate": potoPath,  # 上传参数
            "agreementFileName": "生成图片.png",
            "includeRule": "鹅鹅鹅",           # 纳入规则说明
            "excludeRule": "",  # 排除规则说明
            "createUserId": self.authUserId,
            "id": "9",  # 当最后两个存在时是修改项目
            "createUserName": self.userName
        }
        assert_post(url, data, self.cook, "更新成功1条数据")

    @allure.story("查看项目的进度条")
    def test_findPage1(self):
        url = host + port_project + "/recruit/patient/findPage.json"
        data = dict(projectId=7,  # 这里是固定的，别的数据没有进度条
                    # page=1, size=10,
                    isAgreement="", searchWord="",
                    authUserId=self.authUserId, authToken=self.authToken)
        overWrite_assert_get_xls_hint(url, data, self.cook, recrutmentPath, "分页验证5")

    @allure.story('查看项目状态')
    def test_getOne(self):
        url = host + port_project + "/recruit/project/getOne.json"
        dicdata = self.transfer_project()
        data = dict(id=dicdata[0][0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, dicdata[0][1])

    @allure.story("删除招募组")
    def test_remove(self):
        url = host + port_project + "/recruit/project/remove.json"
        ids = self.transfer_project()
        if len(ids) > 0:
            for i in ids:   # 每次删除30条记录（含有tag标签）
                data = dict(id=i[0],
                            authUserId=self.authUserId, authToken=self.authToken)
                assert_post(url, data, self.cook, "删除成功")


if __name__ == '__main__':
    pytest.main()