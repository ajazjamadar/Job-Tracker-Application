"""
Pytest configuration and shared fixtures
"""
import pytest
from app import create_app, db
from app.models import User, JobApplication


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'SECRET_KEY': 'test-secret-key',
        'MAIL_SUPPRESS_SEND': True,  # Don't send real emails in tests
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Authentication helper fixture."""
    class AuthActions:
        def __init__(self, client):
            self._client = client
        
        def register(self, name='Test User', email='test@example.com', 
                     password='password123', password2=None):
            """Register a new user."""
            if password2 is None:
                password2 = password
            return self._client.post(
                '/auth/register',
                data={
                    'name': name,
                    'email': email,
                    'password': password,
                    'password2': password2
                },
                follow_redirects=True
            )
        
        def login(self, email='test@example.com', password='password123'):
            """Log in a user."""
            return self._client.post(
                '/auth/login',
                data={'email': email, 'password': password},
                follow_redirects=True
            )
        
        def logout(self):
            """Log out the current user."""
            return self._client.get('/auth/logout', follow_redirects=True)
    
    return AuthActions(client)


@pytest.fixture
def user(app):
    """Create a test user in the database."""
    user = User(name='Test User', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def application(app, user):
    """Create a test job application."""
    job_app = JobApplication(
        company='Test Company',
        position='Software Engineer',
        status='Applied',
        user_id=user.id
    )
    db.session.add(job_app)
    db.session.commit()
    return job_app
