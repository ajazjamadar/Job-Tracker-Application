# Test Suite Documentation

## Overview
This test suite uses **pytest** to test the Job Application Tracker application.

## Test Structure

```
tests/
├── __init__.py              # Package marker
├── conftest.py              # Shared fixtures and configuration
├── test_auth.py             # Authentication tests
├── test_models.py           # Database model tests
├── test_routes.py           # Route/view tests
├── test_api.py              # API endpoint tests
├── test_email.py            # Email functionality tests
└── README.md                # This file
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_auth.py
```

### Run specific test function
```bash
pytest tests/test_auth.py::test_register_success
```

### Run with verbose output
```bash
pytest -v
```

### Run with coverage report
```bash
pytest --cov=app --cov-report=html
```

### Run tests by marker
```bash
# Run only auth tests
pytest -m auth

# Run only API tests
pytest -m api

# Skip slow tests
pytest -m "not slow"
```

## Fixtures

### `app`
Creates a test Flask application with in-memory SQLite database.

**Usage:**
```python
def test_something(app):
    with app.app_context():
        # Your test code
```

### `client`
Flask test client for making HTTP requests.

**Usage:**
```python
def test_route(client):
    response = client.get('/some-route')
    assert response.status_code == 200
```

### `auth`
Authentication helper with methods:
- `auth.register(name, email, password, password2)`
- `auth.login(email, password)`
- `auth.logout()`

**Usage:**
```python
def test_protected_route(client, auth):
    auth.login()
    response = client.get('/dashboard')
    assert response.status_code == 200
```

### `user`
Pre-created test user in the database.

**Usage:**
```python
def test_user_feature(user):
    assert user.email == 'test@example.com'
```

### `application`
Pre-created test job application.

**Usage:**
```python
def test_edit_application(client, auth, application):
    auth.login()
    response = client.get(f'/applications/{application.id}/edit')
```

## Test Coverage

### Authentication (`test_auth.py`)
- ✓ User registration (success, duplicate email, password mismatch)
- ✓ User login (success, invalid credentials)
- ✓ User logout
- ✓ Password hashing

### Models (`test_models.py`)
- ✓ User model creation
- ✓ Password hashing and verification
- ✓ JobApplication model creation
- ✓ User-Application relationship
- ✓ Default values
- ✓ Cascade delete

### Routes (`test_routes.py`)
- ✓ Public pages (index)
- ✓ Protected routes (dashboard, applications)
- ✓ CRUD operations (create, read, update, delete)
- ✓ User isolation
- ✓ Search functionality
- ✓ Pagination

### API (`test_api.py`)
- ✓ GET /api/applications (authorized/unauthorized)
- ✓ POST /api/applications (success, validation, authorization)
- ✓ User isolation
- ✓ JSON format validation

### Email (`test_email.py`)
- ✓ Welcome email
- ✓ Application reminder
- ✓ Status change notification
- ✓ Error handling

## Configuration

### `pytest.ini`
Main pytest configuration file with:
- Test discovery patterns
- Coverage settings
- Custom markers
- Logging configuration

### `conftest.py`
Shared fixtures and test configuration:
- Test database setup (in-memory SQLite)
- CSRF disabled for testing
- Email suppression
- Authentication helpers

## Best Practices

1. **Use fixtures** for common setup (users, applications, authentication)
2. **Test isolation**: Each test should be independent
3. **Test both success and failure** cases
4. **Use descriptive test names**: `test_feature_scenario`
5. **Assert specific behaviors**, not just status codes
6. **Clean up after tests**: Fixtures handle this automatically

## Example Test

```python
def test_create_application(client, auth, user, app):
    """Test creating a new job application."""
    # Arrange: Login
    auth.login()
    
    # Act: Submit form
    response = client.post(
        '/applications/new',
        data={
            'company': 'Google',
            'position': 'Engineer',
            'status': 'Applied'
        },
        follow_redirects=True
    )
    
    # Assert: Verify creation
    assert response.status_code == 200
    
    with app.app_context():
        from app.models import JobApplication
        app_obj = JobApplication.query.filter_by(company='Google').first()
        assert app_obj is not None
        assert app_obj.user_id == user.id
```

## Continuous Integration

Tests can be integrated with CI/CD pipelines:

### GitHub Actions
```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app
```

## Troubleshooting

### Import errors
Make sure you're running from the project root:
```bash
cd job-tracker
pytest
```

### Database errors
Tests use in-memory SQLite. No setup needed.

### CSRF errors
CSRF is disabled in test config (`WTF_CSRF_ENABLED = False`).

### Email errors
Emails are suppressed in tests (`MAIL_SUPPRESS_SEND = True`).




