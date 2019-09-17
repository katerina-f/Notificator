import os


class Config(object):

    SQLALCHEMY_BASE_URI = os.environ.get('SQLALCHEMY_BASE_URI') or \
                          'postgresql+psycopg2://{}:{}@{}/{}'.format(
                          'test', '1234', 'notificator.db', 'postgres')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    INTERVAL = (0,1)
    NOTIFICATION_TIME = os.environ.get('NOTIFICATION_TIME')

    ADMIN = os.environ.get('ADMIN')
    RECIPIENTS = [ADMIN]
