import json
import requests
import smtplib
from email.message import EmailMessage
import time
from apscheduler.schedulers.background import BackgroundScheduler

# todo: use config file
url = 'https://api.open-meteo.com/v1/forecast?latitude=59.9375&longitude=30.3086&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=UTC'
# max temperature
m = 15
n = 10
sender = 'weather@mail.com'
receiver = 'user@adress.com'


def report(date, temperature):
    msg = EmailMessage()
    msg.set_content(f'{date} {temperature}')
    msg['From'] = sender
    msg['To'] = receiver
    s = smtplib.SMTP('localhost', 8080)
    s.send_message(msg)
    s.quit()


def check_forecast():
    response = requests.get(url)
    forecast = response.json()

    for i in range(1, 3):
        if forecast['daily']['temperature_2m_max'][i] > m:
            report(forecast['daily']['time'][i], forecast['daily']['temperature_2m_max'][i])


if __name__ == '__main__':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(check_forecast, 'interval', seconds=n)
    scheduler.start()
    try:
        while True:
            time.sleep(3)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
