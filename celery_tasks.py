"""
Celery tasks for background job processing.

Tasks:
    - send_daily_reminders_task: Send reminders for applications due today
    - send_upcoming_reminders_task: Send reminders for upcoming follow-ups
    - send_welcome_email_task: Send welcome email asynchronously
"""

from celery_app import celery_app
from app.scheduler import send_daily_reminders, send_upcoming_reminders
from app.email import send_welcome_email
from app.models import User
from app import app


@celery_app.task(name='celery_tasks.send_daily_reminders_task')
def send_daily_reminders_task():
    """
    Celery task to send daily follow-up reminders.
    Scheduled to run daily at 9:00 AM.
    """
    return send_daily_reminders()


@celery_app.task(name='celery_tasks.send_upcoming_reminders_task')
def send_upcoming_reminders_task(days_ahead=3):
    """
    Celery task to send upcoming follow-up reminders.
    Scheduled to run weekly on Monday at 8:00 AM.
    
    Args:
        days_ahead: Number of days to look ahead (default: 3)
    """
    return send_upcoming_reminders(days_ahead)


@celery_app.task(name='celery_tasks.send_welcome_email_task')
def send_welcome_email_task(user_id):
    """
    Celery task to send welcome email asynchronously.
    
    Args:
        user_id: ID of the user to send welcome email to
    """
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            send_welcome_email(user)
            return f"Welcome email sent to {user.email}"
        return f"User {user_id} not found"


# Example: Trigger tasks manually
if __name__ == '__main__':
    # Send daily reminders now
    result = send_daily_reminders_task.delay()
    print(f"Task submitted: {result.id}")
    
    # Get result
    print(f"Result: {result.get(timeout=30)}")
