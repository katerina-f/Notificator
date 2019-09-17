FROM python:3.6
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python3", "runserver.py"]
