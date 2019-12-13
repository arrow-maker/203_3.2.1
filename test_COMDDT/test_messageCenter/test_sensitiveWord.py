#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file: test_sensitiveWord.py
@time: 2019/9/30 11:19
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.feature("敏感词")
class Test_medicalPersonnelmessage:

    @allure.story("敏感词展示")
    @allure.step("参数：login={0}")
    def test_findList(self, login):
        response1, cook = login
        url = host + portlogin + "/sensitiveWord/findList.json"
        data = dict(
            word="", operatorFunction='51181-viewWordList',
            operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def transfer_findList(self, response1, cook):
        url = host + portlogin + "/sensitiveWord/findList.json"
        data = dict(
            word="", operatorFunction='51181-viewWordList',
            operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        ids = []
        resultdic = json.loads(result.text)["responseData"]
        if len(resultdic) > 0:
            for i in resultdic:
                ids.append((i['id'], i['word']))
        return ids

    @allure.story("添加敏感词")
    @allure.step("参数： login={0}")
    def test_saveSensitiveWord(self, login):
        response1, cook = login
        url = host + portlogin + "/sensitiveWord/saveSensitiveWord.json"
        data = dict(
            word='新增22', operatorFunction='51181-addWord',
            operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.story("修改敏感词汇")
    @allure.step("参数： login={0}")
    def test_saveSensitiveWord1(self, login):
        response1, cook = login
        url = host + portlogin + "/sensitiveWord/saveSensitiveWord.json"
        dicdata = self.transfer_findList(response1, cook)
        allure.attach(f"内部参数： dicdata={dicdata}")
        data = dict(
            word='新增22', id=dicdata[0][0], operatorFunction='51181-editWord',
            operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)

    @allure.story("删除敏感词")
    @allure.step("参数：login={0}")
    def test_deleteSensitiveWord(self, login):
        response1, cook = login
        url = host + portlogin + "/sensitiveWord/deleteSensitiveWord.json"
        dicdata = self.transfer_findList(response1, cook)
        allure.attach(f"内部参数：dicdata={dicdata}")
        data = dict(
            id=dicdata[0][0], operatorFunction='51181-delWord',
            operatorId=response1["authUserId"],
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_post(url, data, cook)