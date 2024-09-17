from celery import shared_task
from time import sleep


@shared_task
def example_task():
    print('This is an example task ')
    sleep(10)
    return "Task finish"
