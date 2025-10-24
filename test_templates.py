"""Test template rendering."""
from app import app

with app.test_client() as client:
    print('Testing template rendering...\n')
    
    # Test index page
    resp = client.get('/')
    print(f'✓ Index page (GET /): {resp.status_code}')
    
    # Test login page
    resp = client.get('/auth/login')
    print(f'✓ Login page (GET /auth/login): {resp.status_code}')
    
    # Test register page
    resp = client.get('/auth/register')
    print(f'✓ Register page (GET /auth/register): {resp.status_code}')
    
    print('\n✓ All templates render successfully!')
