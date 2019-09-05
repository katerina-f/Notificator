from .reminder import Postman
from .clients import EmailClient
from notificator.user.model import User
from notificator.extensions import config


def send_notifications(session):
        # logger.warning('подключение успешно')
        print('Начали слушать')
        notificator = Postman(config.NOTIFICATION_TIME)
        notificator.subscribe(EmailClient)
        result = notificator.get_data(config.INTERVAL, User, session)

        if result:
            print(result)
            client = EmailClient()
            client.subscribe_to_queue()
        else:
            print('нет дней рождения')
            pass
            # logger.warning('нет контента для отправки')
