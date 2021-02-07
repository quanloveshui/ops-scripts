#!/usr/bin/python3.6
#coding=utf-8

import xlsxwriter
import datetime
import subprocess
from subprocess import Popen, PIPE
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.application import MIMEApplication
import string
import os,stat


#生成巡检excel类
class CreateExcel():
    def __init__(self):
        self.today = datetime.datetime.now().strftime("%m%d")
        self.today2 = datetime.datetime.now().strftime("%Y%m%d")
        self.excel_name = '%s-%s.xlsx' % ('LSDN维护作业计划', self.today2)
        self.sheet_name = '日表'
        self.dirs = r"/home/yqh/%s" % (datetime.datetime.now().strftime('%Y%m%d'))
        self.path = '/维护作业计划/xxxxx/2021/维护日报'
        self.system_content = '%s/%s/%s' % (self.path, self.today, self.today2 + '.txt')
        self.backup_content = 'xxx服务器上：/BackupGitlab/'
        self.gslbnum_content = 'xxx服务器上:/BackupGitlab/'
        self.gslbtime_content = '%s/%s/%s' % (self.path, self.today, '带宽流量汇总-%s.png' % self.today2)
        self.security_content = '%s/%s/%s' % (self.path, self.today, self.today2 + '.txt')
        self.row_order = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
        self.row_content = ('序号', '测试类别', '维护项目', '周期', '执行结果', '输出物', '负责人', '备注')
        self.items = ['网络连通性检查', '磁盘空间检查', '服务器CPU、内存使用情况检查', '应用软件进程状态检查',
                 '业务数据及系统配置文件备份', 'gitlab数据备份', '流量汇总检查', '系统日志安全检查']

    #写数据到excel
    def wite_to_excel(self):
        if os.path.exists(self.dirs):
            pass
        else:
            os.makedirs(self.dirs)
            os.chmod(self.dirs,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
        # 创建excel文件
        workbook = xlsxwriter.Workbook( '%s/%s' %(self.dirs,self.excel_name))
        # 添加新的sheet表
        worksheet = workbook.add_worksheet(self.sheet_name)
        # 添加样式
        cell_format = workbook.add_format({'align': 'center',
                                           'valign': 'vcenter',
                                           'border': 1,
                                           'font_size': 10,
                                           # 'bold': 'true',
                                           'text_wrap': 1  # 自动换行

                                           })
        # 行高
        worksheet.set_row(8, 30)
        worksheet.set_row(9, 30)
        worksheet.set_row(10, 30)
        worksheet.set_row(11, 30)
        # 列宽
        worksheet.set_column('A:D', 10, cell_format)
        worksheet.set_column('C:C', 50, cell_format)
        worksheet.set_column('E:E', 10, cell_format)
        worksheet.set_column('F:F', 50, cell_format)
        worksheet.set_column('G:H', 10, cell_format)
        # 合并单元格写内容
        worksheet.merge_range('A1:H1', 'xxxx组件维护作业执行表（日表）')
        worksheet.merge_range('A2:H2', '涉及网元：xxxx')
        worksheet.merge_range('B5:B11', '系统基本运行情况检查')
        worksheet.merge_range('F5:F8', '')
        worksheet.merge_range('G5:G12', 'xxxx')
        worksheet.merge_range('H5:H12', '自动+人工')
        for i in range(0, len(self.row_order)):
            locate = '%s3:%s4' % (self.row_order[i], self.row_order[i])
            worksheet.merge_range(locate, self.row_content[i])
        # 单个单元格写内容
        worksheet.write('B12', '安全-日')
        for index, item in enumerate(self.items, 5):
            worksheet.write('A%d' % index, index - 4)
            worksheet.write('C%d' % index, item)
            worksheet.write('D%d' % index, '日')
            worksheet.write('E%d' % index, '正常')
        # 写入输出物内容
        worksheet.write('F5', self.system_content)
        worksheet.write('F9', self.backup_content)
        worksheet.write('F10', self.gslbnum_content)
        worksheet.write('F11', self.gslbtime_content)
        worksheet.write('F12', self.security_content)
        workbook.close()
        return self.excel_name

#定义发送邮件类
class SendEmail():
    def __init__(self,txt):
        self.dirs = datetime.datetime.now().strftime('%Y%m%d')
        self.mail_host = 'smtp.qq.com'
        self.mail_user = 'xxxx'
        self.mail_passwd = 'xxxx'
        self.sender = 'xxxx'
        #self.receivers = ['xxxxx']
        self.receivers = ['yxxxxx']
        self.subject = 'xxxx巡检报告'
        self.text = txt
    #发送邮件
    def send(self,info):
        message = MIMEMultipart()#创建一个带附件的事例
        message.attach(MIMEText(self.text, 'plain', 'utf-8'))  # 添加正文内容
        message['From'] = self.sender
        message['To'] = ",".join(self.receivers)
        message['Subject'] = Header(self.subject, 'utf-8')
        # 添加附件
        filepath=filepath='/home/yqh/%s/' % self.dirs
        #print(filepath)
        # 通过循环统计附件个数，便于添加添加附件
        att = []
        for i in range(len(info)):
            att.append(i)
        #循环添加附件
        for i in att:
            keyname = list(info[i].keys())[0]
            filename = info[i][keyname]
            att[i] = MIMEText(open(os.path.join(filepath,filename), 'rb').read(), 'base64', 'utf-8')
            att[i]["Content-Type"] = 'application/octet-stream'
            # 附件名称非中文时的写法
            #att2["Content-Disposition"] = 'attachment; filename=%s' % 'OTT-GSLB-0429.xlsx'
            #附件名称为中文时的写法
            att[i].add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
            message.attach(att[i])

        try:
            smtp = SMTP_SSL(self.mail_host, 465)
            # smtp.set_debuglevel(1)
            smtp.ehlo(self.mail_host)
            smtp.login(self.mail_user, self.mail_passwd)
            smtp.sendmail(self.sender, self.receivers, message.as_string())
            print("邮件发送成功")
        except Exception as e:
            print(e)



if __name__ == "__main__":
    dirpath = datetime.datetime.now().strftime('%Y%m%d')
    #需要发送的附件名
    info_dic = [{'traffic':'带宽流量汇总-%s.png' % dirpath},{'txt':'%s.txt' % dirpath},{'excel_name':'xxx维护作业计划-%s.xlsx' % dirpath},
               ]
    #存放正文内容
    filepath='/home/yqh/%s/' % dirpath

    msg=""""""
    f = open('%s/%s.txt' % (filepath,dirpath),'r+')
    for i in range(5):
        msg+=f.readline()
    msg+='今日巡检结果详见附件,请检查'
    f.close()

    obj_excel = CreateExcel()
    obj_email =SendEmail(msg)
    name=obj_excel.wite_to_excel()
    obj_email.send(info_dic)
