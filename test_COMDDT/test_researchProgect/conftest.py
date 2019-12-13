#!/usr/bin/env python
# encoding=utf-8 
"""
@file: conftest.py
@time: 2019/11/15 18:13
@Author:Terence
"""
from public.overWrite_Assert import *


@allure.description("下面的是传递问卷的Id")
@pytest.fixture()
def questionId(login):
    response1, cook = login
    url = host + port_qt + "/qtInfo/findFhirQsList.json"
    data = dict(page=1, size=1000, authUserId=response1["authUserId"], authToken=response1["authToken"])
    print(f"\nurl = {url}\ndata = {data}")
    result = requests.get(url, data, cookies=cook)
    resultdic = json.loads(result.text)["responseData"]
    ids = []
    for i in resultdic:
        ids.append(f'Questionnaire/{i["resourceId"]}')
    return ids
