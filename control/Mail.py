import smtplib
from email.mime.text import MIMEText
from email.header import Header


# sender = 'oliverlorentino@gmail.com'
# receivers = ['21099573d@connect.polyu.hk']

class Mail:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def send(self, msg):

        # contents of the mail
        global smtpObj
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header("admin", 'utf-8')
        message['To'] = Header("user", 'utf-8')

        # subject
        subject = 'Events notify' \
                  '' \
                  '' \
                  '' \
                  ''
        message['Subject'] = Header(subject, 'utf-8')

        try:
            # SMTP
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP service
            smtpObj.starttls()  # safe connects TLS
            smtpObj.login(self.sender, 'jcfl djiv mgjn ytju')  #
            smtpObj.sendmail(self.sender, self.receiver, message.as_string())  # send mail
        except smtplib.SMTPException as e:
            print("Error: ；mail send fail", e)
        finally:
            smtpObj.quit()
