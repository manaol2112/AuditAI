import os
from celery import Celery
from celery.schedules import timedelta
# Set the Django settings module explicitly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AUDITAI.settings')
app = Celery('AUDITAI')
# Load settings from Django settings module
app.config_from_object('django.conf:settings', namespace='CELERY')
# Define a periodic task to run every 20 seconds
app.conf.beat_schedule = {
    'fetch_files_task': {
        'task': 'appAUDITAI.tasks.fetch_files_from_sftp',
        'schedule': timedelta(seconds=60),
    },
    'process_file_task': {  # Unique key for the new task
        'task': 'appAUDITAI.tasks.process_file_from_server',  # Task function to execute
        'schedule': timedelta(seconds=10),
    },
}
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
