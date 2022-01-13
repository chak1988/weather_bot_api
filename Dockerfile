FROM python:3.9-slim
RUN apt-get update
RUN apt-get install -y
RUN pip3 install flask
RUN pip3 install pytelegrambotapi
RUN pip3 install mongoengine
WORKDIR /weather_bot
COPY . .
COPY webhook_weather_key.pem /etc/ssl/private/webhook_weather_key.pem
COPY webhook_weather_cert.pem /etc/ssl/certs/webhook_weather_cert.pem
RUN pip3 install gunicorn
CMD ["gunicorn"  , "--bind", "0.0.0.0:5000", "my_weather_bot:app"]
