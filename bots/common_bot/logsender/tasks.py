from celery import shared_task, Celery
from .backup_sql import *

app = Celery('task', broker='redis://localhost:6379/0')


@shared_task
def backup_database_task():
    backup_database()



