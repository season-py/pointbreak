from __future__ import absolute_import
import celery

celery = celery

app = celery.Celery('pointbreak')

app.conf.update(
    BROKER_URL='redis://localhost:6379/0',
    CELERY_IMPORTS=('celery_tasks.tasks', ),
    CELERY_TASK_RESULT_EXPIRES=18000,
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    # CELERY_RESULT_DBURI='mysql://root@localhost:3306/celery',
    # CELERY_RESULT_SERIALIZER='json',
    CELERYD_CONCURRENCY=6,
    CELERYD_PREFETCH_MULTIPLIER=100,
    CELERY_ANNOTATIONS={'*': {'rate_limit': '60/s'}},
    # CELERY_ROUTES={
    # 	'tasks.add': {'queue': 'default'}
    # },
    CELERYBEAT_SCHEDULE={
    },
    CELERY_DEFAULT_QUEUE='celery',
    # CELERY_QUEUES=(
    # 	Queue('celery', Exchange('direct'), routing_key='celery'),
    # )
    # CELERY_QUEUES = (Broadcast('broadcast_tasks'), )
)
