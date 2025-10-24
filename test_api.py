"""Test REST API endpoints"""
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as flask_app, db
from app.models import User, JobApplication
import json

def test_api():
    """Test API endpoints"""
    # Enable testing mode
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    with flask_app.app_context():
        # Create a test user
        test_user = User.query.filter_by(email='api_test@example.com').first()
        if not test_user:
            test_user = User(name='API Test User', email='api_test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print(f"✓ Created test user: {test_user.email}")
        else:
            print(f"✓ Using existing test user: {test_user.email}")
        
        # Create test client
        client = flask_app.test_client()
        
        # Login using the form
        login_response = client.post('/auth/login', data={
            'email': 'api_test@example.com',
            'password': 'password123'
        }, follow_redirects=False)
        
        print(f"✓ Login Status Code: {login_response.status_code}")
        
        # Test GET /api/applications
        print("\n--- Testing GET /api/applications ---")
        response = client.get('/api/applications')
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"✓ Retrieved {len(data)} applications")
            if data:
                print(f"  Sample application:")
                print(f"    - Company: {data[0].get('company')}")
                print(f"    - Position: {data[0].get('position')}")
                print(f"    - Status: {data[0].get('status')}")
        else:
            print(f"✗ GET request failed")
            print(f"  Response: {response.get_data(as_text=True)[:200]}")
        
        # Test POST /api/applications
        print("\n--- Testing POST /api/applications ---")
        new_app_data = {
            'company': 'Tech Corp API',
            'position': 'API Developer',
            'status': 'Applied'
        }
        response = client.post('/api/applications',
                              data=json.dumps(new_app_data),
                              content_type='application/json')
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            data = response.get_json()
            print(f"✓ Created application with ID: {data.get('id')}")
        else:
            print(f"✗ POST request failed")
            print(f"  Response: {response.get_data(as_text=True)[:200]}")
        
        # Test POST with missing company (should fail)
        print("\n--- Testing POST with missing 'company' field ---")
        invalid_data = {
            'position': 'Developer'
        }
        response = client.post('/api/applications',
                              data=json.dumps(invalid_data),
                              content_type='application/json')
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            data = response.get_json()
            print(f"✓ Validation error correctly returned: {data.get('error')}")
        else:
            print(f"✗ Expected 400 error but got {response.status_code}")
        
        # Verify data was created
        print("\n--- Verifying created data ---")
        response = client.get('/api/applications')
        if response.status_code == 200:
            data = response.get_json()
            api_apps = [a for a in data if 'API' in a.get('company', '')]
            print(f"✓ Found {len(api_apps)} API-related application(s)")
            for app in api_apps[:3]:  # Show up to 3 API apps
                print(f"  - {app.get('company')} - {app.get('position')}")
        
        print("\n" + "="*50)
        print("API ENDPOINTS SUMMARY:")
        print("="*50)
        print("GET  /api/applications  - List all applications")
        print("POST /api/applications  - Create new application")
        print("="*50)
        print("\n✓ API test completed!")

if __name__ == '__main__':
    test_api()
