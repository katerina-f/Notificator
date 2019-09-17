# Notificator


This application will allow you to receive notifications by mail about the birthdays of persons whose data is stored in your database.

## Getting Started


All you need is to have a database that stores data about persons with the following fields:
```
first_name
last_name
birth_date
```
or change the names of the fields in the
```
notificator / app / reminder.py
 ```
module code in lines 36 - 46

### Primarily

This application uses Postgres. If you use a different database, change the name of the variables in the environment file, in the notificator / config.py module, the description of the service in docker-compose!

Before install the app, you need to create the
```
.env
```
file for environment variables. What variables you need in this app:
```
NOTIFICATION_TIME=<alert-time>
COMPOSE_PROJECT_NAME=notificator
MAIL_USERNAME=<your-mail-address>
MAIL_PASSWORD=<your-mail-password>
MAIL_PORT=<mail-port>
MAIL_SERVER=<mail-server>
POSTGRES_USER=<user-for-your-database>
POSTGRES_PASSWORD=<password-for-your-db>
TZ=<your-time-zone>
SQLALCHEMY_BASE_URI=<uri-for-your-db>
ADMIN=<who-will-recieve-notifications>
```
By default, the interval by day of birth is set as notification day to day and one day before the birthday. The interval is set to a tuple in notificator / config.py, you can change it as you wish

### Instalation

To install and run the code in the docker containers,
make script
```
run.sh
```
executable
```
chmod +x ./run.sh
```

This script will start building the postgresql, rabbitmq services and our application. If you are using a different database, modify the docker-compose file!

and run it in the project root
```
./run.sh
```

## Authors

* **Katerina Frolova** - *Initial work* - [katyfrolova](https://github.com/katyfrolova)
