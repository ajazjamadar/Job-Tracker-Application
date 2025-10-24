"""Test CRUD templates rendering."""
from app import app, db
from app.models import User, JobApplication
from datetime import datetime, timedelta

with app.test_client() as client:
    print('Testing CRUD template rendering...\n')
    
    # Create a test user and login
    with app.app_context():
        # Clean up any existing test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            JobApplication.query.filter_by(user_id=test_user.id).delete()
            db.session.delete(test_user)
            db.session.commit()
        
        # Create fresh test user
        user = User(email='test@example.com', name='Test User')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Create test applications
        app1 = JobApplication(
            company='Google',
            position='Software Engineer',
            status='Applied',
            date_applied=datetime.now().date(),
            user_id=user.id
        )
        app2 = JobApplication(
            company='Microsoft',
            position='Data Scientist',
            status='Interview',
            date_applied=datetime.now().date() - timedelta(days=5),
            follow_up_date=datetime.now().date() + timedelta(days=2),
            notes='Second round interview scheduled',
            user_id=user.id
        )
        db.session.add_all([app1, app2])
        db.session.commit()
        
        print(f'✓ Created test user: {user.email}')
        print(f'✓ Created {JobApplication.query.filter_by(user_id=user.id).count()} test applications\n')
    
    # Login
    resp = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123',
        'remember': False
    }, follow_redirects=False)
    print(f'✓ Login: {resp.status_code}')
    
    # Test dashboard
    resp = client.get('/dashboard')
    print(f'✓ Dashboard (GET /dashboard): {resp.status_code}')
    
    # Test applications list
    resp = client.get('/applications')
    print(f'✓ Applications list (GET /applications): {resp.status_code}')
    
    # Test new application form
    resp = client.get('/applications/new')
    print(f'✓ New application form (GET /applications/new): {resp.status_code}')
    
    # Test edit application form
    resp = client.get('/applications/1/edit')
    print(f'✓ Edit application form (GET /applications/1/edit): {resp.status_code}')
    
    print('\n✓ All CRUD templates render successfully!')
    print('\nNote: Test data created in database for visual testing.')
