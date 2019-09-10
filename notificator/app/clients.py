from abc import ABC
from abc import abstractmethod
import json
from datetime import datetime
import os

import pika
from loguru import logger
from notificator.app.mail import Sender


"""Шаблоны для отправки в разные клиенты."""

class AbstractClient(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def callback(self, *args, **kwargs):
        pass

    def parsing_request(self, body):
        """ Преобразует строку из очереди """
        msg_body = json.loads(body)
        header = f'Не забудьте поздравить!\n'
        for day in msg_body['all_dates']:
            user_data = f'\tДень рождения через {day["date"]}:\n'
            if day['users']:
                for user in day['users']:
                    user_data += f'\t{user["first_name"]} {user["last_name"]}\n'
            else:
                user_data += f'Нет именниников!'
            header += user_data
        return header

    @abstractmethod
    def subscribe_to_queue(self):
        pass


class EmailClient(AbstractClient):
    def __init__(self):
        pass

    def update(self, message):
        """Создает объект отправителя, отправляет сообщение"""
        sender = Sender(message, 'Birthdays')
        try:
            sender.send_message()
        except Exception:
            logger.warning(Exception.__str__(self))

    @logger.catch(level='ERROR')
    def callback(self, ch, method, properties, body):
        """ Принимает сообщение из очереди, инициирует отправку сообщения."""
        logger.warning('подключение прошло успешно')
        msg_body = self.parsing_request(body)
        self.update(msg_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    @logger.catch(level='ERROR')
    def subscribe_to_queue(self):
        """ Проводит операции с очередью - подключение, отправку ответа, закрытие соединения"""
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='notificator.mq'))
        channel = connection.channel()
        channel.queue_declare(queue=__class__.__name__, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(__class__.__name__, self.callback, auto_ack=False)
        try:
            channel.start_consuming()
            logger.warning('сообщение отправлено')
            connection.close()
        except:
            logger.warning('не удалось отправить сообщение. соединение отключено')
            channel.stop_consuming()
            connection.close()


class SMSClient(AbstractClient):
    def __init__(self):
        pass

    def callback(self, *args, **kwargs):
        pass

    def update(self):
        pass


class SlackClient(AbstractClient):
    def __init__(self):
        pass

    def callback(self, *args, **kwargs):
        pass

    def update(self):
        pass
