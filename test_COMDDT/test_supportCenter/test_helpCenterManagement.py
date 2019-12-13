# !/usr/bin/python
# -*- coding:utf-8 -*-
"""
    File:    test_helpCenterManagement.py
    Time:    2019/11/29 15:21
    Author:  Arrow
"""
from public.Login_Cookies import login_cookies
from public.overWrite_Assert import *

manualId = 23  # 用户手册的数据ID
troubleId = 22  # 问题管理的数据ID
editionId = 61  # 版本的数据ID


@allure.feature("帮助中心管理")
class Test_helpCenterManagement:

    def setup_class(self):
        response, self.cook = login_cookies()
        self.authUserId = response["responseData"]["roleList"][0]["orgUserId"]  # 获取用户登录的id
        self.authToken = response["responseData"]["roleList"][0]["orgUserIdToken"]
        self.userName = response["responseData"]["userName"]

    @allure.title("关键字列表展示")
    @allure.story("首页管理")
    def test_findkeyWorkList(self):
        url = host + port_help + "/help/findKeywordList.json"
        data = dict(status=1, page=1, size=10, name="", isShow="",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    def ids(self):
        url = host + port_help + "/help/findKeywordList.json"
        data = dict(status=1, page=1, size=10, name="", isShow="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result = requests.get(url, data, cookies=self.cook)
        resultdic = json.loads(result.text)["responseData"]["content"]
        ids = []
        for i in resultdic:
            ids.append(i["ID"])
        return ids

    @allure.title("添加关键字")
    @allure.story("首页管理")
    @pytest.mark.parametrize("name", ("咳嗽", "12345", "!@#"))
    def test_createKeyword(self, name):
        url = host + port_help + "/help/createKeyword.json"
        data = {
            "status": 1,
            "operatorId": self.authUserId,
            "operatorName": self.userName,
            "name": name,
            "isShow": 1,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, "咳嗽")

    @allure.title("关键字更改权限-可见度")
    @allure.story("首页管理")
    def test_updateKeyword(self):
        url = host + port_help + "/help/updateKeyword.json"
        ids = self.ids()
        data = {
            "id": ids[0],
            "operatorId": self.authUserId,
            "operatorName": self.userName,
            "isShow": 0,  # 这里是改的可见度 0 不可见 1 可见
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("关键字置顶")
    @allure.story("首页管理")
    def test_doTopKeyword(self):
        url = host + port_help + "/help/doTopKeyword.json"
        ids = self.ids()
        data = {
            "id": ids[-1],
            "operatorId": self.authUserId,
            "operatorName": self.userName,
            "isTop": 1,  # 这个字段是置顶 1表示置顶 0表示取消置顶
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook, str(ids[-1]))

    @allure.title("关键字删除")
    @allure.story("首页管理")
    def test_deleteKeyword(self):
        url = host + port_help + "/help/deleteKeyword.json"
        ids = self.ids()
        for i in range(len(ids) - 2):
            data = {
                "id": ids[i],
                "operatorId": self.authUserId,
                "operatorName": self.userName,
                "authUserId": self.authUserId,
                "authToken": self.authToken
            }
            assert_post(url, data, self.cook)

    @allure.title("菜单问题汇总")
    @allure.story("菜单管理")
    @pytest.mark.parametrize("category,hint", ((1, "科研项目管理"), (2, "数据挖掘分析")))
    def test_findMenuList(self, category, hint):
        url = host + port_help + "/help/findMenuList.json"
        data = dict(category=category,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint)

    @allure.title("新增用户手册-添加关联模块")
    @allure.story("用户手册管理")
    def test_findArticleListByModule(self):
        url = host + port_help + "/help/findArticleListByModule.json"
        data = dict(moduleData="home_id",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook, hint="home_id")

    @allure.title("新增用户手册-添加手册汇总")
    @allure.story("用户手册管理")
    def test_createMenu(self):
        url = host + port_help + "/help/createMenu.json"
        data = dict(status=1, menuName="新增用户手册1.0", isTop=0, category=1,
                    parentId="", operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        result, resultdic = assert_post(url, data, self.cook, hint=self.userName)
        global manualId
        manualId = resultdic["responseData"]["id"]

    @allure.title("手册汇总列表-修改汇总")
    @allure.story("用户手册")
    def test_updateMenu(self):
        url = host + port_help + "/help/updateMenu.json"
        data = dict(menuName="新增用户手册1.0.0", isTop=0, id=manualId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint="问题汇总2.0.1")

    @allure.title("手册汇总列表-汇总置顶")
    @allure.story("用户手册")
    @pytest.mark.parametrize("isTop", (1, 0))
    def test_doTopMenu(self, isTop):
        url = host + port_help + "/help/doTopMenu.json"
        data = dict(id=manualId, isTop=isTop, operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint=self.userName)

    @allure.title("手册汇总列表-汇总删除")
    @allure.story("用户手册")
    def test_deleteMenu2(self):
        url = host + port_help + "/help/deleteMenu.json"
        data = dict(id=manualId, operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint=self.userName)

    @allure.title("新增用户手册-添加文件")
    @allure.story("用户手册管理")
    def test_fileSave(self):
        url = host + port_project + "/project/file/save.json"
        file = {"file": open(uploadpath1, "rb")}
        data = {
            "displayName": "生成图片.png",
            "status": 1
        }
        assert_post(url, data, files=file, cook=self.cook, hint="生成图片.png")

    @allure.title("新增用户手册-发布")
    @allure.story("用户手册管理")
    def test_createArticle(self):
        url = host + port_help + "/help/createArticle.json"
        ids = self.articleId()
        allure.attach(f"传递参数ids={ids}")
        data = {
            "title": "新增操作",
            "moduleName": "首页-首页",
            "moduleData": "home_id",
            "content": "<p>用于实验</p>",
            "category": 1,
            "operatorId": self.authUserId,
            "operatorName": self.userName,
            "menuId": 20,
            "otherIds": 177,  # 上传文件的fileId
            "articleIds": ids[0],  # 关联手册的ID
            "status": 1,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    def articleId(self):
        url = host + port_help + "/help/findArticleList.json"
        data = dict(category="1,2", operatorId=self.authUserId, menuId=20,
                    operatorName=self.userName, page=1, size=10,
                    status=1, title="", orderby="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result, resultdic = assert_get(url, data, self.cook)
        ids = []
        for i in resultdic["responseData"]["content"]:
            ids.append(i["ID"])
        return ids

    @allure.title("用户手册详情查看")
    @allure.story("用户手册")
    def test_findArticle(self):
        url = host + port_help + "/help/findArticle.json"
        ids = self.articleId()
        allure.attach(f"传递参数ids={ids}")
        data = dict(id=ids[0], operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("用户手册详情查看")
    @allure.story("用户手册")
    @pytest.mark.parametrize("datatype", (1, 2))
    def test_findArticleExtList(self, datatype):
        url = host + port_help + "/help/findArticleExtList.json"
        ids = self.articleId()
        allure.attach(f"传递参数ids={ids}")
        data = dict(
            dataType=datatype, articleId=ids[0],
            authUserId=self.authUserId, authToken=self.authToken
        )
        assert_get(url, data, self.cook)

    @allure.title("对应的用户手册列表")
    @allure.story("用户手册管理")
    @pytest.mark.parametrize("status", ("", 1, 2))
    def test_findArticleList(self, status):
        url = host + port_help + "/help/findArticleList.json"
        data = {
            "category": 1,
            "operatorId": self.authUserId,
            "menuId": 20,
            "operatorName": self.userName,
            "page": 1,
            "size": 10,
            "status": status,  # 表示状态， 空的为全部， 1表示已发布，2表示已保存
            "title": "",
            "orderby": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("用户手册信息修改")
    @allure.story("用户手册")
    def test_updateArticle(self):
        url = host + port_help + "/help/updateArticle.json"
        ids = self.articleId()
        allure.attach(f"传递参数ids={ids}")
        data = dict(title="新增操作2.0", moduleName="首页-首页", moduleData="home_id",
                    content="<p>细致内</p>", operatorId=self.authUserId, operatorName=self.userName,
                    otherIds=192, articleIds="", status=1, id=ids[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, "新增操作2.0")

    @allure.title("用户手册信息置顶")
    @allure.story("用户手册")
    @pytest.mark.parametrize("isTop", (0, 1))
    def test_doTopArticle(self, isTop):
        url = host + port_help + "/help/doTopArticle.json"
        ids = self.articleId()
        allure.attach(f"传递参数ids={ids}")
        data = {
            "id": ids[0],
            "isTop": isTop,
            "operatorId": self.authUserId,
            "operatorName": self.userName,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问题汇总列表-新增汇总")
    @allure.story("问题管理")
    def test_createMenu2(self):
        url = host + port_help + "/help/createMenu.json"
        data = dict(status=1, menuName="问题汇总2.0", isTop=0, category=2,
                    parentId="", operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url=url, data=data, cook=self.cook, hint=self.userName)
        global troubleId
        troubleId = result[1]["responseData"]["id"]

    @allure.title("问题汇总列表-修改汇总")
    @allure.story("问题管理")
    def test_updateMenu2(self):
        url = host + port_help + "/help/updateMenu.json"
        data = dict(menuName="问题汇总2.0.1", isTop=0, id=troubleId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint="问题汇总2.0.1")

    @allure.title("问题汇总列表-汇总置顶")
    @allure.story("问题管理")
    @pytest.mark.parametrize("isTop", (1, 0))
    def test_doTopMenu2(self, isTop):
        url = host + port_help + "/help/doTopMenu.json"
        data = dict(id=troubleId, isTop=isTop, operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint=self.userName)

    @allure.title("问题管理-发布")
    @allure.story("问题管理")
    def test_createArticle2(self):
        url = host + port_help + "/help/createArticle.json"
        data = dict(title="新增问题管理1.0", moduleName="首页-首页", moduleData="home_id",
                    content="<p>新增内容11111111</p>", category=2, operatorId=self.authUserId,
                    operatorName=self.userName, menuId=21, otherIds="", articleIds="", status=1,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint=self.userName)

    def articleId2(self):
        url = host + port_help + "/help/findArticleList.json"
        data = dict(category="1,2", operatorId=self.authUserId, menuId=21,
                    operatorName=self.userName, page=1, size=10,
                    status=1, title="", orderby="",
                    authUserId=self.authUserId, authToken=self.authToken)
        result, resultdic = assert_get(url, data, self.cook)
        ids = []
        for i in resultdic["responseData"]["content"]:
            ids.append(i["ID"])
        return ids

    @allure.title("问题管理详情查看")
    @allure.story("问题管理")
    def test_findArticle2(self):
        url = host + port_help + "/help/findArticle.json"
        ids = self.articleId2()
        allure.attach(f"传递参数ids={ids}")
        data = dict(id=ids[0], operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("问题管理详情查看")
    @allure.story("问题管理")
    @pytest.mark.parametrize("datatype", (1, 2))
    def test_findArticleExtList2(self, datatype):
        url = host + port_help + "/help/findArticleExtList.json"
        ids = self.articleId2()
        allure.attach(f"传递参数ids={ids}")
        data = dict(
            dataType=datatype, articleId=ids[0],
            authUserId=self.authUserId, authToken=self.authToken
        )
        assert_get(url, data, self.cook)

    @allure.title("对应的问题管理列表")
    @allure.story("问题管理")
    @pytest.mark.parametrize("status", ("", 1, 2))
    def test_findArticleList2(self, status):
        url = host + port_help + "/help/findArticleList.json"
        data = {
            "category": 1,
            "operatorId": self.authUserId,
            "menuId": 21,
            "operatorName": self.userName,
            "page": 1,
            "size": 10,
            "status": status,  # 表示状态， 空的为全部， 1表示已发布，2表示已保存
            "title": "",
            "orderby": "",
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_get(url, data, self.cook)

    @allure.title("问题管理信息修改")
    @allure.story("问题管理")
    def test_updateArticle2(self):
        url = host + port_help + "/help/updateArticle.json"
        ids = self.articleId2()
        allure.attach(f"传递参数ids={ids}")
        data = dict(title="新增操作2.0", moduleName="首页-首页", moduleData="home_id",
                    content="<p>细致内</p>", operatorId=self.authUserId, operatorName=self.userName,
                    otherIds=192, articleIds="", status=1, id=ids[0],
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, "新增操作2.0")

    @allure.title("问题管理信息置顶")
    @allure.story("问题管理")
    @pytest.mark.parametrize("isTop", (0, 1))
    def test_doTopArticle2(self, isTop):
        url = host + port_help + "/help/doTopArticle.json"
        ids = self.articleId2()
        allure.attach(f"传递参数ids={ids}")
        data = {
            "id": ids[0],
            "isTop": isTop,
            "operatorId": self.authUserId,
            "operatorName": self.userName,
            "authUserId": self.authUserId,
            "authToken": self.authToken
        }
        assert_post(url, data, self.cook)

    @allure.title("问题汇总列表-汇总删除")
    @allure.story("问题管理")
    def test_deleteMenu2(self):
        url = host + port_help + "/help/deleteMenu.json"
        data = dict(id=troubleId, operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint=self.userName)

    @allure.title("更新数据展示")
    @allure.story("版本更新管理")
    def test_findArticleList1(self):
        url = host + port_help + "/help/findArticleList.json"
        data = dict(page=1, size=5, title="", operatorId=self.authUserId, operatorName=self.userName,
                    menuId="", orderby="pubdate", category=4, status=1, sort="desc",
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_get(url, data, self.cook)

    @allure.title("新增版本数据")
    @allure.story("版本更新管理")
    def test_createArticle4(self):
        url = host + port_help + "/help/createArticle.json"
        data = dict(title="验证可行性版本", content="<p><br></p><p>这里填写数据</p><p><br></p>",
                    category=4, status=1, operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        result = assert_post(url, data, self.cook, hint=self.userName)
        global editionId
        editionId = result[1]["responseData"]["id"]

    @allure.title("新增版本数据")
    @allure.story("版本更新管理")
    def test_updateArticle3(self):
        url = host + port_help + "/help/updateArticle.json"
        data = dict(title="验证可行性版本", content="<p><br></p><p>这里填写数据</p><p><br></p>",
                    category=4, status=1, operatorId=self.authUserId, operatorName=self.userName, id=editionId,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook, hint=self.userName)

    @allure.title("删除版本数据")
    @allure.story("版本更新管理")
    def test_deleteArticle3(self):
        url = host + port_help + "/help/deleteArticle.json"
        data = dict(id=editionId, operatorId=self.authUserId, operatorName=self.userName,
                    authUserId=self.authUserId, authToken=self.authToken)
        assert_post(url, data, self.cook)


if __name__ == '__main__':
    pytest.main()
