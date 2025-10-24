"""Email utility functions for sending notifications"""
from flask import render_template
from flask_mail import Message
from . import mail, app
from threading import Thread


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body=None, html_body=None):
    """
    Send email with both text and HTML body.
    
    Args:
        subject: Email subject line
        recipients: List of recipient email addresses
        text_body: Plain text email body
        html_body: HTML email body
    """
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Send email asynchronously to avoid blocking
    Thread(target=send_async_email, args=(app, msg)).start()


def send_welcome_email(user):
    """Send welcome email to new user"""
    subject = "Welcome to Job Application Tracker!"
    recipients = [user.email]
    text_body = f"""
Hi {user.name or 'there'},

Welcome to Job Application Tracker!

We're excited to help you organize and track your job applications.

Here's what you can do:
- Add new job applications
- Track application status
- Set follow-up reminders
- View your application statistics

Get started by logging in and adding your first application!

Best regards,
The Job Tracker Team
"""
    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #0d6efd;">Welcome to Job Application Tracker!</h2>
    <p>Hi {user.name or 'there'},</p>
    <p>We're excited to help you organize and track your job applications.</p>
    
    <h3>Here's what you can do:</h3>
    <ul>
        <li>Add new job applications</li>
        <li>Track application status</li>
        <li>Set follow-up reminders</li>
        <li>View your application statistics</li>
    </ul>
    
    <p>Get started by logging in and adding your first application!</p>
    
    <p>Best regards,<br>
    The Job Tracker Team</p>
</body>
</html>
"""
    send_email(subject, recipients, text_body, html_body)


def send_application_reminder(user, application):
    """Send reminder email for application follow-up"""
    subject = f"Reminder: Follow up with {application.company}"
    recipients = [user.email]
    text_body = f"""
Hi {user.name or 'there'},

This is a reminder to follow up on your application to {application.company}.

Application Details:
- Company: {application.company}
- Position: {application.position or 'N/A'}
- Status: {application.status}
- Applied on: {application.date_applied.strftime('%B %d, %Y') if application.date_applied else 'N/A'}
- Follow-up date: {application.follow_up_date.strftime('%B %d, %Y') if application.follow_up_date else 'N/A'}

Notes: {application.notes or 'None'}

Good luck with your application!

Best regards,
The Job Tracker Team
"""
    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #0d6efd;">Follow-up Reminder</h2>
    <p>Hi {user.name or 'there'},</p>
    <p>This is a reminder to follow up on your application to <strong>{application.company}</strong>.</p>
    
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0d6efd; margin: 20px 0;">
        <h3 style="margin-top: 0;">Application Details</h3>
        <p><strong>Company:</strong> {application.company}</p>
        <p><strong>Position:</strong> {application.position or 'N/A'}</p>
        <p><strong>Status:</strong> <span style="padding: 3px 8px; background-color: #0dcaf0; color: white; border-radius: 3px;">{application.status}</span></p>
        <p><strong>Applied on:</strong> {application.date_applied.strftime('%B %d, %Y') if application.date_applied else 'N/A'}</p>
        <p><strong>Follow-up date:</strong> {application.follow_up_date.strftime('%B %d, %Y') if application.follow_up_date else 'N/A'}</p>
        {f'<p><strong>Notes:</strong> {application.notes}</p>' if application.notes else ''}
    </div>
    
    <p>Good luck with your application!</p>
    
    <p>Best regards,<br>
    The Job Tracker Team</p>
</body>
</html>
"""
    send_email(subject, recipients, text_body, html_body)


def send_status_change_notification(user, application, old_status, new_status):
    """Send notification when application status changes"""
    subject = f"Status Update: {application.company} - {new_status}"
    recipients = [user.email]
    text_body = f"""
Hi {user.name or 'there'},

Your application status has been updated!

Company: {application.company}
Position: {application.position or 'N/A'}
Old Status: {old_status}
New Status: {new_status}

Keep up the great work on your job search!

Best regards,
The Job Tracker Team
"""
    
    # Status color mapping
    status_colors = {
        'Applied': '#0dcaf0',
        'Interview': '#ffc107',
        'Offer': '#198754',
        'Accepted': '#198754',
        'Rejected': '#dc3545',
        'Withdrawn': '#6c757d'
    }
    
    html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #0d6efd;">Application Status Update</h2>
    <p>Hi {user.name or 'there'},</p>
    <p>Your application status has been updated!</p>
    
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #0d6efd; margin: 20px 0;">
        <p><strong>Company:</strong> {application.company}</p>
        <p><strong>Position:</strong> {application.position or 'N/A'}</p>
        <p><strong>Old Status:</strong> <span style="padding: 3px 8px; background-color: {status_colors.get(old_status, '#6c757d')}; color: white; border-radius: 3px;">{old_status}</span></p>
        <p><strong>New Status:</strong> <span style="padding: 3px 8px; background-color: {status_colors.get(new_status, '#6c757d')}; color: white; border-radius: 3px;">{new_status}</span></p>
    </div>
    
    <p>Keep up the great work on your job search!</p>
    
    <p>Best regards,<br>
    The Job Tracker Team</p>
</body>
</html>
"""
    send_email(subject, recipients, text_body, html_body)
