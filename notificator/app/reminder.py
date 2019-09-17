import json

from datetime import datetime
from datetime import timedelta

import pika

from sqlalchemy import and_
from sqlalchemy import extract
from loguru import logger

from notificator.extensions import config


class BdayFinder:
    """
    Класс ищет пользователей по заданным ему параметрам в базе и
    отдает полученные данные

    """

    def __init__(self, model=None, interval=(), session=None):
        self.obj = model
        self.interval = interval
        self.session = session

    def find_persons_for_date(self, remind_date):

        """
        Принимает количество дней до искомой даты,
        вычисляет день рождения, ищет пользователей с этим днем рождения в базе.
        """

        date = datetime.today() + timedelta(days=int(remind_date))

        b_day = extract('day', self.obj.birth_date)
        b_month = extract('month', self.obj.birth_date)

        query = self.session.query(self.obj).filter(and_(b_day == date.day, b_month == date.month))
        persons = query.all()
        if not persons:
            return

        persons = [{'bdate': '{}'.format(person.birth_date),
                  'first_name': '{}'.format(person.first_name),
                  'last_name': '{}'.format(person.last_name),
                  'days_to_birthday': remind_date} for person in persons]
        return persons

    def creating_persons_list(self):

        """ генерирует json для передачи в очередь """
        persons_list = {'all_dates': [{'date': date, 'persons': self.find_persons_for_date(date)} for date in self.interval]}

        if any(persons_list['all_dates'][i]['persons'] for i in range(len(persons_list['all_dates']))):
            return json.dumps(persons_list)

        else:
            return {}


class Postman:
    """
    Подписывает на себя нужных клиентов, создает очередь передачи данных,
    принимает время оповещения, отправляет сообщение клиенту
    """

    def __init__(self, notification_time):
        self.subscribers = set()
        self.notification_time = notification_time  #<type 'str'>

    def get_data(self, interval, obj, session):
        """
        Создает очередь отправки сообщений, получает от поисковика результат,
        если он есть, вызывает метод оповещения
        """

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='notificator.mq'))
        finder = BdayFinder(obj, interval, session)
        result = finder.creating_persons_list()

        if result:
            self.notify(connection, result)
        return result

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubcribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def create_queue(self, subscriber, connection):
        """ Создает очередь для отправки клиенту """
        logger.warning('создалась очередь')
        channel = connection.channel()
        channel.queue_declare(queue=subscriber.__name__, durable=True)
        return channel

    @logger.catch(level='ERROR')
    def notify(self, connection, message):
        """
        Подключает всех клиентов к очередям отправки сообщений,
        отправлет в очереди сообщения.
        """

        for subscriber in self.subscribers:
            channel = self.create_queue(subscriber, connection)
            channel.basic_publish(exchange='',
                                  routing_key=subscriber.__name__,
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
        connection.close()
