from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(config_class='config.Config'):
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    
    # Configure logging
    configure_logging(app)
    
    # Import models first (needed by other modules)
    from . import models
    
    # Register blueprints
    from .auth import auth_bp
    from .routes import main_bp
    from .api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


def configure_logging(app):
    """Configure logging for the application."""
    # Set basic logging configuration
    logging.basicConfig(level=logging.INFO)
    
    # Don't configure file handler in testing mode
    if app.config.get('TESTING'):
        return
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # File handler for WARNING and above
    log_file = app.config.get('LOG_FILE', 'app.log')
    file_handler = RotatingFileHandler(
        f'logs/{log_file}',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.WARNING)
    
    # Set log format
    log_format = logging.Formatter(
        app.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    file_handler.setFormatter(log_format)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    
    # Set app logger level based on config
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level))
    
    # Log startup message
    app.logger.info('Application startup')


# Module-level app for backwards compatibility (used by wsgi.py and development)
app = create_app()

