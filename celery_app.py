from celery import Celery
from celery.schedules import crontab
from currencies.parser import CryptoParser


BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'

URL = 'https://coinranking.com/'


app = Celery(__name__, broker=BROKER_URL, backend=BACKEND_URL)


@app.task
def retrieve_currencies():
    _parser = CryptoParser(url=URL)
    _parser.main()


app.conf.beat_schedule = {
    'retrieve_currencies_every_15_min': {
        'task': 'celery_app.retrieve_currencies',
        'schedule': crontab(minute='*/15')
    }
}

app.conf.timezone = 'Europe/Moscow'
