#!/usr/bin/env python

"""
@file: conftest.py
@time: 2019/9/2  17:37
@Author:Terence
"""
'''
这里时配置文件：
    每一个test_文件执行前都要走过的文件(相当于一个public只是不用自己导入了)
    方法：可以配置登录等公共的方法（个人的理解这里是添加public的方法）
    变量：变量的配置好像在ini文件中（注意这里的ini文件需要解读（readConfig（解读配置文件））
    
'''
import os, sys

path111 = os.path.dirname(__file__)
sys.path.append(path111)

from public.overWrite_Assert import *
from selenium import webdriver
import win32crypt


# --------------------登录------------------
@pytest.fixture(scope="session")
def login():
    result = requests.post(url=loginurl, data=logindata)
    resultData = json.loads(result.text)

    authUserId = resultData["responseData"]["roleList"][0]["orgUserId"]
    authToken = resultData["responseData"]["roleList"][0]["orgUserIdToken"]
    hospitalCode = resultData["responseData"]["platformList"][0]["code"]  # 用户所在的医院的code
    userName = resultData["responseData"]["userName"]  # 用户的姓名
    mobile = resultData["responseData"]["mobileTelephone"]
    orgId = resultData["responseData"]["roleList"][0]["orgId"]
    itemOrgId = resultData["responseData"]["itemOrgId"]
    hospital = resultData["responseData"]["platformList"][0]["platformName"]  # 获取医院的名字
    orgName = resultData["responseData"]["roleList"][0]["orgName"]  # 用户所属的科室
    timelocal = time.strftime("%Y-%m-%d", time.localtime())
    idToken = resultData["responseData"]["roleList"][0]["idToken"]
    ids = resultData["responseData"]["roleList"][0]["id"]
    userId = resultData["responseData"]["userId"]  # 获取用户的Id
    roleName = resultData["responseData"]["roleList"][0]["roleName"]  # 获取角色信息
    datadic = {"authUserId": authUserId, "authToken": authToken, "hospitalCode": hospitalCode, "orgId": orgId,
               "itemOrgId": itemOrgId, "hospital": hospital, "orgName": orgName, "timelocal": timelocal,
               "idToken": idToken, "ids": ids, "userId": userId, "roleName": roleName, "userName": userName,
               "mobile": mobile}

    yield datadic, result.cookies

@pytest.fixture(scope="session")
def login2():
    result = requests.post(url=loginurl, data=logindata2)
    resultData = json.loads(result.text)
    authUserId = resultData["responseData"]["roleList"][0]["orgUserId"]
    authToken = resultData["responseData"]["roleList"][0]["orgUserIdToken"]
    datadic = {"authUserId": authUserId, "authToken": authToken}

    yield datadic, result.cookies

@pytest.fixture()
def orgPath(login):
    response1, cook = login
    if response1["itemOrgId"] == response1["orgId"]:
        return f'400,{response1["itemOrgId"]}'
    else:
        return f'400,{response1["itemOrgId"]},{response1["orgId"]},'


# -------------------获取cookie值--------------------

# 读取chrome 登录的cookie值
def transferCookie(host):
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"  # 找到Chrome cookie路径
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host  # 找到特定的cookie
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {name: win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value
                   in
                   cu.execute(sql).fetchall()}
        # print(f"\n+++{cookies}")
        return cookies


def driverlogin(host):
    driver = webdriver.Chrome()
    driver.get(host)
    time.sleep(1)
    driver.find_element_by_xpath("//*[@class='ivu-select-selection']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//li[text()='广州医科大学附属第一医院']").click()
    driver.find_element_by_xpath("//*[@placeholder='请输入用户名']").send_keys("arrow")
    driver.find_element_by_xpath("//*[@placeholder='请输入密码']").send_keys("tP123456@")
    driver.find_element_by_xpath("//*[@type='button']").click()
    time.sleep(1)
    cookie = driver.get_cookies()
    time.sleep(1)
    cookiedata = f"{cookie[0]['name']}={cookie[0]['value']}; {cookie[1]['name']}={cookie[1]['value']}"
    driver.quit()
    return cookiedata


# 浏览器登录，确保cookie值的可用
@pytest.fixture(scope="session")
def dlogin():
    hostl = get_url("durl")
    host = re.findall("http://(.+?):30", hostl)[0]
    cookie = transferCookie(host)  # 获取最近登录的cookie
    if len(cookie.keys()) > 0:  # 如果最近有登录 直接获取
        yield f"JSESSIONID={cookie['JSESSIONID']}"
    else:  # 获取登录的cookies       # 如果最近没有登录 就去selenium登录并获取cookie值
        cookiestr = driverlogin(hostl)
        yield cookiestr


# -------------------通过筛选得到的患者列表的信息----------------------
@allure.description("通过指标（没有指标所有的患者）添加患者")
def savedataTempLate(response1, cook):
    url = host + port_dataindex + "/dataIndex/dataTemplate/saveDataTemplate.json"
    data = dict(status=2, version=3, dataIds="2887,248,249",
                patientQueryWhere='{"logicSymbol":"and","whereList":[{"logicSymbol":"or","whereType":1,"whereList":'
                                  '[{"logicSymbol":"or","whereList":[{"symbol":"=","dataValueType":"1","dataId":"462",'
                                  '"dataRId":"484","columnValue":"2018-11-06,2019-11-06","columnName":"VISIT_DATE",'
                                  '"columnTitle":"入院时间","columnType":"date","dataName":"入院时间"}]}]}]}',
                dataScope=1, dataQueryWhere="", type=0, operatorId=response1["authUserId"],
                templateName="初始版本1573019180603",
                # businessVariables='{"dataId":"7206","dataType":"1","hospitalCode":"12440100455344205E","orgId":75635}',
                timeScope=2, indexRule=1,
                authUserId=response1["authUserId"], authToken=response1["authToken"])
    result = requests.post(url, data, cookies=cook)
    resultdic = json.loads(result.text)
    templateId = resultdic["responseData"]["templateId"]
    return templateId


@allure.description("分析临时的指标得到的数据")
def getDataAnalysisCount(response1, cook):
    templateId = savedataTempLate(response1, cook)
    url = host + port_dataindex + "/dataIndex/dataStore/getDataAnalyzeCount.json"
    data = dict(templateId=templateId, authUserId=response1["authUserId"], authToken=response1["authToken"])
    assert_post(url, data, cook)
    return templateId


@allure.description("得到临时的指标筛选的患者的列表信息")
@pytest.fixture(scope="session")
def resultList(login):
    response1, cook = login
    temp = getDataAnalysisCount(response1, cook)
    url = host + port_dataindex + "/dataIndex/dataTemplate/getDataAnalysisResultList.json"
    data = dict(templateId=temp, page=2, size=25, resultType=0,
                operatorId=response1["authUserId"],
                # projectId=7206,
                authUserId=response1["authUserId"], authToken=response1["authToken"])
    result = requests.get(url, data, cookies=cook)
    resultdic = json.loads(result.text)["responseData"][0]["dataPage"]["content"]
    ids = {"patientId": [], "orgUserId": [], "patiId": []}
    for i in resultdic:
        ids["patientId"].append(i["PATIENT_ID"])
        ids["orgUserId"].append(i["ORG_USER_ID"])
        ids["patiId"].append(i["PATI_ID"])
    return ids