"""Background scheduler for sending follow-up reminders"""
from datetime import date, datetime, timedelta
from flask_mail import Message
from . import mail, app, db
from .models import JobApplication, User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_followup_reminder(user, appn):
    """
    Send follow-up reminder email to user for a specific application.
    
    Args:
        user: User object
        appn: JobApplication object
    """
    try:
        msg = Message(
            subject=f"Follow-up reminder: {appn.company}",
            recipients=[user.email]
        )
        
        # Plain text body
        msg.body = f"""Hi {user.name or user.email},

This is a reminder to follow up with {appn.company} about the {appn.position or 'position'} you applied for.

Follow-up Date: {appn.follow_up_date.strftime('%B %d, %Y') if appn.follow_up_date else 'Today'}
Application Status: {appn.status}
Date Applied: {appn.date_applied.strftime('%B %d, %Y') if appn.date_applied else 'N/A'}

{f'Notes: {appn.notes}' if appn.notes else ''}

Good luck with your follow-up!

Best regards,
Job Application Tracker
"""
        
        # HTML body
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #0d6efd;">Follow-up Reminder</h2>
    <p>Hi {user.name or user.email},</p>
    <p>This is a reminder to follow up with <strong>{appn.company}</strong> about the <strong>{appn.position or 'position'}</strong> you applied for.</p>
    
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0d6efd; margin: 20px 0;">
        <p><strong>Follow-up Date:</strong> {appn.follow_up_date.strftime('%B %d, %Y') if appn.follow_up_date else 'Today'}</p>
        <p><strong>Application Status:</strong> <span style="padding: 3px 8px; background-color: #0dcaf0; color: white; border-radius: 3px;">{appn.status}</span></p>
        <p><strong>Date Applied:</strong> {appn.date_applied.strftime('%B %d, %Y') if appn.date_applied else 'N/A'}</p>
        {f'<p><strong>Notes:</strong> {appn.notes}</p>' if appn.notes else ''}
    </div>
    
    <p>Good luck with your follow-up!</p>
    
    <p>Best regards,<br>
    Job Application Tracker</p>
</body>
</html>
"""
        
        mail.send(msg)
        logger.info(f"Sent follow-up reminder to {user.email} for {appn.company}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send reminder to {user.email}: {str(e)}")
        return False


def send_daily_reminders():
    """
    Check for applications with follow-up dates today and send reminders.
    This function should be called daily by a scheduler.
    
    Returns:
        dict: Summary of reminders sent
    """
    with app.app_context():
        today = date.today()
        
        # Find applications with follow-up date = today
        # Only send for Applied and Interview statuses
        applications = JobApplication.query.filter(
            JobApplication.follow_up_date == today,
            JobApplication.status.in_(['Applied', 'Interview'])
        ).all()
        
        sent_count = 0
        failed_count = 0
        
        logger.info(f"Found {len(applications)} applications needing follow-up reminders")
        
        for appn in applications:
            user = User.query.get(appn.user_id)
            if user and user.email:
                if send_followup_reminder(user, appn):
                    sent_count += 1
                else:
                    failed_count += 1
            else:
                logger.warning(f"No user found for application {appn.id}")
                failed_count += 1
        
        summary = {
            'date': today.strftime('%Y-%m-%d'),
            'total_applications': len(applications),
            'sent': sent_count,
            'failed': failed_count
        }
        
        logger.info(f"Reminder summary: {summary}")
        return summary


def send_upcoming_reminders(days_ahead=3):
    """
    Send reminders for applications with follow-up dates in the next N days.
    
    Args:
        days_ahead: Number of days to look ahead (default: 3)
    
    Returns:
        dict: Summary of reminders sent
    """
    with app.app_context():
        today = date.today()
        future_date = today + timedelta(days=days_ahead)
        
        # Find applications with follow-up dates in the next N days
        applications = JobApplication.query.filter(
            JobApplication.follow_up_date >= today,
            JobApplication.follow_up_date <= future_date,
            JobApplication.status.in_(['Applied', 'Interview'])
        ).all()
        
        sent_count = 0
        failed_count = 0
        
        logger.info(f"Found {len(applications)} applications with upcoming follow-ups")
        
        for appn in applications:
            user = User.query.get(appn.user_id)
            if user and user.email:
                if send_followup_reminder(user, appn):
                    sent_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        summary = {
            'date_range': f"{today.strftime('%Y-%m-%d')} to {future_date.strftime('%Y-%m-%d')}",
            'total_applications': len(applications),
            'sent': sent_count,
            'failed': failed_count
        }
        
        logger.info(f"Upcoming reminder summary: {summary}")
        return summary


if __name__ == '__main__':
    # For testing: run daily reminders
    print("Running daily follow-up reminders...")
    result = send_daily_reminders()
    print(f"Results: {result}")
