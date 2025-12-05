from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Student_Management_System.settings')

app = Celery('Student_Management_System')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
