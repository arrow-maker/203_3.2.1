#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@file:
@time: 2019/10/10 10:15
@Author:Terence
"""
from readConfig import *
from public.Link_database import conOracle

@pytest.fixture(scope="session")
def linkBigScreen():
    # 找到所有的大屏数据
    pub =[]
    result1 = conOracle(OracleDataurl, "SELECT * FROM report_group WHERE GROUP_NAME LIKE '%大屏%'")
    # 找到特定的大屏和对应的group_on
    for i in result1:
        pub.append((i[1], i[4]))
    print(pub)
    # 找到 对应大屏的数据
    result2 = conOracle(OracleDataurl, "SELECT * FROM report_lib WHERE GROUP_NO = 'ipf01'")
