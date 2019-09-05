from abc import ABC
from abc import abstractmethod
import json
from datetime import datetime
import os

import pika

from .mail import Sender


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
        return msg_body

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
            print('отправляем сообщение')
            sender.send_message()
        except Exception:
            print('something wrong', datetime.now())


    def callback(self, ch, method, properties, body):
        """ Принимает сообщение из очереди, инициирует отправку сообщения."""
        # logger.warning('подключение прошло успешно')
        print('подключились к очереди')
        msg_body = self.parsing_request(body)
        self.update(msg_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    # @logger.catch(level='ERROR')
    def subscribe_to_queue(self):
        """ Проводит операции с очередью - подключение, отправку ответа, закрытие соединения"""
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='0.0.0.0'))
        channel = connection.channel()
        print(channel)
        channel.queue_declare(queue=__class__.__name__, durable=True)
        print('Клиент создал очередь')
        channel.basic_qos(prefetch_count=1)
        print('Принимаем сообщение')
        channel.basic_get(__class__.__name__, self.callback)
        print('Закончили обработку')
        try:
            channel.start_consuming()
            connection.close()
        except:
            # logger.warning('не удалось отправить сообщение. соединение отключено')
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
