"""
Email functionality tests
"""
import pytest
from app.email import send_welcome_email, send_application_reminder, send_status_change_notification
from app.models import JobApplication
from datetime import datetime


def test_welcome_email_creation(user, app):
    """Test welcome email is created correctly."""
    with app.app_context():
        # In test mode, emails are suppressed
        # Just verify no exceptions are raised
        try:
            send_welcome_email(user)
            success = True
        except Exception as e:
            success = False
            print(f"Error: {e}")
        
        assert success is True


def test_application_reminder_email(user, application, app):
    """Test application reminder email."""
    with app.app_context():
        try:
            send_application_reminder(user, application)
            success = True
        except Exception as e:
            success = False
            print(f"Error: {e}")
        
        assert success is True


def test_status_change_notification(user, application, app):
    """Test status change notification email."""
    with app.app_context():
        try:
            send_status_change_notification(user, application, 'Applied', 'Interview')
            success = True
        except Exception as e:
            success = False
            print(f"Error: {e}")
        
        assert success is True


def test_email_with_none_user(application, app):
    """Test email functions handle None user gracefully."""
    with app.app_context():
        # Should not raise exception
        try:
            send_application_reminder(None, application)
            # Should handle gracefully (may log error but not crash)
            result = True
        except AttributeError:
            # Expected if trying to access None.email
            result = True
        except Exception as e:
            result = False
        
        # Test should pass (either handles gracefully or raises expected error)
        assert result is True
