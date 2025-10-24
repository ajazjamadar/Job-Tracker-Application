import os
import logging


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    
    # Database Configuration
    # Option 1: Use Railway's pre-built MYSQL_URL (recommended)
    if os.environ.get('MYSQL_URL'):
        # Railway provides: mysql://user:password@host:3306/database
        # Convert to SQLAlchemy format: mysql+mysqlconnector://
        SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URL').replace('mysql://', 'mysql+mysqlconnector://')
    
    # Option 2: Build from individual Railway variables
    elif all([
        os.environ.get('MYSQLUSER'),
        os.environ.get('MYSQLPASSWORD'),
        os.environ.get('MYSQLHOST'),
        os.environ.get('MYSQLDATABASE')
    ]):
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{os.environ.get('MYSQLUSER')}:"
            f"{os.environ.get('MYSQLPASSWORD')}@"
            f"{os.environ.get('MYSQLHOST')}:"
            f"{os.environ.get('MYSQLPORT', '3306')}/"
            f"{os.environ.get('MYSQLDATABASE')}"
        )
    
    # Option 3: Manual override or local development
    else:
        # Default to SQLite for local development
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
