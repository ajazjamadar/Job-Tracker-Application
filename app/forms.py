from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):
    """User registration form."""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ApplicationForm(FlaskForm):
    """Job application form matching the JobApplication model."""
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position/Role', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
        ('Withdrawn', 'Withdrawn')
    ], default='Applied')
    date_applied = DateField('Date Applied', validators=[Optional()], format='%Y-%m-%d')
    follow_up_date = DateField('Follow-up Date', validators=[Optional()], format='%Y-%m-%d')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save')
