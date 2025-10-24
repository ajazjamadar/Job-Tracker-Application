"""
Celery configuration for background tasks.

Installation:
    pip install celery redis

Setup Redis (required for Celery):
    - Windows: Download from https://github.com/microsoftarchive/redis/releases
    - Linux: sudo apt-get install redis-server
    - Mac: brew install redis
    
    Start Redis:
    - Windows: redis-server.exe
    - Linux/Mac: redis-server

Usage:
    1. Start Celery worker:
       celery -A celery_app worker --loglevel=info
    
    2. Start Celery beat (scheduler):
       celery -A celery_app beat --loglevel=info
    
    3. Or run both together:
       celery -A celery_app worker --beat --loglevel=info
"""

from celery import Celery
from celery.schedules import crontab
import os

# Create Celery instance
celery_app = Celery(
    'job_tracker',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Periodic task schedule
celery_app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'celery_tasks.send_daily_reminders_task',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9:00 AM
    },
    'send-upcoming-reminders': {
        'task': 'celery_tasks.send_upcoming_reminders_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),  # Monday at 8:00 AM
    },
}

if __name__ == '__main__':
    celery_app.start()
