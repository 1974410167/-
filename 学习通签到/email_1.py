
from email.mime.text import MIMEText
import smtplib
import datetime
from email.header import Header

class send_email():

    def __init__(self,to_address,name):
        self.to_address = to_address
        self.name = name
        self.form_addr = "1974410167@qq.com"
        self.password = "ejdfbhvgwurbdicg"
        self.smtp_server = 'smtp.qq.com'

    def message(self):

        msg = MIMEText(f'{self.name}  已为你签到  {datetime.datetime.now()}','plain','utf-8')
        msg['To'] = Header(self.to_address,'utf-8')
        msg["Subject"] = Header('签到提醒','utf-8')
        return msg

    def send(self):

        with smtplib.SMTP_SSL(self.smtp_server,465) as server:
            server.login(self.form_addr,self.password)
            msg = self.message()
            server.sendmail(self.form_addr,[self.to_address],msg.as_string())

