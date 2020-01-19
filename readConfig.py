#!/usr/bin/env python
# --coding:utf-8--
"""
@file: readConfig.py
@time: 2019/9/4  10:54
@Author:Terence
"""
import os, configparser, pytest, requests, \
    json, time, sqlite3, re, allure, random, yaml, datetime, sys
from public.Regular_frist import *


def get_sysPath():
    path12 = os.path.split(os.path.realpath(__file__))[0]
    return path12


syspath = get_sysPath()
config_path = os.path.join(syspath, 'pytest.ini')

# 读取文件
config = configparser.ConfigParser()
config.read(config_path)


# -----------------读取ini配置文件信息-----------------
def get_url(name):
    value = config.get('change_value', name)
    return value


def get_port(name):
    value = systemUserAndEnvireonmentCongYaml["登录"]["配置端口"] + systemUserAndEnvireonmentCongYaml["登录"]["项目文件"] + name
    return value


def get_database(name):
    value = config.get('database', name)
    return value


def get_casePath(name):
    value = config.get('testCasePath', name)
    return value


def get_email(name):
    value = config.get('email', name)
    return value


#   --*-读取yaml的内容-*--
def readyamlload(yamlName):
    yamlfile1 = open(yamlName, "r", encoding="utf-8")
    fileY1 = yamlfile1.read()
    conyaml1 = yaml.full_load(fileY1)
    return conyaml1


# --*-配置yaml的路径-*--
yamlPath = os.path.join(syspath, "file", "config.yaml")
systemYamlPath = os.path.join(syspath, "file", "用户和环境.yaml")
#  --*-读取yaml的内容-*--
congyaml = readyamlload(yamlPath)
systemUserAndEnvireonmentCongYaml = readyamlload(systemYamlPath)

"""
                                配置登录的信息
"""
# ----------变量---------
"http://192.168.0.203/"
if systemUserAndEnvireonmentCongYaml["登录"]["外网的IP"] is not None:
    host_1 = systemUserAndEnvireonmentCongYaml["登录"]["外网的IP"]
else:
    host_1 = systemUserAndEnvireonmentCongYaml["登录"]["内网的IP"]
host = f"http://{host_1}"
"""
            用户
"""
useName = systemUserAndEnvireonmentCongYaml["登录"]["用户名"]  # 登录用户名
useName2 = systemUserAndEnvireonmentCongYaml["登录"]["配置用户"]  # 登录配置用户名
Encrypt = systemUserAndEnvireonmentCongYaml["登录"]["医院"]  # 登录医院的编号
password = systemUserAndEnvireonmentCongYaml["登录"]["密码"]
isSend = systemUserAndEnvireonmentCongYaml["登录"]["是否发送邮件"]  # 判断是否发送邮件 1 发送，非1的发送
portlogin = systemUserAndEnvireonmentCongYaml["登录"]["登录端口"]
port = systemUserAndEnvireonmentCongYaml["登录"]["配置端口"]
durl = f"http://{host_1}{portlogin}/v3/#/login"
loginurl = f"http://{host_1}{portlogin}/ext/shop/login.json"
HospitaiName = systemUserAndEnvireonmentCongYaml["登录"]["医院"]


# --*- 获取医院的信息 -*--
def Hospital(hospitalName):
    url = f"http://{host_1}{portlogin}/platform/hospital/findAllHospital.json"
    result = requests.get(url)
    dictresult = json.loads(result.text)["responseData"]
    for i in dictresult:
        if hospitalName in i["name"]:
            return i["orgId"]
        else:
            print("不存在这个医院")


logindata = {"loginName": useName,"password": "e9c37fc431a1a423754260ae02a31e83","withEncrypt": 1,"itemOrgId": Hospital(HospitaiName)}
logindata2 = {"loginName": useName2,"password": "e9c37fc431a1a423754260ae02a31e83","withEncrypt": 1,"itemOrgId": Hospital(HospitaiName)}
# ---------路径--------
port_model = host + config.get("port", "model")
port_qt = get_port("qt")
port_project = get_port("project")
port_resource = get_port("resource")
port_dataindex = get_port("dataindex")
port_sourcedata = get_port("sourcedata")
port_es = get_port("es")
port_primaryIndex = get_port("primary-index")
port_bbs = get_port("bbs")
port_python = get_port("python")
port_help = get_port("help")
port_mobile = get_port("mobile")
port_patient = get_port("patient")
# ------数据库-----
OracleDataurl = get_database("OracleDataurl")
OracleDataurlIndex = get_database("OracleDataurlIndex")
# ---------路径------
runIndexPath = os.path.join(syspath, "file", get_casePath("runIndexPath"))
researchCatePath = os.path.join(syspath, "file", get_casePath("researchCatePath"))
clincalPath = os.path.join(syspath, "file", get_casePath("clincalPath"))
systemPath = os.path.join(syspath, "file", get_casePath("systemPath"))
wardDoctorBenchPath = os.path.join(syspath, "file", get_casePath("wardDoctorBenchPath"))
recrutmentPath = os.path.join(syspath, "file", get_casePath("recrutmentPath"))
# --*-上传文件的位置----
uploadpath1 = os.path.join(syspath, "file", "生成图片.png")
uploadpath2 = os.path.join(syspath, "file", "运行图.png")
uploadpath3 = os.path.join(syspath, "file", "成功运行图.png")
# ----------邮箱配置-----
sender = systemUserAndEnvireonmentCongYaml["登录"]["发送者"]
passwd = systemUserAndEnvireonmentCongYaml["登录"]["邮箱密码"]
toget = systemUserAndEnvireonmentCongYaml["登录"]["接收者"]
# --------当天的日期------
timelocal = time.strftime("%Y-%m-%d", time.localtime())
timelocal_1 = f"{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday - 1}"
# -------13位的-时间戳-毫秒级的时间戳--------
time_up = int(str(time.time())[:10] + str(time.time())[11:14])
# ----------随机数------
num = random.randint(1, 999)
# -------日期--所有日期，五年，三年，一年，半年，季节，一个月--------
searchdate = (("2019-01-01", "2020-12-31"), ("2000-01-01", "2020-12-31"),
              ("2017-01-01", "2020-12-31"), ("2018-01-01", "2020-12-31"),
              ("2019-06-01", "2020-01-31"), ("2019-10-01", "2020-01-31"),
              ("2020-01-01", "2020-01-31"), ("", ""))


# 对json数据的分行加工
def print_json_multi_row(resultDic):
    print(json.dumps(resultDic, sort_keys=True, indent=1, ensure_ascii=False))


# 用例的优先级
A1 = "blocker"  # 中断缺陷(客户端不能执行下一步)
A2 = "critical"  # 临界缺陷(功能点缺陷)
A3 = "normal"  # 普通缺陷(数值计算错误)
A4 = "minor"  # 次要缺陷(界面错误)
A5 = "trivial"  # 轻微缺陷(提示不规范)


# ----*--写入yaml数据--*----
def writhyaml():
    dd = [["05001,05005", "肺功能检查率"], ("02001,02002", "COPD抗菌药物使用率"), ("01006,01003", "CD率"),
          ("01004,01005", "48小时再入院率"), ("01001,01002", "COPD急性加重期住院死亡率")]
    try:
        with open(yamlPath, "a+", encoding="utf-8") as file:
            yaml.dump(data=dd, stream=file, allow_unicode=True)
    except Exception as e:
        print(f"写入yaml文件失败{e}")
    else:
        print(f"写入yaml文件成功")


if __name__ == '__main__':  # 测试一下，我们读取配置文件的方法是否可用
    print(f"今天的时间={host}")
    print(f"data={logindata}\nmodel={port_mobile}")
    print(Hospital("演示医院1"))
    "广州医科大学附属第一医院"
    print(Hospital("广州医科大学"))
    # sys.stdout.encoding
    """
        这里的是打印当前的model的编码类型
        aa = sys.stdout.encoding
        print(aa)
    """
    # print(f"useName={useName}\ntype={type(useName)}\nuseName2={useName2}")
    # print(f"isSend={isSend}\ntype={type(isSend)}")
    # print(f"type={type(logindata)}logindata={logindata}\nlogindata2={logindata2}")
    # print('HTTP中的baseurl值为：', get_url("loginurl"))
    # print('EMAIL中的开关on_off值为：', get_port('python'))
    # print(time_up)
    # writhyaml()
    # print(congyaml["质控首页_患者基本指标"], "\n", f'type={type(congyaml["质控首页_患者基本指标"][0])}')
