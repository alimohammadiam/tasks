from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تنظیمات پایه پروژه را از فایل settings.py بخوانید
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_gateway2.settings')

app = Celery('bank_gateway2')

# از تنظیمات Django برای تنظیمات Celery استفاده کنید
app.config_from_object('django.conf:settings', namespace='CELERY')

# جستجو و ثبت خودکار Taskها از فایل‌های tasks.py
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
