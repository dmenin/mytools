import requests
from celery import Celery

app = Celery()#'TasksFile', broker = 'amqp://guest:guest@127.0.0.1//')
app.config_from_object('config')

@app.task
def reverse(string):
    return string [::-1]

@app.task
def fetch_url(url):
    r = requests.get(url)
    return r.status_code
    
#commnad 1:
#celery -A TasksFile worker --loglevel=info