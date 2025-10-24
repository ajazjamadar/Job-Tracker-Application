from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(256))  # Increased from 128 to 256 for scrypt hashes
    applications = db.relationship('JobApplication', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Applied')  # e.g., Applied, Interview, Offer, Rejected, Accepted
    date_applied = db.Column(db.Date, default=datetime.utcnow().date)
    follow_up_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Alias for compatibility
    @property
    def application_date(self):
        return self.date_applied
    
    @application_date.setter
    def application_date(self, value):
        self.date_applied = value

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'position': self.position,
            'status': self.status,
            'date_applied': self.date_applied.isoformat() if self.date_applied else None,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'notes': self.notes,
        }


# Helper functions for backwards compatibility with routes
# Alias JobApplication as Application for existing code
Application = JobApplication


def list_applications():
    """Get all job applications ordered by date."""
    return JobApplication.query.order_by(JobApplication.date_applied.desc()).all()


def get_application(app_id):
    """Get a single application by ID."""
    return JobApplication.query.get(app_id)


def create_application(company, role, status='Applied', notes=None):
    """Create a new job application."""
    app_obj = JobApplication(company=company, position=role, status=status, notes=notes)
    db.session.add(app_obj)
    db.session.commit()
    return app_obj
