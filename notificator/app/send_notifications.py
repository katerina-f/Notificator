from notificator.app.reminder import Postman
from notificator.app.clients import EmailClient
from notificator.user.model import User
from notificator.extensions import config

from loguru import logger


def send_notifications(session):
    """ Нотификатор - осуществляет всю логику отправки сообщений """
    logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation='1 week')
    notificator = Postman(config.NOTIFICATION_TIME)
    notificator.subscribe(EmailClient)
    result = notificator.get_data(config.INTERVAL, User, session)
    logger.warning('подключение успешно')
    if result:
        client = EmailClient()
        client.subscribe_to_queue()
    else:
        print('нет дней рождения')
        logger.warning('нет контента для отправки')
