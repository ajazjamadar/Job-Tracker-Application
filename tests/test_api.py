"""
API endpoint tests
"""
import pytest
import json
from app import db
from app.models import JobApplication


def test_api_get_applications_unauthorized(client):
    """Test API GET without authentication."""
    response = client.get('/api/applications')
    # Flask-Login redirects to login page (302), not 401
    assert response.status_code == 302


def test_api_get_applications_empty(client, auth, user):
    """Test API GET with no applications."""
    auth.login()
    response = client.get('/api/applications')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['applications'] == []
    assert data['total'] == 0


def test_api_get_applications(client, auth, user, application):
    """Test API GET with applications."""
    auth.login()
    response = client.get('/api/applications')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total'] == 1
    assert len(data['applications']) == 1
    assert data['applications'][0]['company'] == 'Test Company'


def test_api_post_application(client, auth, user, app):
    """Test API POST to create application."""
    auth.login()
    
    new_app_data = {
        'company': 'API Test Company',
        'position': 'Backend Engineer',
        'status': 'Applied',
        'notes': 'Created via API'
    }
    
    response = client.post(
        '/api/applications',
        data=json.dumps(new_app_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['company'] == 'API Test Company'
    assert data['position'] == 'Backend Engineer'
    
    # Verify in database
    with app.app_context():
        created_app = JobApplication.query.filter_by(company='API Test Company').first()
        assert created_app is not None
        assert created_app.user_id == user.id


def test_api_post_application_missing_fields(client, auth, user):
    """Test API POST with missing required fields."""
    auth.login()
    
    incomplete_data = {
        'company': 'Incomplete Inc'
        # Missing position
    }
    
    response = client.post(
        '/api/applications',
        data=json.dumps(incomplete_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_api_post_application_unauthorized(client):
    """Test API POST without authentication."""
    new_app_data = {
        'company': 'Test',
        'position': 'Dev',
        'status': 'Applied'
    }
    
    response = client.post(
        '/api/applications',
        data=json.dumps(new_app_data),
        content_type='application/json'
    )
    
    # Flask-Login redirects to login page (302), not 401
    assert response.status_code == 302


def test_api_user_isolation(client, auth, app):
    """Test API returns only current user's applications."""
    with app.app_context():
        from app.models import User
        
        # Create two users with applications
        user1 = User(name='User1', email='user1@test.com')
        user1.set_password('password')
        user2 = User(name='User2', email='user2@test.com')
        user2.set_password('password')
        db.session.add_all([user1, user2])
        db.session.commit()
        
        app1 = JobApplication(company='User1 Co', position='Dev', user_id=user1.id)
        app2 = JobApplication(company='User2 Co', position='Dev', user_id=user2.id)
        db.session.add_all([app1, app2])
        db.session.commit()
    
    # Login as user1
    auth.login('user1@test.com', 'password')
    
    response = client.get('/api/applications')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['total'] == 1
    assert data['applications'][0]['company'] == 'User1 Co'


def test_api_json_format(client, auth, user, application):
    """Test API returns properly formatted JSON."""
    auth.login()
    response = client.get('/api/applications')
    
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'applications' in data
    assert 'total' in data
    assert isinstance(data['applications'], list)
    
    if data['total'] > 0:
        app_data = data['applications'][0]
        assert 'id' in app_data
        assert 'company' in app_data
        assert 'position' in app_data
        assert 'status' in app_data
