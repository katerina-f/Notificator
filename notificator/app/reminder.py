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
    The class searches for users according to the parameters specified in the database
    and gives the received data
    """

    def __init__(self, model=None, interval=(), session=None):
        self.obj = model
        self.interval = interval
        self.session = session

    def find_persons_for_date(self, remind_date):

        """
        Accepts the number of days before the desired date,
        calculates a birthday, searches for users with this birthday in the database.
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

        """ generates json to queue """
        persons_list = {'all_dates': [{'date': date, 'persons': self.find_persons_for_date(date)} for date in self.interval]}

        if any(persons_list['all_dates'][i]['persons'] for i in range(len(persons_list['all_dates']))):
            return json.dumps(persons_list)

        else:
            return {}


class Postman:
    """
    Signs on the right customers, creates a data transfer queue,
    takes a notification time, sends a message to the client
    """

    def __init__(self, notification_time):
        self.subscribers = set()
        self.notification_time = notification_time  #<type 'str'>

    def get_data(self, interval, obj, session):
        """
        Creates a queue for sending messages, receives the result from the search engine,
        if it is, calls the notification method
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
        """ Creates a queue for sending to a client """
        logger.warning('queue created')
        channel = connection.channel()
        channel.queue_declare(queue=subscriber.__name__, durable=True)
        return channel

    @logger.catch(level='ERROR')
    def notify(self, connection, message):
        """
        Connects all clients to message sending queues,
        sends queued messages.
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
