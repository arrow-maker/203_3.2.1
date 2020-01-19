#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file: test_pulmonaryFunction.py
@time: 2019/9/30 16:14
@Author:Terence
"""
from public.overWrite_Assert import *
from public.Link_database import conOracle
import importlib
importlib.reload(sys)
os.environ['NLS_LANG'] = 'Simplified Chinese_CHINA.ZHS16GBK'

@allure.feature("肺功能大屏")
class Test_pulmonartFunction:

    # @pytest.mark.parametrize("login")
    # def __init__(self, login):
    #     response1, cook = login

    # 这里的数据是默认的所有的数据-但是界面上显示的是按日期显示的
    @allure.story("链接数据库")
    def database(self, groupNo):
        # 这里是查找那个大屏的选择
        result1 = conOracle(OracleDataurl, r"select * from report_group where GROUP_NAME like '%大屏%'")

        # 这里是选择当前的大屏
        pub = []
        for i in result1:
            pub.append((i[1], i[4]))  # 保存大屏和大屏的Id
        # print(pub)
        pppp = [('支气管扩张大屏', 'zkdp'), ('肺功能大屏', 'fdp01'), ('肺功能大屏', 'fdp02'), ('肺部真菌感染大屏', 'fzjdp'), ('脑卒中大屏', 'nzzdp'),
                ('哮喘大屏', 'XCDP'), ('间质肺大屏', 'ipf01'), ('慢阻肺大屏', 'AECOPD-01'), ('慢阻肺大屏', 'AECOPD-031'),
                ('ACO大屏', 'acodp'), ('慢阻肺大屏', 'AECOPD-01'), ('慢阻肺大屏', 'AECOPD-031')]
        # 肺功能大屏的数据
        b = []
        result2 = conOracle(OracleDataurl, u"SELECT * FROM report_lib WHERE GROUP_NO = 'fdp01'")
        for i in result2:
            b.append(i[10])
        c = tuple(b)  # 这个大屏的所有的疾病Id
        ccccc = (15046, 15047, 15048, 15010, 15011, 15012, 15050, 15015, 15016, 15018, 'fzjdp01', 15049, 15013)
        cccccc = ('I6154', 'I6172', 'I6174', 'I6149', 'I7030', 'I6153', 'I6175', 'I6155', 'I6162', 'I6173', 'I6160',
                  'I6163', 'I6167', 'I6170', 'I6165', 'I6150', 'I6156', 'I6151', 'I6206', 'I6161', 'I6176')
        # 有疾病的id 找到data_Id找到对应的数据参数
        q3 = conOracle(OracleDataurl, u"SELECT * FROM anal_report_source_data WHERE data_id IN {0}".format(c))
        # print(f"\n+++{q3}")
        # 读取某个指标的具体数据
        dd = []  # 用来保存这个疾病和疾病的数据
        for i in q3:
            # print(i)
            # 下面是消除 换行
            ww = re.split("\n", i[2].read())
            a = ""
            for k in ww:
                if "-" not in k:
                    # print(k)
                    a = a + k + " "
            # 删除多余的空格
            bb = a.replace("       ", " ")
            # print(f"-*-{bb}")
            # 删除；
            cc = bb.replace(";", "")
            if ") t" in cc:
                # 这里删除多余的t
                dd12 = cc.replace(") t", ")")
            elif "/*" in cc:
                # print(cc)
                if "30天再入院率" not in cc:
                    ass = cc.split("/")
                    # 下面是删除 注释的一种方法
                    # 之后对 ass字符串进行判断ass[0] == * 删除，之后再拼接起来
                    resultStr1 = ""
                    if ass[0] != "*" and ass[-1] != "*":
                        for j in ass:
                            resultStr1 += j
                    # print(ass)
                    dd12 = resultStr1
                else:
                    dd12 = cc
            else:
                dd12 = cc
            try:
                q5 = conOracle(OracleDataurl, dd12)
                # print(f"---{q5}")
                dd.append((i[1], q5[-1]))
            except Exception as e:
                pass
                # print(e)
        # print(dd)
        return dd

    @allure.story("数据来源 的url")
    @allure.link(url=f"{host}/code/codeItem/findCodeItem.json", name="link_url")
    @allure.severity(A2)
    @pytest.mark.parametrize("itemCode", (
            "ES_DOMAIN", "COLLECT_DOMAIN", "KINSHIP_DOMAIN", "DS_DOMAIN", "SOURCEDATA_DOMAIN",
            "PYTHON_STATISTIC_DOMAIN", "QT_DOMAIN", "PRIMARY_INDEX_DOMAIN", "BBS_DOMAIN",
            "DATAINDEX_DOMAIN", "PROJECT_DOMAIN", "AI_TOOL_DOMAIN", "RESOURCE_DOMAIN"))
    def test_findCodeItem(self, itemCode, login):
        response1, cook = login
        url = host + portlogin + "/code/codeItem/findCodeItem.json"
        data = dict(code="SYS_DOMAIN",
                    itemCode=itemCode)
        assert_get(url, params=data, cook=cook)


    @allure.story("最近的医院")
    @allure.link(url=f"{host}/platform/hospital/getCurrentHospital.json", name="link_url")
    @allure.severity(A3)
    def test_getCurrentHospital(self, login):
        response1, cook = login
        url = host + portlogin + "/platform/hospital/getCurrentHospital.json"
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        result, resultdic = assert_get(url, data, cook)
        assert response1["hospital"] in result

    @allure.story("显示数据分组")
    @allure.link(url=f"{host}/quality/control/getReportGroupList.json", name="link_url")
    @allure.severity(A3)
    @pytest.mark.parametrize("groupNo", ('zkdp', 'fdp01', 'fdp02', 'nzzdp', 'XCDP',
                                         'ipf01', 'AECOPD-01', 'AECOPD-031', 'acodp', 'AECOPD-01', 'AECOPD-031'))
    def test_getReportGroupList(self, login, groupNo):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo=groupNo,  # fdp01
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    def trandfer_groupon(self, groupNo, response1, cook):
        url = host + port_sourcedata + "/quality/control/getReportGroupList.json"
        data = dict(groupNo=groupNo,
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        ids = []
        for i in resultdic:
            ids.append(i["reportNo"])
        return tuple(ids)

    @allure.story("地图上所有的医院")
    @allure.link(url=f"{host}/analItem/getAnalItemConfigList.json", name="link_url")
    @allure.severity(A3)
    @allure.step("传入的参数：login={0}")
    def test_getAnalItemConfigList(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/analItem/getAnalItemConfigList.json"
        data = dict(authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)

    @allure.story("所有展示数据的数据来源")
    @allure.link(url=f"{host}/quality/control/getReportDatas.json", name="link_url")
    @allure.severity(A3)
    @pytest.mark.parametrize("groupNo", ('zkdp', 'fdp01', 'fdp02', 'nzzdp',
                                         'ipf01', 'AECOPD-01', 'acodp', 'AECOPD-01'))
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getReportDatas(self, login, groupNo, start, end):
        response1, cook = login
        orgdata = self.database(groupNo)
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        reportNo = self.trandfer_groupon(groupNo, response1, cook)
        allure.attach(f"内部参数：orgdata={orgdata}\n reportNo={reportNo}")
        data = dict(
            hospitalCode=response1["hospitalCode"],
            reportNos=reportNo,
            indexTimeStart=start,
            indexTimeEnd=end,
            authUserId=response1["authUserId"], authToken=response1["authToken"])
        result = requests.get(url, data, cookies=cook)
        resultdic = json.loads(result.text)["responseData"]
        # 傻傻的做, 没有意义
        if len(resultdic) > 0:
            for i in resultdic:  # 接口返回的数据
                for k in orgdata:  # 数据库返回的数据
                    if k[0] in i:
                        for j in i["data"]["rows"]:  # 每个指标的详细的数据
                            if k[1][0] == j["group"]:
                                if len(k[1]) > 1:
                                    assert str(k[1][1]) == j["count"]
                                    if len(k[1]) > 2:
                                        assert str(k[1][2]) == j["value"]
        print_json_multi_row(json.loads(result.text))

    @allure.story("门诊住院总人数")
    @allure.step("传入的参数：login={0}")
    @allure.link(url=f"{host}/quality/control/getReportDatas.json", name="link_url")
    @allure.severity(A3)
    @pytest.mark.parametrize("groupNo", ('zkdp', 'fdp01', 'fdp02', 'nzzdp',
                                         'ipf01', 'AECOPD-01', 'acodp', 'AECOPD-01'))
    @pytest.mark.parametrize("start,end", searchdate)
    def test_getReportData(self, login, groupNo, start, end):
        response1, cook = login
        url = host + port_sourcedata + "/quality/control/getReportDatas.json"
        reportNo = self.trandfer_groupon(groupNo, response1, cook)
        allure.attach(f"内部参数：repotNO={reportNo}")
        for i in range(len(reportNo) // 2):
            data = dict(
                reportNos=f'{reportNo[2 * i]},{reportNo[2 * i + 1]}', hospitalCode=response1["hospitalCode"],
                indexTimeStart=start, indexTimeEnd=end,
                authUserId=response1["authUserId"], authToken=response1["authToken"]
            )
            assert_get(url, data, cook)

    @allure.story("全国省份数据")
    @allure.link(url=f"{host}/map/geo-json/100000.json", name="link_url")
    @allure.severity(A3)
    @allure.step("传入的参数：login={0}")
    def test_geoJson10000(self, login):
        url = host + port_sourcedata + "/map/geo-json/100000.json"
        assert_get(url, {}, login[1], "true")

    @allure.story("广州省份的数据")
    @allure.link(url=f"{host}/map/geo-json/province/440000.json", name="link_url")
    @allure.severity(A3)
    @allure.step("传入的参数：login={0}")
    def test_geoJson440000(self, login):
        url = host + port_sourcedata + "/map/geo-json/province/440000.json"
        assert_get(url, {}, login[1], "广州市")

    @allure.story("广东市的数据")
    @allure.link(url=f"{host}/map/geo-json/440000/440100.json", name="link_url")
    @allure.severity(A3)
    @allure.step("传入的参数：login={0}")
    def test_geoJson440100(self, login):
        url = host + port_sourcedata + "/map/geo-json/440000/440100.json"
        assert_get(url, {}, login[1], "UTF8Encoding")

    @allure.story("顶部显示的区域范围")
    @allure.link(url=f"{host}/analItem/getAnalItemConfigList.json", name="link_url")
    @allure.severity(A3)
    @allure.step("传入的参数：login={0}")
    def test_getAnalItemConfigList1(self, login):
        response1, cook = login
        url = host + port_sourcedata + "/analItem/getAnalItemConfigList.json"
        data = dict(hospitalCode=response1["hospitalCode"],
                    authUserId=response1["authUserId"], authToken=response1["authToken"])
        assert_get(url, data, cook)


if __name__ == '__main__':
    pytest.main()
