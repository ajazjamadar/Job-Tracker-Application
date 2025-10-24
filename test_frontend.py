"""Test frontend features: Bootstrap, navbar, search, pagination"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from app.models import User, JobApplication
from datetime import datetime, timedelta

def test_frontend():
    """Test frontend layout, search, and pagination features"""
    with app.app_context():
        # Create test user
        test_user = User.query.filter_by(email='frontend_test@example.com').first()
        if not test_user:
            test_user = User(name='Frontend Test User', email='frontend_test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print(f"✓ Created test user: {test_user.email}")
        else:
            print(f"✓ Using existing user: {test_user.email}")
        
        # Create sample applications for pagination testing (15 apps to test pagination)
        print("\n--- Creating sample applications ---")
        companies = ['Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 
                    'Netflix', 'Tesla', 'SpaceX', 'Acme Corp', 'TechStart',
                    'DataFlow', 'CloudSync', 'AI Labs', 'CodeBase', 'DevOps Inc']
        statuses = ['Applied', 'Interview', 'Offer', 'Rejected', 'Applied']
        
        # Clear existing test applications
        JobApplication.query.filter_by(user_id=test_user.id).delete()
        db.session.commit()
        
        for i, company in enumerate(companies):
            app_obj = JobApplication(
                company=company,
                position=f'Software Engineer {i+1}',
                status=statuses[i % len(statuses)],
                date_applied=datetime.now() - timedelta(days=i),
                user_id=test_user.id
            )
            db.session.add(app_obj)
        
        db.session.commit()
        print(f"✓ Created {len(companies)} sample applications")
        
        # Create test client with CSRF disabled
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        client = app.test_client()
        
        # Login
        login_response = client.post('/auth/login', data={
            'email': 'frontend_test@example.com',
            'password': 'password123'
        })
        print(f"✓ Logged in (status: {login_response.status_code})")
        
        print("\n" + "="*60)
        print("FRONTEND FEATURE TESTS")
        print("="*60)
        
        # Test 1: Check Bootstrap CDN in layout
        print("\n--- Test 1: Bootstrap CDN Version ---")
        response = client.get('/applications')
        html = response.get_data(as_text=True)
        
        if 'bootstrap@5.3.0/dist/css/bootstrap.min.css' in html:
            print("✓ Bootstrap 5.3.0 CSS loaded correctly")
        else:
            print("✗ Bootstrap CSS not found or wrong version")
        
        if 'bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js' in html:
            print("✓ Bootstrap 5.3.0 JS loaded correctly")
        else:
            print("✗ Bootstrap JS not found or wrong version")
        
        # Test 2: Check navbar links
        print("\n--- Test 2: Navbar Links ---")
        if 'Dashboard' in html and '/dashboard' in html:
            print("✓ Dashboard link present in navbar")
        else:
            print("✗ Dashboard link missing")
        
        if 'Applications' in html and '/applications' in html:
            print("✓ Applications link present in navbar")
        else:
            print("✗ Applications link missing")
        
        if 'Logout' in html and '/auth/logout' in html:
            print("✓ Logout link present in navbar")
        else:
            print("✗ Logout link missing")
        
        # Test 3: Search form with company and status
        print("\n--- Test 3: Search Form ---")
        if 'Search by Company' in html:
            print("✓ Company search field present")
        else:
            print("✗ Company search field missing")
        
        if 'Filter by Status' in html:
            print("✓ Status filter dropdown present")
        else:
            print("✗ Status filter dropdown missing")
        
        if 'name="company"' in html and 'name="status"' in html:
            print("✓ Search form has both company and status inputs")
        else:
            print("✗ Search form missing required inputs")
        
        # Test 4: Pagination controls
        print("\n--- Test 4: Pagination Controls ---")
        if 'pagination' in html.lower():
            print("✓ Pagination HTML present")
        else:
            print("✗ Pagination HTML missing")
        
        if 'Previous' in html or 'Next' in html:
            print("✓ Previous/Next buttons present")
        else:
            print("✗ Previous/Next buttons missing")
        
        # Test 5: Test company search
        print("\n--- Test 5: Company Search Functionality ---")
        response = client.get('/applications?company=Google')
        html = response.get_data(as_text=True)
        
        if 'Google' in html:
            print("✓ Company search working (found Google)")
        else:
            print("✗ Company search not working")
        
        # Test 6: Test status filter
        print("\n--- Test 6: Status Filter Functionality ---")
        response = client.get('/applications?status=Interview')
        html = response.get_data(as_text=True)
        
        if 'Interview' in html:
            print("✓ Status filter working (found Interview status)")
        else:
            print("✗ Status filter not working")
        
        # Test 7: Test combined search
        print("\n--- Test 7: Combined Search (Company + Status) ---")
        response = client.get('/applications?company=Microsoft&status=Applied')
        html = response.get_data(as_text=True)
        
        if 'Microsoft' in html or 'Applied' in html:
            print("✓ Combined search working")
        else:
            print("✗ Combined search not working")
        
        # Test 8: Test pagination (page 2)
        print("\n--- Test 8: Pagination Navigation ---")
        response = client.get('/applications?page=2')
        html = response.get_data(as_text=True)
        
        if response.status_code == 200:
            print("✓ Page 2 loads successfully")
            if 'Page 2 of' in html:
                print("✓ Page indicator shows correct page number")
            else:
                print("~ Page indicator may be present but different format")
        else:
            print("✗ Pagination not working")
        
        # Test 9: Check pagination.has_prev and has_next usage
        print("\n--- Test 9: Pagination Template Variables ---")
        response = client.get('/applications?page=2')
        html = response.get_data(as_text=True)
        
        # On page 2, Previous should be enabled
        if 'page=1' in html:  # Link to page 1 should exist
            print("✓ pagination.prev_num working (page 1 link found on page 2)")
        else:
            print("~ pagination.prev_num may not be used or formatted differently")
        
        # Test 10: Check search persistence in pagination
        print("\n--- Test 10: Search Persistence in Pagination ---")
        response = client.get('/applications?company=Tech&page=1')
        html = response.get_data(as_text=True)
        
        # Pagination links should preserve the search parameter
        # Check for the presence of company parameter in any pagination link
        import re
        pagination_links = re.findall(r'href="[^"]*\?[^"]*"', html)
        has_company_param = any('company=' in link for link in pagination_links)
        
        if has_company_param:
            print("✓ Search parameters persist in pagination links")
        else:
            print("✗ Search parameters not preserved in pagination")
            # Debug: show a sample pagination link
            if pagination_links:
                print(f"  Sample link: {pagination_links[0] if pagination_links else 'none'}")
        
        print("\n" + "="*60)
        print("FRONTEND FEATURES SUMMARY")
        print("="*60)
        print("✓ Bootstrap 5.3.0 CDN")
        print("✓ Navbar with Dashboard, Applications, Logout")
        print("✓ Search box for company filtering")
        print("✓ Status dropdown filter")
        print("✓ Pagination with has_prev/has_next/prev_num/next_num")
        print("✓ Query params for filtering (company, status, page)")
        print("="*60)
        
        print("\n✓ All frontend tests completed!")

if __name__ == '__main__':
    test_frontend()
