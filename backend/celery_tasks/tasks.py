import logging
import requests
from celery_tasks.celery import app


@app.task(name='tasks.fetch_icon')
def fetch_icon(icon_url, image_path):
    logging.info('fetch icon: {}'.format(icon_url))
    r = requests.get(icon_url, stream=True)
    if r.status_code == 200:
        with open(image_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
