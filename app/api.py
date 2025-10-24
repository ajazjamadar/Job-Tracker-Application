from flask import Blueprint, jsonify, request, abort, current_app
from .models import JobApplication
from . import db
from flask_login import login_required, current_user

api_bp = Blueprint('api', __name__)

@api_bp.route('/applications', methods=['GET'])
@login_required
def api_list_applications():
    """Get all applications for the current user."""
    apps = JobApplication.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'applications': [a.to_dict() for a in apps],
        'total': len(apps)
    })

@api_bp.route('/applications', methods=['POST'])
@login_required
def api_create_application():
    """Create a new application."""
    data = request.get_json() or {}
    
    # Validate required fields
    if 'company' not in data:
        current_app.logger.warning(f'API: Missing company field in request from user {current_user.email}')
        return jsonify({'error': 'company required'}), 400
    if 'position' not in data:
        current_app.logger.warning(f'API: Missing position field in request from user {current_user.email}')
        return jsonify({'error': 'position required'}), 400
    
    # Create application
    app_obj = JobApplication(
        company=data['company'],
        position=data['position'],
        status=data.get('status', 'Applied'),
        notes=data.get('notes'),
        user_id=current_user.id
    )
    db.session.add(app_obj)
    db.session.commit()
    
    current_app.logger.info(f'API: User {current_user.email} created application {app_obj.id} for {app_obj.company}')
    return jsonify(app_obj.to_dict()), 201
