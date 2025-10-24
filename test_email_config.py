"""Test email configuration and functionality"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app

def test_email_config():
    """Test email configuration"""
    print("="*60)
    print("EMAIL CONFIGURATION TEST")
    print("="*60)
    
    with app.app_context():
        print("\n--- Flask-Mail Configuration ---")
        print(f"MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        print(f"MAIL_PORT: {app.config.get('MAIL_PORT')}")
        print(f"MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        print(f"MAIL_USERNAME: {app.config.get('MAIL_USERNAME') or '(Not set)'}")
        print(f"MAIL_PASSWORD: {'***' if app.config.get('MAIL_PASSWORD') else '(Not set)'}")
        print(f"MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER') or '(Not set)'}")
        
        print("\n--- Configuration Status ---")
        if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
            print("✓ Email credentials configured")
            print("✓ Ready to send emails")
        else:
            print("⚠ Email credentials NOT configured")
            print("\nTo enable email notifications, set these environment variables:")
            print("  MAIL_USERNAME=your-email@gmail.com")
            print("  MAIL_PASSWORD=your-app-password")
            print("  MAIL_DEFAULT_SENDER=your-email@gmail.com")
            print("\nFor Gmail, you need to:")
            print("  1. Enable 2-factor authentication")
            print("  2. Generate an App Password")
            print("  3. Use the App Password (not your regular password)")
        
        print("\n--- Email Functions Available ---")
        from app.email import (
            send_welcome_email,
            send_application_reminder,
            send_status_change_notification
        )
        print("✓ send_welcome_email(user)")
        print("✓ send_application_reminder(user, application)")
        print("✓ send_status_change_notification(user, application, old_status, new_status)")
        
        print("\n--- Usage Example ---")
        print("""
# In your code:
from app.email import send_welcome_email

# After user registration:
send_welcome_email(user)

# For application reminders:
from app.email import send_application_reminder
send_application_reminder(user, application)

# For status changes:
from app.email import send_status_change_notification
send_status_change_notification(user, application, 'Applied', 'Interview')
""")
        
        print("="*60)
        print("\n✓ Email configuration loaded successfully!")
        print("\nNote: Emails will be sent asynchronously in background threads.")
        print("      This prevents blocking the main application.")
        print("="*60)

if __name__ == '__main__':
    test_email_config()
