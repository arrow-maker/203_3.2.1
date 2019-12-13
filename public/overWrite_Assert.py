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


def assert_get(url, params=None, cook=None, hint="true", **kwargs):
    result = requests.get(url, params=params, cookies=cook, **kwargs)
    resultdic = json.loads(result.text)
    print_json_multi_row(resultdic)
    allure.attach(f"url={url}\nparams={params}\nhint={hint}\nkwargs={kwargs}\nresult={result.text}", name="参数数据")
    if hint not in result.text:
        assert "SUCCESS" in result.text
    return result.text, resultdic


def assert_post(url, data=None, cook=None, hint="true", **kwargs):
    result = requests.post(url, data=data, cookies=cook, **kwargs)
    resultdic = json.loads(result.text)
    print_json_multi_row(resultdic)
    allure.attach(f"url={url}\ndata={data}\nhint={hint}\nkwargs={kwargs}\nresult={result.text}", name="参数数据")
    if hint not in result.text:
        assert "SUCCESS" in result.text
    return result.text, resultdic

