# -*- coding: utf-8 -*-

import cx_Oracle

def conOracle(conOracleStr, oracleSQL):
    connect = cx_Oracle.connect(conOracleStr)
    cur = connect.cursor()
    cur.execute(oracleSQL)  # "select table_name from user_tables" 用户的所有的表名
    dataAll11 = cur.fetchall()
    # cur.close()
    return dataAll11

# pub =[]
# q = conOracle(OracleDataurl,"select * from user_tab_columns where table_name='REPORT_GROUP'")
# for i in q:
#     print(i)
# print()
# q_1 = conOracle(OracleDataurl,"select * from user_tab_columns where table_name='REPORT_LIB'")
# for i in q_1:
#     print(i)
# q_2 = conOracle(OracleDataurl,"select * from user_tab_columns where table_name='ANAL_REPORT_SOURCE_DATA'")
# print()
# for i in q_2:
#     print(i)
# q1 = conOracle(OracleDataurl,"SELECT * FROM report_group WHERE GROUP_NAME LIKE '%大屏%'")
# for i in q1:
#     pub.append((i[1], i[4]))
# print(pub)
# pppp = [('支气管扩张大屏', 'zkdp'), ('肺功能大屏', 'fdp01'), ('肺功能大屏', 'fdp02'), ('肺部真菌感染大屏', 'fzjdp'), ('脑卒中大屏', 'nzzdp'), ('哮喘大屏', 'XCDP'), ('间质肺大屏', 'ipf01'), ('慢阻肺大屏', 'AECOPD-01'), ('慢阻肺大屏', 'AECOPD-031'), ('ACO大屏', 'acodp'), ('慢阻肺大屏', 'AECOPD-01'), ('慢阻肺大屏', 'AECOPD-031')]
# b = []

# 找到特定的大屏的数据
# q2 = conOracle(OracleDataurl,"SELECT * FROM report_lib WHERE GROUP_NO = 'ipf01'")
# for i in q2:
#     b.append(i[10])
# c = tuple(b)
# q3 = conOracle(OracleDataurl,"SELECT * FROM anal_report_source_data WHERE data_id IN {0}".format(c))
# print(q3)
# print(f"\n+{q}\n++{q_1}\n++++{q_2}")
# print(f"\n-{q2}\n--{q3}")

#     print(i[19].read())
# print(dd)
# a = "select (select count(distinct v.inpatient_no) from warehouse.DW_T_DIAGNOSIS2 v,warehouse.dw_t_order dv where v.data_type = 1 and v.index_rule in (0,1) and v.ILDS_INTERSTITIAL='有' and dv.hospital_code = v.hospital_code and dv.index_rule in (0,1) and dv.inpatient_no = v.inpatient_no and dv.drug_class41 = '有' ) as value,(select count(distinct v.inpatient_no) from warehouse.DW_T_DIAGNOSIS2 v where v.index_rule in (0,1) and v.data_type = 1 and  v.ILDS_INTERSTITIAL='有') as value2 from dual"
# result = conOracle(OracleDataurl, a)
# print(result)
# q4 = conOracle(OracleDataurl,"select key, value,value2 from(select L_INSPIRE as key, COUNT(report_id) as value, round(count(report_id)/(select count(report_id) from warehouse.DW_T_LUNG_SCREEN t where t.L_INSPIRE is not null [t.index_time >= to_date(:indexTimeStart,'yyyy-mm-dd')] [t.index_time <= to_date(:indexTimeEnd,'yyyy-mm-dd')] [t.hospital_code = :hospitalCode] ), 4)*100 value2 from warehouse.DW_T_LUNG_SCREEN v where L_INSPIRE is not null,[to_char(v.index_time,'yyyy-mm-dd') >= :indexTimeStart],[to_char(v.index_time,'yyyy-mm-dd') <= :indexTimeEnd],[v.hospital_code = :hospitalCode] group by L_INSPIRE ) where key is not null")
# print(q4)


# q2 = conOracle(OracleDataurl, "SELECT * FROM report_lib WHERE GROUP_NO = '脑卒中大屏' ")
# print()
# print(q[1])
# print(f"{q1},\n{type(q1)}")
#
# print(f"{q2},\n{type(q2)}")
# q2 = conOracle(OracleDataurlIndex,"select * from DATA_TEMPLATE t where t.template_id=21563 and rownum < 5")
# ww = q2

# q2 = conOracle(OracleDataurlIndex,"select * from DATA_TEMPLATE t where t.template_id=21563 and rownum < 5")
# ww = q2
# print(ww)
# from readConfig import *
# tempResult = conOracle(OracleDataurlIndex, "select * from data_template t where t.template_id=10320")
# print(f"tempresult = {tempResult}")