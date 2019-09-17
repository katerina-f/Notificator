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

This application uses Postgres. If you use a different database, change the name of the variables in the environment file, the description of the service in docker-compose!

###### Example
```
./docker-compose.yml

...

services:
  database:
    container_name: notificator.db
    image: mysql:5.7  # here
    ports:
      - 3306:3306  # here
    volumes:
      - notificator.db:/var/lib/mysql  # and here
    env_file:
      - ./.env

...
```

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
POSTGRES_USER=<user-for-your-database>  # change to MYSQL_USER for example if you use different db
POSTGRES_PASSWORD=<password-for-your-db>  # change to MYSQL_PASSWORD for the same reason
TZ=<your-time-zone>
SQLALCHEMY_BASE_URI=<uri-for-your-db>  # use the driver spicific for your db
ADMIN=<who-will-recieve-notifications>
```
By default, the interval by day of birth is set as notification day to day and one day before the birthday. The interval is set to a tuple in notificator / config.py, you can change it as you wish

###### Example

```
notificator/config.py

...

INTERVAL = (0, 3, 7)  # here we are change interval between birthday and notifications days before - 3 days                         # and week respectively

...
```

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
