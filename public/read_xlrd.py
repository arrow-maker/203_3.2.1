# -*- coding: utf-8 -*-
import xlrd, json, os
import pandas as pd
# from readConfig import researchCatePath

syspath1 = os.path.dirname(os.path.dirname(__file__))

def read_xls(catePath, Sheet):
    data = []  # 传入输入数据
    ass = []  # 传入断言数据
    hint = []  # 传入提示信息
    work = xlrd.open_workbook(catePath)
    sheet_name = work.sheet_by_name(Sheet)
    nrow1 = sheet_name.nrows
    for i in range(1, nrow1):
        ass.append(sheet_name.row_values(i)[2])
        hint.append(sheet_name.row_values(i)[3])
        if "@" in sheet_name.row_values(i)[1]:  # 下列是判断输入数据 中是是否由多重字典(用@分开)
            qq = sheet_name.row_values(i)[1].split("@")
            dataDic12 = json.loads(qq[0])
            for k in range(1, len(qq)):
                bb = qq[k].split("=")
                dataDic12[bb[0]] = bb[1]
            data.append(dataDic12)
        else:
            data.append(sheet_name.row_values(i)[1])
    return data, ass, hint, nrow1 - 1


def read_excel(catePath, Sheet):
    work = xlrd.open_workbook(catePath)
    sheet_name = work.sheet_by_name(Sheet)
    nrow1 = sheet_name.nrows
    data = []
    for i in range(1, nrow1):
        # ass.append(sheet_name.row_values(i)[2])
        # hint.append(sheet_name.row_values(i)[3])
        value = sheet_name.row_values(i)
        if "@" in value[1]:  # 下列是判断输入数据 中是是否由多重字典(用@分开)
            qq = value[1].split("@")
            paramdic = json.loads(qq[0])
            for k in range(1, len(qq)):
                bb = qq[k].split("=")
                paramdic[bb[0]] = bb[1]
            data.append((paramdic, value[2], value[3]))
        else:
            data.append((json.loads(value[1]), value[2], value[3]))
    return data
# result = read_excel(researchCatePath, "我的项目-项目数据")
# print(result)
def get_excel(excelname, sheetname12):
    filepath = os.path.join(syspath1, "file", excelname)
    work = xlrd.open_workbook(filepath)
    data = work.sheet_by_name(sheetname12)
    nrows = data.nrows
    result = []
    for i in range(1, nrows):
        result.append(data.row_values(i))
    return result

def pandas_excel(excelname, sheetname12):
    filepath = os.path.join(syspath1, "file", excelname)
    result = pd.read_excel(filepath, sheet_name=sheetname12)
    result = pd.DataFrame(result)
    return result

# ff = pandas_excel("临床指标筛选所有指标.xls", "专病指标")
# print(list(ff[423:424]["hint"]))
# print(list(ff[423:424]["hint"])[0])
# print(type(list(ff[423:424]["hint"])[0]))