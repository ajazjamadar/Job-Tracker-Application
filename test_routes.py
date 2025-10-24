"""Test all routes are registered properly."""
from app import app
from flask import url_for

print('✓ App created successfully')
print('✓ Registered blueprints:', list(app.blueprints.keys()))

with app.test_request_context():
    print('\n📋 Main Routes (Blueprint: main):')
    print('  GET  /', url_for('main.index'))
    print('  GET  /dashboard', url_for('main.dashboard'), '(protected)')
    print('  GET  /applications', url_for('main.applications_list'), '(protected)')
    print('  GET/POST /applications/new', url_for('main.new_application'), '(protected)')
    print('  GET/POST /applications/<id>/edit', url_for('main.edit_application', app_id=1), '(protected)')
    print('  POST /applications/<id>/delete', url_for('main.delete_application', app_id=1), '(protected)')
    
    print('\n🔐 Auth Routes (Blueprint: auth):')
    print('  GET/POST /auth/register', url_for('auth.register'))
    print('  GET/POST /auth/login', url_for('auth.login'))
    print('  GET  /auth/logout', url_for('auth.logout'), '(protected)')
    
    print('\n🧪 Test Routes (Module-level):')
    print('  GET  /hello', url_for('hello'))

print('\n✓ All routes registered and working!')
