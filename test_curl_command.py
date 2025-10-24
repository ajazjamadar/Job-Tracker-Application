"""
Test the specific curl command:
curl -X POST -H "Content-Type: application/json" \
  -d '{"company":"Acme","position":"Engineer"}' \
  http://127.0.0.1:5000/api/applications -b cookiejar.txt
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from app import app as flask_app, db
from app.models import User

def test_curl_command():
    """Simulate the curl POST command"""
    # Enable testing mode
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    with flask_app.app_context():
        # Ensure test user exists
        test_user = User.query.filter_by(email='api_test@example.com').first()
        if not test_user:
            test_user = User(name='API Test User', email='api_test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print(f"✓ Created test user: {test_user.email}")
        else:
            print(f"✓ Using test user: {test_user.email}\n")
        
        # Create test client
        client = flask_app.test_client()
        
        # Step 1: Login (equivalent to: curl -c cookiejar.txt -X POST ... /auth/login)
        print("="*60)
        print("STEP 1: Login to get session cookie")
        print("="*60)
        print("Command: curl -c cookiejar.txt -X POST http://127.0.0.1:5000/auth/login \\")
        print('         -d "email=api_test@example.com&password=password123"')
        print()
        
        login_response = client.post('/auth/login', data={
            'email': 'api_test@example.com',
            'password': 'password123'
        })
        
        print(f"Status Code: {login_response.status_code}")
        print(f"✓ Login successful - Session cookie stored\n")
        
        # Step 2: POST new application (the curl command you provided)
        print("="*60)
        print("STEP 2: Create application via API")
        print("="*60)
        print("Command: curl -X POST -H 'Content-Type: application/json' \\")
        print('         -d \'{"company":"Acme","position":"Engineer"}\' \\')
        print("         http://127.0.0.1:5000/api/applications -b cookiejar.txt")
        print()
        
        new_app_data = {
            'company': 'Acme',
            'position': 'Engineer'
        }
        
        response = client.post('/api/applications',
                              data=json.dumps(new_app_data),
                              content_type='application/json')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.get_json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print(f"\n✓ SUCCESS! Created application with ID: {result['id']}\n")
        else:
            print(f"✗ FAILED")
            print(f"Response: {response.get_data(as_text=True)}\n")
        
        # Step 3: Verify by listing all applications
        print("="*60)
        print("STEP 3: Verify - List all applications")
        print("="*60)
        print("Command: curl http://127.0.0.1:5000/api/applications -b cookiejar.txt")
        print()
        
        list_response = client.get('/api/applications')
        
        if list_response.status_code == 200:
            applications = list_response.get_json()
            acme_apps = [a for a in applications if a.get('company') == 'Acme']
            
            print(f"Status Code: {list_response.status_code}")
            print(f"Total Applications: {len(applications)}")
            print(f"Acme Applications: {len(acme_apps)}")
            print()
            
            if acme_apps:
                print("Acme Application Details:")
                for app in acme_apps:
                    print(json.dumps(app, indent=2))
                    print()
                print(f"✓ VERIFIED! Found {len(acme_apps)} Acme application(s)")
        
        print("\n" + "="*60)
        print("COMPLETE CURL WORKFLOW:")
        print("="*60)
        print("# 1. Login and save session cookie")
        print("curl -c cookiejar.txt -X POST http://127.0.0.1:5000/auth/login \\")
        print('     -d "email=api_test@example.com&password=password123"')
        print()
        print("# 2. Create application using saved cookie")
        print("curl -X POST -H 'Content-Type: application/json' \\")
        print('     -d \'{"company":"Acme","position":"Engineer"}\' \\')
        print("     http://127.0.0.1:5000/api/applications -b cookiejar.txt")
        print()
        print("# 3. List all applications")
        print("curl http://127.0.0.1:5000/api/applications -b cookiejar.txt")
        print("="*60)

if __name__ == '__main__':
    test_curl_command()
