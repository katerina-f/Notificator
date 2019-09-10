from datetime import datetime
from datetime import timedelta
import json

from sqlalchemy import and_
from sqlalchemy import extract
import pika

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

    def find_users_for_date(self, remind_date):
        """
        Принимает количество дней до искомой даты,
        вычисляет день рождения, ищет пользователей с этим днем рождения в базе.
        """

        date = datetime.today() + timedelta(days=int(remind_date))

        b_day = extract('day', self.obj.birth_date)
        b_month = extract('month', self.obj.birth_date)

        query = self.session.query(self.obj).filter(and_(b_day == date.day, b_month == date.month))
        users = query.all()
        if not users:
            return

        users = [{'bdate': '{}'.format(user.birth_date),
                  'first_name': '{}'.format(user.first_name),
                  'last_name': '{}'.format(user.last_name),
                  'days_to_birthday': remind_date} for user in users]
        return users

    def creating_users_list(self):
        """ генерирует json для передачи в очередь """
        users_list = {'all_dates': [{'date': date, 'users': self.find_users_for_date(date)}
                      for date in self.interval]}
        if any(users_list['all_dates'][i]['users'] for i in range(len(users_list['all_dates']))):
            return json.dumps(users_list)
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

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
        finder = BdayFinder(obj, interval, session)
        result = finder.creating_users_list()
        if result:
            self.notify(connection, result)
        return result

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubcribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def create_queue(self, subscriber, connection):
        """ Создает очередь для отправки клиенту """
        # logger.warning('создалась очередь')
        channel = connection.channel()
        channel.queue_declare(queue=subscriber.__name__, durable=True)
        return channel

    def notify(self, connection, message):
        """
        Подключает всех клиентов к очередям отправки сообщений,
        отправлет в очереди сообщения.
        """

        for subscriber in self.subscribers:
            channel = self.create_queue(subscriber, connection)
            print(channel)
            channel.basic_publish(exchange='',
                                  routing_key=subscriber.__name__,
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
        print('Сообщение отправлено в очередь')
        connection.close()