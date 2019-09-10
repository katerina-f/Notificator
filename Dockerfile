FROM python:3.6
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN apt-get update
RUN pip3 install -r requirements.txt
CMD ["python3", "runserver.py", "&"]
