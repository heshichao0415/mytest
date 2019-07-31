import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from write_readini import read_ini
import configpath
import os

# path = configpath.getpath()
# mail_body_path = os.path.join(path, 'result', 'report.html')
# f = open(mail_body_path, 'rb')
# mail_body = f.read()

class Mail(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.send_name_from = read_ini('EMAIL', 'cc_name')
        self.send_pwd_from = read_ini('EMAIL', 'cc_pwd')
        self.send_pd_from = read_ini('EMAIL', 'cc_pd')
        self.send_subject = read_ini('EMAIL', 'subject')
        self.send_name_to = read_ini('EMAIL', 'address')
        self.email_host = read_ini('EMAIL', 'mail_host')
        self.email_text = read_ini('EMAIL', 'TEXT')
        self.mail_body = open(os.path.join(configpath.getpath(), 'result', 'report.html'), 'rb').read()

    def send_email(self):
        """发送邮件,携带附件且将内容写入邮件正文"""
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['FROM'] = self.send_name_from
        msg['TO'] = self.send_name_to
        msg['subject'] = self.send_subject

        """邮件正文内容"""
        msg.attach(MIMEText(self.email_text, 'plain', 'utf-8'))

        """构造附件"""
        att = MIMEText(self.mail_body, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename=result; encoding=utf-8'
        msg.attach(att)

        try:
            #smtp = smtplib.SMTP()
            smtp = smtplib.SMTP_SSL(self.email_host, 465)  #链接至邮件服务器
            #smtp.connect(self.email_host, 25)
            smtp.login(self.send_name_from, self.send_pd_from)  #登录邮件服务器
            smtp.sendmail(self.send_name_from, self.send_name_to, msg.as_string()) #发送邮件
            smtp.quit()
            print('给%s发送邮件成功' % self.send_name_to)

        except Exception as f:
            print('给%s发送邮件失败，失败原因%s' % self.send_name_to, f)

if __name__ == '__main__':
    mail = Mail()
    mail.send_email()











