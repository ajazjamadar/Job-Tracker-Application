"""
Route tests
"""
import pytest
from app import db
from app.models import JobApplication


def test_index_page(client):
    """Test index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Job Application Tracker' in response.data


def test_dashboard_requires_login(client):
    """Test dashboard requires authentication."""
    response = client.get('/dashboard')
    assert response.status_code == 302  # Redirect to login


def test_dashboard_logged_in(client, auth, user):
    """Test dashboard access when logged in."""
    auth.login()
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_applications_list_requires_login(client):
    """Test applications list requires authentication."""
    response = client.get('/applications')
    assert response.status_code == 302


def test_applications_list_logged_in(client, auth, user):
    """Test applications list when logged in."""
    auth.login()
    response = client.get('/applications', follow_redirects=True)
    assert response.status_code == 200
    assert b'Applications' in response.data


def test_new_application_get(client, auth, user):
    """Test GET request to new application form."""
    auth.login()
    response = client.get('/applications/new')
    assert response.status_code == 200
    assert b'Company' in response.data
    assert b'Position' in response.data


def test_new_application_post(client, auth, user, app):
    """Test creating a new application."""
    auth.login()
    
    response = client.post(
        '/applications/new',
        data={
            'company': 'Microsoft',
            'position': 'Software Developer',
            'status': 'Applied',
            'application_date': '2025-10-20',
            'notes': 'Applied through LinkedIn'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    # Verify application was created
    with app.app_context():
        app_obj = JobApplication.query.filter_by(company='Microsoft').first()
        assert app_obj is not None
        assert app_obj.position == 'Software Developer'
        assert app_obj.user_id == user.id


def test_edit_application_get(client, auth, user, application):
    """Test GET request to edit application form."""
    auth.login()
    response = client.get(f'/applications/{application.id}/edit')
    assert response.status_code == 200
    assert b'Test Company' in response.data


def test_edit_application_post(client, auth, user, application, app):
    """Test updating an application."""
    auth.login()
    
    response = client.post(
        f'/applications/{application.id}/edit',
        data={
            'company': 'Updated Company',
            'position': 'Senior Engineer',
            'status': 'Interview',
            'application_date': '2025-10-20',
            'notes': 'Updated notes'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    # Verify application was updated
    with app.app_context():
        updated_app = JobApplication.query.get(application.id)
        assert updated_app.company == 'Updated Company'
        assert updated_app.status == 'Interview'


def test_delete_application(client, auth, user, application, app):
    """Test deleting an application."""
    auth.login()
    
    app_id = application.id
    response = client.post(
        f'/applications/{app_id}/delete',
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    # Verify application was deleted
    with app.app_context():
        deleted_app = JobApplication.query.get(app_id)
        assert deleted_app is None


def test_user_isolation(client, auth, app):
    """Test that users can only see their own applications."""
    # Create two users
    with app.app_context():
        from app.models import User
        
        user1 = User(name='User1', email='user1@example.com')
        user1.set_password('password')
        db.session.add(user1)
        
        user2 = User(name='User2', email='user2@example.com')
        user2.set_password('password')
        db.session.add(user2)
        db.session.commit()
        
        # Create application for user1
        app1 = JobApplication(company='User1 Company', position='Dev', user_id=user1.id)
        db.session.add(app1)
        db.session.commit()
        
        app1_id = app1.id
    
    # Login as user2
    auth.login('user2@example.com', 'password')
    
    # Try to access user1's application
    response = client.get(f'/applications/{app1_id}/edit')
    assert response.status_code == 404  # Should not be found


def test_search_applications(client, auth, user, app):
    """Test search functionality."""
    with app.app_context():
        # Create multiple applications
        apps = [
            JobApplication(company='Google', position='Engineer', status='Applied', user_id=user.id),
            JobApplication(company='Microsoft', position='Developer', status='Interview', user_id=user.id),
            JobApplication(company='Amazon', position='SDE', status='Applied', user_id=user.id),
        ]
        db.session.add_all(apps)
        db.session.commit()
    
    auth.login()
    
    # Search by company
    response = client.get('/applications?company=Google')
    assert response.status_code == 200
    assert b'Google' in response.data
    
    # Search by status
    response = client.get('/applications?status=Interview')
    assert response.status_code == 200
    assert b'Microsoft' in response.data


def test_pagination(client, auth, user, app):
    """Test pagination with more than 10 applications."""
    with app.app_context():
        # Create 15 applications
        for i in range(15):
            job_app = JobApplication(
                company=f'Company {i}',
                position='Engineer',
                status='Applied',
                user_id=user.id
            )
            db.session.add(job_app)
        db.session.commit()
    
    auth.login()
    
    # First page
    response = client.get('/applications?page=1')
    assert response.status_code == 200
    assert b'Company 0' in response.data
    
    # Second page
    response = client.get('/applications?page=2')
    assert response.status_code == 200
    # Should have remaining applications
