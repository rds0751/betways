from __future__ import absolute_import, unicode_literals

import os
import sys
import django

from celery import Celery

os.environ.setdefault('DJANGOS_SETTINGS_MODULE', 'aboota.settings')

app = Celery('aboota')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aboota.settings.settings')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../aboota')))
django.setup()
from django.conf import settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)