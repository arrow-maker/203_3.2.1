#!/usr/bin/env python
# --coding:utf-8--
"""
@file: readConfig.py
@time: 2019/9/4  10:54
@Author:Terence
"""
import os, configparser, pytest, requests, \
    json, time, sqlite3, re, allure, random, yaml, datetime
from public.Regular_frist import *


def get_sysPath():
    '''这里还可以使用
    os.getcwd()  但是会随着运行的文件的位置而变动
    os.path.dirname() 这个是使用父类的文件位置
    '''
    path12 = os.path.split(os.path.realpath(__file__))[0]
    return path12


syspath = get_sysPath()
config_path = os.path.join(syspath, 'pytest.ini')

# 读取文件
config = configparser.ConfigParser()
config.read(config_path)

"""
下面使用的相当于在public中的变量使用get_组名(变量名)再读取一遍
强制性关系：减少了定义的变量名（以防重复）没有直接使用public简单好用
"""


# -----------------读取ini配置文件信息-----------------
def get_url(name):
    value = config.get('change_value', name)
    return value


def get_port(name):
    value = get_url("port") + get_url("api") + name
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

# ----------变量---------
host = get_url("host")
durl = get_url("durl")
loginurl = get_url("loginurl")
logindata = json.loads(get_url("logindata"))
logindata2 = json.loads(get_url("logindata2"))
# ---------路径--------
portlogin = get_url("portlogin")
port = get_url("port")
port_model = host + config.get("port", "model")
port_qt = get_port("qt")
port_project = get_port("project")
port_resource = get_port("resource")
port_dataindex = get_port("dataindex")
port_sourcedata = get_port("sourcedata")
port_es = get_port("es")
port_primaryIndex = get_port("primary-index")
port_bbs = get_port("bbs")
port_python = config.get("change_value", "port") + config.get("change_value", "api") + config.get("port", "python")
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
# --*-配置yaml的路径-*--
yamlPath = os.path.join(syspath, "file", "config.yaml")
#  --*-读取yaml的内容-*--
congyaml = readyamlload(yamlPath)
# ----------邮箱配置-----
sender = get_email("sender")
passwd = get_email("passwd")
toget = get_email("toget")
# --------当天的日期------
timelocal = time.strftime("%Y-%m-%d", time.localtime())
# -------13位的-时间戳-毫秒级的时间戳--------
time_up = int(str(time.time())[:10] + str(time.time())[11:14])
# ----------随机数------
num = random.randint(1, 999)


# 对json数据的分行加工
def print_json_multi_row(resultDic):
    print(json.dumps(resultDic, sort_keys=True, indent=1, ensure_ascii=False))
# ----*--写入yaml数据--*----
def writhyaml():
    dd = [["05001,05005", "肺功能检查率"], ("02001,02002", "COPD抗菌药物使用率"), ("01006,01003", "CD率"), ("01004,01005", "48小时再入院率"), ("01001,01002", "COPD急性加重期住院死亡率")]
    try:
        with open(yamlPath, "a+", encoding="utf-8") as file:
            yaml.dump(data=dd, stream=file, allow_unicode=True)
    except Exception as e:
        print(f"写入yaml文件失败{e}")
    else:
        print(f"写入yaml文件成功")

if __name__ == '__main__':  # 测试一下，我们读取配置文件的方法是否可用
    # print('HTTP中的baseurl值为：', get_url("loginurl"))
    # print('EMAIL中的开关on_off值为：', get_port('python'))
    # print(time_up)
    # writhyaml()
    print(congyaml["质控首页_患者基本指标"],"\n",f'type={type(congyaml["质控首页_患者基本指标"][0])}')
    # data1234 = [("05001,05005", "肺功能检查率"), ("02001,02002", "COPD抗菌药物使用率"), ("01006,01003", "CD率"),
    #             ("01004,01005", "48小时再入院率"), ("01001,01002", "COPD急性加重期住院死亡率")]
    # data12345 = data1234 + [pytest.param('01006,01003', "肺功能检查率", marks=pytest.mark.xfail)]
    # print(f"\ndata1234={data1234}\ndata12345={data12345}")

