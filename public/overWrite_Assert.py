from public.read_xlrd import *
from readConfig import *


def overWrite_assert_get_xls_hint(url, params, cook, catePath, Sheet):
    xlsParament = read_xls(catePath, Sheet)
    for i in range(0, xlsParament[3]):
        # print(type(xlsParament[0][i]),xlsParament[0][i])
        if type(xlsParament[0][i]) is dict:  # 判断data是字典
            xlsdata = xlsParament[0][i]
        else:
            xlsdata = json.loads(xlsParament[0][i])
        xlshint = xlsParament[2][i]
        actualResult = requests.get(url, dict(xlsdata, **params), cookies=cook)
        print("{0} {1}行的结果 {2}".format(Sheet, i + 2, actualResult.text))
        ecpectedResult = xlsParament[1][i]
        response_data = json.loads(actualResult.text)
        if type(response_data["responseData"]) is dict:
            if "totalElements" in response_data["responseData"].keys():
                totalElements = response_data["responseData"]["totalElements"]
                size = response_data["responseData"]["size"]
            elif "page" in response_data["responseData"].keys():
                if type(response_data["responseData"]["page"]) is dict:
                    if "totalElements" in response_data["responseData"]["page"].keys():
                        totalElements = response_data["responseData"]["page"]["totalElements"]
                        size = response_data["responseData"]["page"]["size"]
                else:
                    totalElements = 0
                    size = 0
            # 对是有页数的进行页数断言
            if ecpectedResult == "验证page":  # 判断断言的信息是不是页数
                if totalElements != 0:  # 用来判断是否有数据
                    if type(totalElements / size) is not int:
                        assert str(totalElements // size + 1) in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                    else:
                        assert str(totalElements // size) in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                    # 有数据的页数--页数断言失误
                else:
                    assert '成功' in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 没有数据对页数的断言
            elif ecpectedResult == "验证numberOfElements":
                # numberPage=responseData["responseData"]["numberOfElements"]
                if totalElements != 0:
                    assert str(totalElements % size) in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 断言最后一页个数失误
                else:
                    assert "成功" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
            else:  # 对非页数数据断言.
                if type(response_data["responseData"]) is dict:
                    if "content" in response_data["responseData"].keys():
                        if len(response_data["responseData"]["content"]) == 0:  # 对没有返回数据的用"SUCCESS"进行断言
                            assert "成功" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                        else:
                            assert ecpectedResult in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                    elif "page" in response_data["responseData"].keys():  # 这个时针对科研审核-受试者终止-数据的
                        if type(response_data["responseData"]["page"]) is dict:
                            if len(response_data["responseData"]["page"]["content"]) == 0:  # 对没有返回数据的用"SUCCESS"进行断言
                                assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 对没有数据断言的相应进行
                        else:  # 有数据的用数据内部的字段进行断言
                            assert ecpectedResult in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 对没有页数的数据断言
                else:
                    if "SUCCESS" not in actualResult.text:
                        assert ecpectedResult in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                    else:
                        assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"


def overWrite_assert_post_xls_hint(url, params, cook, catePath, Sheet):
    xlsParament = read_xls(catePath, Sheet)
    for i in range(0, xlsParament[3]):
        if type(xlsParament[0][i]) is dict:
            xlsdata = xlsParament[0][i]
        else:
            xlsdata = json.loads(xlsParament[0][i])
        xlshint = xlsParament[2][i]
        if type(cook) is dict:
            actualResult = requests.post(url, dict(xlsdata, **params), headers=cook)
        else:
            actualResult = requests.post(url, dict(xlsdata, **params), cookies=cook)
        print(f"{Sheet} 第{i + 2}行 {actualResult.text}")  # 运行的结果
        ecpectedResult = xlsParament[1][i]
        responseData = json.loads(actualResult.text)
        if type(responseData["responseData"]) is dict:
            if "totalElements" in responseData["responseData"].keys():
                totalElements = responseData["responseData"]["totalElements"]
                size = responseData["responseData"]["size"]
            elif "page" in responseData["responseData"].keys():  # 这里是临床访视审核中的列表数据要用到的
                if type(responseData["responseData"]["page"]) is dict:
                    if "totalElements" in responseData["responseData"]["page"].keys():
                        totalElements = responseData["responseData"]["page"]["totalElements"]
                        size = responseData["responseData"]["page"]["size"]
                else:
                    totalElements = 0
                    size = 0
            # 对是有页数的进行页数断言
            if ecpectedResult == "验证page":
                if totalElements != 0:
                    if type(totalElements / size) is not int:
                        assert str(totalElements // size + 1) in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                    else:
                        assert str(totalElements // size) in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                else:
                    assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
            elif ecpectedResult == "验证numberOfElements":
                if totalElements != 0:
                    assert str(totalElements % size) in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 断言最后一页个数失误
                else:
                    assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
            else:  # 对非页数数据断言.
                if type(responseData["responseData"]) is dict:
                    if "content" in responseData["responseData"].keys():
                        if len(responseData["responseData"]["content"]) == 0:
                            assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 对没有数据断言的相应进行
                        else:  # 有数据的用数据内部的字段进行断言
                            assert ecpectedResult in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 对没有页数的数据断言
                    elif "page" in responseData["responseData"].keys():  # 这个时针对科研审核-受试者终止-数据的
                        if type(responseData["responseData"]["page"]) is dict:
                            if len(responseData["responseData"]["page"]["content"]) == 0:
                                assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 对没有数据断言的相应进行
                        else:  # 有数据的用数据内部的字段进行断言
                            assert ecpectedResult in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"  # 对没有页数的数据断言
                else:
                    if "SUCCESS" not in actualResult.text:
                        assert ecpectedResult in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"
                    else:
                        assert "SUCCESS" in actualResult.text, f"{Sheet} 第{i + 2}行 {xlshint}"


def assert_page(page=5):
    if page == 5:
        pass


def assert_get(url, params=None, cook=None, hint="true", **kwargs):
    result = requests.get(url, params=params, cookies=cook, **kwargs)
    resultdic = json.loads(result.text)
    print_json_multi_row(resultdic)
    allure.attach(f"url={url}\nparams={params}\nhint={hint}\nkwargs={kwargs}\nresult={result.text}", name="断言参数数据")
    if hint not in result.text:
        assert "SUCCESS" in result.text
    return result.text, resultdic


def assert_post(url, data=None, cook=None, hint="true", **kwargs):
    result = requests.post(url, data=data, cookies=cook, **kwargs)
    resultdic = json.loads(result.text)
    print_json_multi_row(resultdic)
    allure.attach(f"url={url}\ndata={data}\nhint={hint}\nkwargs={kwargs}\nresult={result.text}", name="断言参数数据")
    if hint not in result.text:
        assert "SUCCESS" in result.text
    return result.text, resultdic

# aa = ['2015-01-16 16:35:43', '2015-04-27 11:26:56', '2015-07-27 13:50:45', '2015-08-31 15:08:16', '2015-12-19 12:18:00',
#       '2016-04-07 12:07:45', '2016-08-30 13:51:56', '2016-01-22 09:29:35', '2016-01-25 14:45:56', '2016-02-01 14:58:07',
#       '2016-02-15 15:29:27', '2016-02-29 15:18:11', '2016-03-07 15:07:05', '2016-05-06 09:44:24', '2017-09-19 14:37:06',
#       '2018-12-06 16:29:42', '2018-12-07 08:59:01', '2018-12-07 09:05:20']
# aa2 = [time.strptime(x, "%Y-%m-%d %H:%M:%S") for x in aa]   # 这个是时间数据
# print(aa2)
# # 字符时间转换为时间戳
# aa1 = [int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))) for x in aa]
# aa1 = []
# for i in aa:
#     print(i)
#     timeArray = time.strptime(i, "%Y-%m-%d %H:%M:%S")
#     aa1.append(int(time.mktime(timeArray)))
# # 时间戳转化为字符时间
# bb = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)) for x in sorted(aa1)]
# print(f"aa1={aa1} \naa2={sorted(aa1)}")
# print(f"bb={bb}")
# print(f"aa={aa}")
# # assert aa == bb1
# assert aa1 == sorted(aa1)
# cc = ['2016-01-22 09:29:35', '2016-01-25 14:45:56', '2016-02-01 14:58:07', '2016-02-15 15:29:27', '2016-02-29 15:18:11', '2016-03-07 15:07:05', '2016-04-07 12:07:45', '2016-05-06 09:44:24', '2016-08-30 13:51:56',]
# cc1 = [int(time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))) for x in cc]
# print(cc1)
# assert cc1 == sorted(cc1)
# print(aa1.sort())
# assert aa1 == sorted(aa1)
# dd = [1460002065, 1472536316, 1453426175, 1453704356, 1454309887, 1455521367, 1456730291, 1457334425, 1462499064]
# dd1= [1453426175, 1453704356, 1454309887, 1455521367, 1456730291, 1457334425, 1460002065, 1462499064, 1472536316]
# cc = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)) for x in dd]
# cc1= [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)) for x in dd1]
# print(f"cc={cc}\ncc1={cc1}")