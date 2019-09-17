import json

import os

from abc import ABC
from abc import abstractmethod
from datetime import datetime

import pika

from loguru import logger

from notificator.app.mail import Sender


"""Templates for sending to different clients."""

class AbstractClient(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def callback(self, *args, **kwargs):
        pass

    def parsing_request(self, body):
        """ Converts a string from a queue """
        msg_body = json.loads(body)
        header = f'Do not forget to congratulate!\n'
        for day in msg_body['all_dates']:
            person_data = f'\tBirthday through {day["date"]}:\n'
            if day['persons']:
                for person in day['persons']:
                    person_data += f'\t{person["first_name"]} {person["last_name"]}\n'
            else:
                person_data += f'No birthday!'
            header += person_data
        return header

    @abstractmethod
    def subscribe_to_queue(self):
        pass


class EmailClient(AbstractClient):
    def __init__(self):
        pass

    def update(self, message):
        """Creates a sender object, sends a message"""
        sender = Sender(message, 'Birthdays')
        try:
            sender.send_message()
        except Exception:
            logger.warning(Exception.__str__(self))

    @logger.catch(level='ERROR')
    def callback(self, ch, method, properties, body):
        """ Receives a message from the queue, initiates sending a message."""
        logger.warning('connection was successful')
        msg_body = self.parsing_request(body)
        self.update(msg_body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    @logger.catch(level='ERROR')
    def subscribe_to_queue(self):
        """ Carries out operations with the queue - connecting, sending a response, closing the connection"""
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='notificator.mq'))
        channel = connection.channel()
        channel.queue_declare(queue=__class__.__name__, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(__class__.__name__, self.callback, auto_ack=False)
        try:
            channel.start_consuming()
            logger.warning('Message sent')
            connection.close()
        except:
            logger.warning('failed to send message. connection disconnected')
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
