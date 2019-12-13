#!/usr/bin/env python
# encoding=utf-8 
"""
@file: conftest.py
@time: 2019/11/11 11:50
@Author:Terence
"""
from public.overWrite_Assert import *
# -----------------添加临床访视计划-----------------
@pytest.fixture()
def addVisitProject(dlogin, login,questionId):
    response1, cook = login
    url = host + portlogin + "/projectDetail/saveProjectInfo.json"
    header = {"cookie": dlogin}
    data = {
        "groupFlag": 3,  # 分组标识？？？
        "businessType": 1,  # 业务类型
        "projectName": f"审核新增临床访视计划 + {num}",  # 项目名称
        "projectId": "",
        "defaultFunction": "MANAGE_PATIENT,CREATE_CRF,CHECK_CRF,MANAGE_PRACTITIONER",
        "followupPlan": '[{"visitOrder":{"start":1,"end":1},"stepCount":1,"stepUnit":{"value":"d","code":"d",'
                            '"display":"天"},"preThreshold":1,"postThreshold":1,"thresholdType":"d",'
                            '"questionnaireId":"%s"}]'%questionId[0],
        "operatorFunction": "54906-submitProjectInfo",  # 操作方法
        "note": "",  # 笔记
        "status": 1,  # 状态
        "operatorId": response1["authUserId"],
        "authUserId": response1["authUserId"],
        "authToken": response1["authToken"]
    }
    assert_post(url, data, headers=header)

# -----------------临床访视计划审核-----------------
def list(response1, cook):
    url = host + portlogin + "/project/check/list.json"
    data = dict(dataType=20, page=1, size=15,
                authUserId=response1["authUserId"], authToken=response1["authToken"])
    result = requests.get(url, data, cookies=cook)
    datadic = {"dataId": [], "checkId": []}
    if "content" in result.text:
        resultdic = json.loads(result.text)["responseData"]["page"]["content"]
        for i in resultdic:
            datadic["dataId"].append(i["DATA_ID"])
            datadic["checkId"].append(i["ID"])
    return datadic


@pytest.fixture()
def submitVisits(login, dlogin):
    response1, cook = login
    dicdata = list(response1, cook)
    dataId = dicdata["dataId"][0]
    checkId = dicdata["checkId"][0]
    url = host + portlogin + "/project/check/submit.json"
    header = {"cookie": dlogin}
    data = dict(dataId=dataId, checkId=checkId, result=1, dataType=20,
                checkOption="", serviceName="projectCheckFollowupService",
                operatorFunction="54946-submitPlan",
                operatorId=response1["authUserId"], authUserId=response1["authUserId"], authToken=response1["authToken"])
    assert_post(url, data, headers=header)

