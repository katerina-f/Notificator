import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from notificator.extensions import config

from loguru import logger

class Sender:
    """
    класс отвечающий за создание соединения с почтовым сервером
    и отправки ему сообщений
    """

    def __init__(self, message, header):
        self.login = config.MAIL_USERNAME
        self.password = config.MAIL_PASSWORD
        self.subject = 'Birthdays'
        self.recipients = config.RECIPIENTS
        self.message = str(message)
        self.header = header

    @logger.catch(level='ERROR')
    def send_message(self):
        message_obj = MIMEMultipart()
        message_obj['From'] = self.login
        message_obj['To'] = ', '.join(self.recipients)
        message_obj['Subject'] = self.subject
        message_obj.attach(MIMEText(self.message))
        print(message_obj)
        smtp_obj = smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT)
        # identify ourselves to smtp client
        smtp_obj.ehlo()
        print(self.recipients)
        # secure our email with tls encryption
        smtp_obj.starttls()
        # re-identify ourselves as an encrypted connection
        smtp_obj.ehlo()
        smtp_obj.login(self.login, self.password)
        smtp_obj.sendmail(self.login, self.recipients, message_obj.as_string())
        smtp_obj.quit()
