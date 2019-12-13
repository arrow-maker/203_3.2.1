#!/usr/bin/env python
# --coding:utf-8--
"""
pytest使用的环境与python运行的环境
@file: auditProject.py
@time: 2019年08月15日   14:27:09
@Author:Terence
"""

from public.overWrite_Assert import *


# ------项目审核--------------
@allure.description("我的项目-项目审核-信息列表")
def auditProjectList(cook, authUserId, authToken):
    url = host + port_project + "/project/check/list.json"
    data = dict(checkType="1",  # 待审核的
                projectCenter="", projectName="",
                page=1, size=10, operatorId=authUserId,
                authUserId=authUserId, authToken=authToken)
    result = requests.get(url, data, cookies=cook)
    auditData = {"DATA_ID": [], "ID": [], "ORG_ID": [], "name": []}
    aa = json.loads(result.text)["responseData"]["content"]
    if len(aa) > 0:
        for i in aa:
            auditData["ORG_ID"].append(i["ORG_ID"])
            auditData["DATA_ID"].append(i["DATA_ID"])
            auditData["ID"].append(i["ID"])
            auditData["name"].append(i["CREATE_USER_NAME"])
    return auditData


@allure.description("我的项目-项目审核-审核对应的项目")
def auditCheckSave(name12, cook, authUserId, authToken):
    url = host + port_project + "/project/check/save.json"
    dataid1 = auditProjectList(cook, authUserId, authToken)
    data = {
        "operatorId": authUserId,  # 操作人员
        "dataId": dataid1["DATA_ID"][0],  # 我的项目列表中的PROJECT_ID  审核列表中的DATA_ID   #3573263
        "result": 1,  # 检查类型
        "checkOption": "",  # 审核意见
        "serviceName": "projectCheckFollowupService",  # 服务名称 固定的
        "checkId": dataid1["ID"][0],  # 检查ID  6683
        "dataType": 10,  # 待审核的
        "operatorFunction": "54826-submitProject",  # 操作方法 固定的格式
        "authUserId ": authUserId,
        "authToken": authToken
    }
    result = requests.post(url, data, cookies=cook)
    print(f"\nurl={url} \ndata={data}")
    print(result.text)
    time.sleep(20)
    if dataid1["DATA_ID"][0] not in result.text:
        assert "已审核" in result.text


# ------------项目申请--------------------
@allure.description("科研质控-申请项目-基础信息的保存")
def projectBase(response1, cook):
    url = host + port_project + "/project/save.json"
    data = {
        "projectName": f"位同步{num}",
        "disciplineTypeId": 1,
        "projectTypeId": 2,
        "projectNameEn": "",
        "solutionCode": "",
        "planStartDateStr": "2018-11-04",
        "planEndDateStr": "2019-12-26",
        "projectContact": response1["userName"],
        "projectContactId": response1["authUserId"],
        "projectContactUnitId": response1["orgId"],
        "projectContactMobile": response1["mobile"],
        "projectContactUnit": response1["hospital"],
        "projectOrganizer": "",
        "researchDesign": "",
        "projectObjective": "蔚然图",
        "projectObjectiveSecond": "",
        "projectObjectiveOther": "",
        "projectCenter": 1,
        "projectUserInType": "",
        "synergyType": 1,
        "projectUserInMult": 1,
        "isStartUpPeriod": 1,
        "followupLostHandling": "",
        "followupLostNumber": "",
        "projectUserElutionTime": "",
        "deadlineType": 1,
        "needAgreement": 1,
        "operatorId": response1["authUserId"],
        "projectId": "",
        "orgId": response1["orgId"],
        "newDrugClinicalStudyNo": "",
        "clinicalStudyTypeCode": "",
        "studyDrugNameZn": "",
        "studyDrugNameEn": "",
        "studyDrugTypeCode": "",
        "studyDrugTypeValue": "",
        "studyDrugRegisterTypeCode": "",
        "studyDrugDosageFormCode": "",
        "clinicalIndications": "",
        "randomGroupType": 0,
        "grouptimeFlag": 1,
        "randomPart": "",
        "randomLength": "",
        "centerCode": 4545,
        "organizerPhone": "",
        "entryRequire": "",
        "diseaseIds": "",
        "authUserId": response1["authUserId"],
        "authToken": response1["authToken"]
    }
    result = requests.post(url, data, cookies=cook)
    resultdic = json.loads(result.text)["responseData"]
    projectId = resultdic["projectId"]
    return projectId


@allure.description("科研质控-申请项目-受试者分组保存")
def projectInfosave(response1, cook, questionId):
    url = host + port_project + "/project/info/start-up-period/save.json"
    projectId = projectBase(response1, cook)
    data = dict(projectId=projectId, operatorId=response1["authUserId"], unInGroupDeadline=44444, deadlineType=1,
                followupPlan='[{"visitOrder":{"start":1,"end":2},"stepCount":3,"stepUnit":{"value":"d","code":"d",'
                             '"display":"天"},"preThreshold":1,"postThreshold":4,"thresholdType":"d",'
                             '"questionnaireId":"%s"}]'%questionId[0],
                startUpPeriodRule=1, startUpPeriodDesc=4444444, startUpPeriodPart=0, startUpPeriodLength="",
                startUpPeriodPrefix="",
                authUserId=response1["authUserId"], authToken=response1["authToken"])
    assert_post(url, data, cook)
    return projectId


@allure.description("科研质控-申请项目-分中心信息保存")
def projectGroup(response1, cook, questionId):
    url = host + port_project + "/project/info/project-group/save.json"
    projectId = projectInfosave(response1, cook, questionId)
    data = dict(projectId=projectId, operatorId=response1["authUserId"], projectName="试验组1",
                projectDesc='{"inCriteria":"","outCriteria":""}', centerCode="",
                projectCount=44444, allowScaleOver=44,
                followupPlan='[{"visitOrder":{"start":1,"end":1},"stepCount":1,"stepUnit":{"value":"d","code":"d",'
                             '"display":"天"},"preThreshold":1,"postThreshold":1,"thresholdType":"d",'
                             '"questionnaireId":"%s"}]'%questionId[0],
                authUserId=response1["authUserId"], authToken=response1["authToken"])
    assert_post(url, data, cook)
    return projectId


@allure.description("科研质控-申请项目-提交申请项目")
def submitProject(login, questionId):
    response1, cook = login
    url = host + port_project + "/project/submit.json"
    projectId = projectGroup(response1, cook, questionId)
    data = dict(projectId=projectId, operatorId=response1["authUserId"], operatorFunction="54806-submitProject",
                authUserId=response1["authUserId"], authToken=response1["authToken"])
    assert_post(url, data, cook)
