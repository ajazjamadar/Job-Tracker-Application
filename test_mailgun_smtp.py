"""
Test Mailgun SMTP configuration
"""
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection to Mailgun"""
    print("=" * 60)
    print("MAILGUN SMTP CONNECTION TEST")
    print("=" * 60)
    
    # Get configuration from environment
    mail_server = os.environ.get('MAIL_SERVER')
    mail_port = int(os.environ.get('MAIL_PORT', 587))
    mail_username = os.environ.get('MAIL_USERNAME')
    mail_password = os.environ.get('MAIL_PASSWORD')
    mail_sender = os.environ.get('MAIL_DEFAULT_SENDER')
    
    print(f"\n--- Configuration ---")
    print(f"MAIL_SERVER: {mail_server}")
    print(f"MAIL_PORT: {mail_port}")
    print(f"MAIL_USERNAME: {mail_username}")
    print(f"MAIL_PASSWORD: {'*' * 20 if mail_password else '(Not set)'}")
    print(f"MAIL_DEFAULT_SENDER: {mail_sender}")
    
    if not all([mail_server, mail_username, mail_password, mail_sender]):
        print("\n❌ ERROR: Missing email configuration")
        print("Please ensure all MAIL_* variables are set in .env file")
        return False
    
    try:
        print(f"\n--- Testing Connection ---")
        print(f"Connecting to {mail_server}:{mail_port}...")
        
        # Create SMTP connection
        server = smtplib.SMTP(mail_server, mail_port)
        server.set_debuglevel(0)  # Set to 1 for verbose output
        
        print("✓ Connection established")
        
        # Start TLS encryption
        print("Starting TLS encryption...")
        server.starttls()
        print("✓ TLS encryption started")
        
        # Login
        print(f"Logging in as {mail_username}...")
        server.login(mail_username, mail_password)
        print("✓ Login successful")
        
        # Create test email
        recipient = "ajaxjamadar121@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = mail_sender
        msg['To'] = recipient
        msg['Subject'] = "Test Email from Job Application Tracker"
        
        body = """
Hello!

This is a test email from your Job Application Tracker application.

Your Mailgun SMTP configuration is working correctly! 🎉

You can now:
- Receive welcome emails when registering
- Get application reminders
- Receive status change notifications

Best regards,
Job Application Tracker Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print(f"\nSending test email to {recipient}...")
        server.send_message(msg)
        print("✓ Email sent successfully!")
        
        # Close connection
        server.quit()
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - Mailgun SMTP is configured correctly!")
        print("=" * 60)
        print(f"\nCheck your inbox at {recipient}")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION ERROR: {e}")
        print("\nPossible issues:")
        print("1. Incorrect API key/password")
        print("2. MAIL_USERNAME should be: postmaster@sandbox164383bdb1864606b4c832581a4e2b83.mailgun.org")
        print("3. MAIL_PASSWORD should be your Mailgun API key")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP ERROR: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_smtp_connection()
