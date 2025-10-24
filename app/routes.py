from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from . import db
from .models import JobApplication, User
from .forms import ApplicationForm

# Create main blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Public landing page."""
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Protected dashboard showing user's applications."""
    # Get applications for current user
    applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(
        JobApplication.date_applied.desc()
    ).limit(5).all()
    
    # Calculate stats
    total_apps = JobApplication.query.filter_by(user_id=current_user.id).count()
    pending_apps = JobApplication.query.filter_by(user_id=current_user.id, status='Applied').count()
    interview_apps = JobApplication.query.filter_by(user_id=current_user.id, status='Interview').count()
    
    return render_template('dashboard.html', 
                         applications=applications,
                         total_apps=total_apps,
                         pending_apps=pending_apps,
                         interview_apps=interview_apps)


@main_bp.route('/applications')
@login_required
def applications_list():
    """List all applications for current user with pagination and search."""
    # Get page number from query string (default to 1)
    page = request.args.get('page', 1, type=int)
    
    # Get search parameters
    q_company = request.args.get('company', '').strip()
    q_status = request.args.get('status', '').strip()
    
    # Base query filtered by current user
    query = JobApplication.query.filter_by(user_id=current_user.id)
    
    # Apply company search filter if provided
    if q_company:
        query = query.filter(JobApplication.company.ilike(f'%{q_company}%'))
    
    # Apply status filter if provided
    if q_status:
        query = query.filter(JobApplication.status == q_status)
    
    # Paginate results (10 per page) ordered by date applied descending
    pagination = query.order_by(JobApplication.date_applied.desc()).paginate(
        page=page, 
        per_page=10, 
        error_out=False
    )
    
    return render_template('applications/list.html', 
                         pagination=pagination, 
                         q_company=q_company,
                         q_status=q_status)


@main_bp.route('/applications/new', methods=['GET', 'POST'])
@login_required
def new_application():
    """Create a new job application."""
    form = ApplicationForm()
    if form.validate_on_submit():
        app_obj = JobApplication(
            company=form.company.data,
            position=form.position.data,
            status=form.status.data,
            date_applied=form.date_applied.data,
            follow_up_date=form.follow_up_date.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(app_obj)
        db.session.commit()
        
        current_app.logger.info(f'User {current_user.email} created application for {app_obj.company}')
        flash('Application added successfully!', 'success')
        return redirect(url_for('main.applications_list'))
    return render_template('applications/edit.html', form=form, application=None)


@main_bp.route('/applications/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    """Edit an existing job application."""
    app_obj = JobApplication.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()
    
    form = ApplicationForm(obj=app_obj)
    if form.validate_on_submit():
        old_status = app_obj.status
        form.populate_obj(app_obj)
        db.session.commit()
        
        current_app.logger.info(f'User {current_user.email} updated application {app_id} for {app_obj.company}')
        if old_status != app_obj.status:
            current_app.logger.info(f'Application {app_id} status changed: {old_status} -> {app_obj.status}')
        
        flash('Application updated successfully!', 'success')
        return redirect(url_for('main.applications_list'))
    
    return render_template('applications/edit.html', form=form, application=app_obj)


@main_bp.route('/applications/<int:app_id>/delete', methods=['POST'])
@login_required
def delete_application(app_id):
    """Delete a job application."""
    app_obj = JobApplication.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()
    company_name = app_obj.company
    db.session.delete(app_obj)
    db.session.commit()
    
    current_app.logger.info(f'User {current_user.email} deleted application {app_id} for {company_name}')
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('main.applications_list'))
