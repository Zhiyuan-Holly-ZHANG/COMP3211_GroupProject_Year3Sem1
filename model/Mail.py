import smtplib
from email.mime.text import MIMEText
from email.header import Header
#sender = 'oliverlorentino@gmail.com'
    #    receivers = ['21099573d@connect.polyu.hk']

class Mail:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def send(self, msg):


        # 邮件内容
        global smtpObj
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header("admin", 'utf-8')
        message['To'] = Header("user", 'utf-8')

        # 邮件主题
        subject = 'Events notify' \
                  '' \
                  '' \
                  '' \
                  ''
        message['Subject'] = Header(subject, 'utf-8')

        try:
            # 使用SMTP服务器发送邮件
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP服务器地址和端口
            smtpObj.starttls()  # 如果服务器需要安全连接，则启用TLS
            smtpObj.login(self.sender, 'jcfl djiv mgjn ytju')  # 登录验证
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())  # 发送邮件
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: ；mail send fail", e)
        finally:
            smtpObj.quit()

