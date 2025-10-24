"""
Test Mailgun API email functions
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.email_mailgun import send_email_mailgun

def test_mailgun_email():
    """Test sending email via Mailgun API"""
    print("=" * 60)
    print("MAILGUN API EMAIL TEST")
    print("=" * 60)
    
    # Check configuration
    mailgun_api_key = os.environ.get('MAILGUN_API_KEY', os.environ.get('MAIL_PASSWORD'))
    mailgun_domain = os.environ.get('MAILGUN_DOMAIN', 'sandbox164383bdb1864606b4c832581a4e2b83.mailgun.org')
    
    print(f"\nConfiguration:")
    print(f"MAILGUN_DOMAIN: {mailgun_domain}")
    print(f"MAILGUN_API_KEY: {'*' * 20 if mailgun_api_key else '(Not set)'}")
    
    if not mailgun_api_key:
        print("\n❌ ERROR: MAILGUN_API_KEY not set")
        return
    
    # Send test email
    print(f"\nSending test email...")
    
    subject = "Test Email from Job Application Tracker"
    recipient = "ajaxjamadar121@gmail.com"
    
    text_body = """
Hello!

This is a test email from your Job Application Tracker application using the Mailgun API.

Your email configuration is working correctly! 🎉

You can now:
- Receive welcome emails when registering
- Get application reminders  
- Receive status change notifications

Best regards,
Job Application Tracker Team
    """
    
    html_body = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #0d6efd;">Test Email Success!</h2>
    <p>Hello!</p>
    <p>This is a test email from your Job Application Tracker application using the <strong>Mailgun API</strong>.</p>
    
    <p>Your email configuration is working correctly! 🎉</p>
    
    <h3>You can now:</h3>
    <ul>
        <li>Receive welcome emails when registering</li>
        <li>Get application reminders</li>
        <li>Receive status change notifications</li>
    </ul>
    
    <p>Best regards,<br>
    Job Application Tracker Team</p>
</body>
</html>
    """
    
    send_email_mailgun(subject, recipient, text_body, html_body)
    
    print(f"\n✓ Email queued for sending to {recipient}")
    print(f"  (Check the terminal output for confirmation)")
    print("\n" + "=" * 60)
    print("Check your inbox at ajaxjamadar121@gmail.com")
    print("=" * 60)
    
    # Give the background thread a moment to complete
    import time
    time.sleep(2)

if __name__ == "__main__":
    test_mailgun_email()
