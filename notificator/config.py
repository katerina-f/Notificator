import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SQLALCHEMY_BASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        'test', '1234', '0.0.0.0', 'postgres')

    LOGFILE = 'log.log'
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    INTERVAL = (0,1)
    NOTIFICATION_TIME = os.environ.get('NOTIFICATION_TIME')

    RECIPIENTS = ['ekaterina.frolova40@gmail.com',
                  'katerinafr0lova@yandex.ru']
