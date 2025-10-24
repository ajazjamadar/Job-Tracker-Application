"""
Authentication tests
"""
import pytest
from app import db
from app.models import User


def test_register_success(client, app):
    """Test successful user registration."""
    response = client.post(
        '/auth/register',
        data={
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'securepassword',
            'password2': 'securepassword'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    
    # Verify user was created in database
    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.name == 'New User'


def test_register_duplicate_email(client, user):
    """Test registration with duplicate email fails."""
    response = client.post(
        '/auth/register',
        data={
            'name': 'Another User',
            'email': 'test@example.com',  # Already exists
            'password': 'password123',
            'password2': 'password123'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Email already registered' in response.data or b'already' in response.data.lower()


def test_register_password_mismatch(client):
    """Test registration with mismatched passwords fails."""
    response = client.post(
        '/auth/register',
        data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'different'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Field must be equal to password' in response.data or b'match' in response.data.lower()


def test_login_success(auth, user):
    """Test successful login."""
    response = auth.login('test@example.com', 'password123')
    assert response.status_code == 200
    # Should redirect to dashboard after login
    assert b'Dashboard' in response.data or b'Applications' in response.data


def test_login_invalid_email(auth):
    """Test login with non-existent email."""
    response = auth.login('nonexistent@example.com', 'password123')
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data or b'Invalid' in response.data


def test_login_invalid_password(auth, user):
    """Test login with wrong password."""
    response = auth.login('test@example.com', 'wrongpassword')
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data or b'Invalid' in response.data


def test_logout(auth, user, client):
    """Test logout functionality."""
    auth.login()
    response = auth.logout()
    assert response.status_code == 200
    # After logout, accessing protected routes should redirect
    response = client.get('/dashboard')
    assert response.status_code in (302, 401)


def test_register_login_flow(client, app):
    """Test complete registration and login flow."""
    # Register
    client.post(
        '/auth/register',
        data={
            'name': 'Flow Test',
            'email': 'flow@example.com',
            'password': 'secret123',
            'password2': 'secret123'
        }
    )
    
    # Login
    rv = client.post(
        '/auth/login',
        data={'email': 'flow@example.com', 'password': 'secret123'},
        follow_redirects=True
    )
    
    assert rv.status_code in (302, 200)
    assert b'Dashboard' in rv.data or b'Applications' in rv.data


def test_password_hashing(app, user):
    """Test that passwords are properly hashed."""
    assert user.password_hash is not None
    assert user.password_hash != 'password123'
    assert user.check_password('password123') is True
    assert user.check_password('wrongpassword') is False
