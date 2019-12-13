#!/usr/bin/env python
# --coding:utf-8--
"""
@file: configEmail.py
@time: 2019/9/18  11:33
@Author:Terence
"""


import smtplib, os
from email.mime.application import MIMEApplication  # 邮件附件
from email.mime.multipart import MIMEMultipart  # 邮件附件
from email.mime.text import MIMEText  # 邮件正文
from email.header import Header
import zipfile

# 下面的是发送压缩文件
from datetime import date
# 文件路径
path1 = os.path.dirname(__file__)
filepath = os.path.dirname(path1)

def getToday():
    '''获得今天的日期，并把名字改成0901这样的格式'''
    today = date.today()
    date_today = today.strftime("%m%d")
    return date_today

def get_zip_file(input_path, result):
    """    对目录进行深度优先遍历    :param input_path:    :param result:    :return:    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)

def zip_file_path(input_path, output_path, output_name=f"{getToday()}html.zip"):
    """    压缩文件
      :param input_path: 压缩的文件夹路径
      :param output_path: 解压（输出）的路径
      :param output_name: 压缩包名称
      :return:
    """
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    get_zip_file(input_path, filelists)
    for file in filelists:
        f.write(file)
        # 调用了close方法才会保证完成压缩
    f.close()
    return output_path + r"/" + output_name

# zip_file_path(r"..\report\html",r"E:\161_API\report","html.zip")
"""
这里是发送附件的邮件
"""


def send_zip(sender, receivers, mail_pass):
    outpath = os.path.join(filepath,"report")
    inpath = os.path.join(outpath, "html")
    zip_file_path(inpath, outpath)
    # sender = '2317782219@qq.com'
    # receivers = ['2317782219@qq.com', "zhanglf@tp-data.com"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    # mail_user = "ternence66@foxmail.com"  # 用户名
    # mail_pass = "zynuezzfolixdhia"  # 口令

    # 构建邮件附件
    zipFile = os.path.join(outpath,f"{getToday()}html.zip")
    zipApart = MIMEApplication(open(zipFile, 'rb').read())
    zipApart.add_header('Content-Disposition', 'attachment', filename=zipFile)

    logFile = os.path.join(outpath,"api.log")

    logApart = MIMEApplication(open(logFile, 'rb').read())
    logApart.add_header('Content-Disposition', 'attachment', filename=logFile)
    #  配置附件信息
    message = MIMEMultipart()
    message.attach(zipApart)
    message.attach(logApart)
    # 邮件正文
    message.attach(MIMEText('Python 邮件发送测试结果', 'plain', 'utf-8'))
    # 邮件信息
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')
    message["From"] = sender
    message["To"] = receivers
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(sender, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# if __name__ == '__main__':
#     send_zip("2317782219@qq.com","2317782219@qq.com","zynuezzfolixdhia")