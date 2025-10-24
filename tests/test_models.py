"""
Database model tests
"""
import pytest
from datetime import datetime, timedelta
from app import db
from app.models import User, JobApplication


def test_user_creation(app):
    """Test creating a user."""
    with app.app_context():
        user = User(name='Test User', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.name == 'Test User'
        assert user.email == 'test@example.com'
        assert user.password_hash is not None


def test_user_password_hashing(app):
    """Test password hashing and verification."""
    with app.app_context():
        user = User(name='Test', email='test@example.com')
        user.set_password('mysecret')
        
        assert user.password_hash != 'mysecret'
        assert user.check_password('mysecret') is True
        assert user.check_password('wrong') is False


def test_user_repr(user):
    """Test user string representation."""
    assert repr(user) == '<User test@example.com>'


def test_job_application_creation(app, user):
    """Test creating a job application."""
    with app.app_context():
        job_app = JobApplication(
            company='Google',
            position='Software Engineer',
            status='Applied',
            application_date=datetime.utcnow().date(),
            user_id=user.id
        )
        db.session.add(job_app)
        db.session.commit()
        
        assert job_app.id is not None
        assert job_app.company == 'Google'
        assert job_app.position == 'Software Engineer'
        assert job_app.status == 'Applied'
        assert job_app.user_id == user.id


def test_job_application_relationship(app, user):
    """Test relationship between User and JobApplication."""
    with app.app_context():
        # Create multiple applications
        app1 = JobApplication(company='Company1', position='Role1', status='Applied', user_id=user.id)
        app2 = JobApplication(company='Company2', position='Role2', status='Interview', user_id=user.id)
        db.session.add_all([app1, app2])
        db.session.commit()
        
        # Query applications
        applications = JobApplication.query.filter_by(user_id=user.id).all()
        
        assert len(applications) == 2
        companies = [a.company for a in applications]
        assert 'Company1' in companies
        assert 'Company2' in companies


def test_job_application_default_values(app, user):
    """Test default values for job application."""
    with app.app_context():
        job_app = JobApplication(
            company='Test Co',
            position='Developer',
            user_id=user.id
        )
        db.session.add(job_app)
        db.session.commit()
        
        # Status should default to 'Applied'
        assert job_app.status == 'Applied'
        # application_date should be set to today
        assert job_app.application_date == datetime.utcnow().date()


def test_job_application_cascade_delete(app):
    """Test that applications are deleted when user is deleted."""
    with app.app_context():
        user = User(name='Delete Me', email='delete@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        job_app = JobApplication(company='Test', position='Dev', user_id=user.id)
        db.session.add(job_app)
        db.session.commit()
        
        app_id = job_app.id
        user_id = user.id
        
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        # Application should be deleted (cascade)
        deleted_app = JobApplication.query.get(app_id)
        assert deleted_app is None


def test_job_application_status_values(app, user):
    """Test different status values."""
    with app.app_context():
        statuses = ['Applied', 'Interview', 'Offer', 'Rejected', 'Accepted']
        
        for status in statuses:
            job_app = JobApplication(
                company=f'Company {status}',
                position='Engineer',
                status=status,
                user_id=user.id
            )
            db.session.add(job_app)
        
        db.session.commit()
        
        for status in statuses:
            apps = JobApplication.query.filter_by(status=status).all()
            assert len(apps) == 1
            assert apps[0].status == status
