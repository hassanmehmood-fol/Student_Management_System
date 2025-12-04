# Student_Management_System/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Correct project settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Student_Management_System.settings')

app = Celery('Student_Management_System')

# Load Celery config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
