"""Test auth blueprint registration."""
from app import app
from flask import url_for

print('✓ App created successfully')
print('✓ Registered blueprints:', list(app.blueprints.keys()))

with app.test_request_context():
    print('\n✓ Auth routes:')
    print('  - Register:', url_for('auth.register'))
    print('  - Login:', url_for('auth.login'))
    print('  - Logout:', url_for('auth.logout'))
    
print('\n✓ All auth routes working!')
