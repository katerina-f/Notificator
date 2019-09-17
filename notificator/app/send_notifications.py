from loguru import logger

from notificator.app.reminder import Postman
from notificator.app.clients import EmailClient
from notificator.person.model import Person
from notificator.extensions import config


def send_notifications(session):
    """ Notifier - implements all the logic of sending messages """
    logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation='1 week')
    notificator = Postman(config.NOTIFICATION_TIME)
    notificator.subscribe(EmailClient)
    result = notificator.get_data(config.INTERVAL, Person, session)
    if result:
        client = EmailClient()
        client.subscribe_to_queue()
    else:
        logger.warning('no content to send')
