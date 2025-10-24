"""
Test script to verify logging configuration
"""
from app import create_app
import logging

# Create app
app = create_app()

with app.app_context():
    # Test different log levels
    app.logger.debug('This is a DEBUG message (should not appear in file)')
    app.logger.info('This is an INFO message (appears in console)')
    app.logger.warning('This is a WARNING message (appears in file and console)')
    app.logger.error('This is an ERROR message (appears in file and console)')
    app.logger.critical('This is a CRITICAL message (appears in file and console)')
    
    print("\n" + "="*60)
    print("Logging test complete!")
    print("="*60)
    print("\nLog file location: logs/app.log")
    print("\nExpected behavior:")
    print("- INFO, WARNING, ERROR, CRITICAL → Console")
    print("- WARNING, ERROR, CRITICAL → File (logs/app.log)")
    print("- DEBUG → Neither (level too low)")
    print("\nCheck logs/app.log for WARNING and above messages")
    print("="*60)
