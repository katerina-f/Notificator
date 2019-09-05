import time
import schedule

from notificator.reminder.send_notifications import send_notifications
from notificator.extensions import db
from notificator.extensions import config

def main():
    session = db.create_session()

    # try:
    #     db.engine.connect()
    # except:
    #     db.create_db()

    try:
        schedule.every().day.at(config.NOTIFICATION_TIME).do(send_notifications, session=session)
        while 1:
            schedule.run_pending()
            time.sleep(1)
    except schedule.ScheduleError as ex:
        # logger.warning(ex.__str__())
        with open(config.LOGFILE, 'w') as f:
            f.write(ex.__str__)


if __name__ == '__main__':
    main()
