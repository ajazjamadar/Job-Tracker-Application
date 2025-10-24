# Logging Configuration Documentation

## Overview
The Job Application Tracker includes comprehensive logging to track application behavior, user actions, and errors.

## Configuration

### Basic Setup
Logging is configured in two places:

1. **`config.py`** - Logging settings
2. **`app/__init__.py`** - Logger initialization

### Configuration Variables

In `config.py`:
```python
LOG_LEVEL = 'INFO'          # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FILE = 'app.log'        # Log file name
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

Environment variables:
```bash
# .env file
LOG_LEVEL=INFO
LOG_FILE=app.log
```

## Log Levels

### What Gets Logged Where

| Level | Console | File (logs/app.log) | When to Use |
|-------|---------|---------------------|-------------|
| DEBUG | ❌ | ❌ | Development debugging |
| INFO | ✅ | ❌ | General information |
| WARNING | ✅ | ✅ | Unexpected behavior |
| ERROR | ✅ | ✅ | Error conditions |
| CRITICAL | ✅ | ✅ | Critical failures |

**File Handler**: Only WARNING and above are written to `logs/app.log`
**Console**: INFO and above are displayed in the terminal

## Log Rotation

Logs automatically rotate when they reach 10MB:
- **Max file size**: 10MB
- **Backup files**: 10 (app.log.1, app.log.2, ..., app.log.10)
- **Location**: `logs/` directory

## What Gets Logged

### Authentication Events

**User Registration**:
```
INFO: New user registered: user@example.com
WARNING: Registration attempt with existing email: user@example.com
```

**User Login**:
```
INFO: User logged in: user@example.com
WARNING: Failed login attempt for email: user@example.com
```

**User Logout**:
```
INFO: User logged out: user@example.com
```

### Application Operations

**Create Application**:
```
INFO: User user@example.com created application for Google
INFO: API: User user@example.com created application 42 for Microsoft
```

**Update Application**:
```
INFO: User user@example.com updated application 15 for Amazon
INFO: Application 15 status changed: Applied -> Interview
```

**Delete Application**:
```
INFO: User user@example.com deleted application 23 for Facebook
```

### API Requests

**Validation Errors**:
```
WARNING: API: Missing company field in request from user user@example.com
WARNING: API: Missing position field in request from user user@example.com
```

**Successful Operations**:
```
INFO: API: User user@example.com created application 10 for Tesla
```

### System Events

**Application Startup**:
```
INFO: Application startup
```

## Accessing Logs

### View Recent Logs
```bash
# Windows PowerShell
Get-Content logs/app.log -Tail 50

# Linux/Mac
tail -f logs/app.log
```

### Search Logs
```bash
# Windows PowerShell
Select-String -Path logs/app.log -Pattern "ERROR"

# Linux/Mac
grep "ERROR" logs/app.log
```

### Filter by Date
```bash
# Windows PowerShell
Get-Content logs/app.log | Select-String "2025-10-24"

# Linux/Mac
grep "2025-10-24" logs/app.log
```

## Testing Logging

Run the test script:
```bash
python test_logging.py
```

Expected output:
```
INFO:app:Application startup
INFO:app:This is an INFO message (appears in console)
WARNING:app:This is a WARNING message (appears in file and console)
ERROR:app:This is an ERROR message (appears in file and console)
CRITICAL:app:This is a CRITICAL message (appears in file and console)
```

Check the log file:
```bash
cat logs/app.log
```

## Custom Logging in Code

### In Routes/Views
```python
from flask import current_app

@app.route('/example')
def example():
    current_app.logger.info('User accessed example page')
    current_app.logger.warning('Unusual activity detected')
    current_app.logger.error('Something went wrong')
    return 'OK'
```

### In Models
```python
from flask import current_app

class MyModel(db.Model):
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info(f'Saved {self.__class__.__name__}')
        except Exception as e:
            current_app.logger.error(f'Failed to save: {e}')
            db.session.rollback()
```

### In Background Tasks
```python
import logging

logger = logging.getLogger(__name__)

def background_task():
    logger.info('Task started')
    try:
        # Do work
        logger.info('Task completed')
    except Exception as e:
        logger.error(f'Task failed: {e}')
```

## Log Format

Default format:
```
2025-10-24 00:09:54,757 - app - WARNING - This is a warning message
```

Format breakdown:
- **Timestamp**: `2025-10-24 00:09:54,757`
- **Logger name**: `app`
- **Level**: `WARNING`
- **Message**: `This is a warning message`

### Custom Format

Modify in `config.py`:
```python
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
```

Available format variables:
- `%(asctime)s` - Timestamp
- `%(name)s` - Logger name
- `%(levelname)s` - Log level
- `%(message)s` - Log message
- `%(pathname)s` - Full file path
- `%(filename)s` - File name
- `%(funcName)s` - Function name
- `%(lineno)d` - Line number

## Production Considerations

### 1. Log Level
Set `LOG_LEVEL=WARNING` in production to reduce log volume:
```bash
# .env
LOG_LEVEL=WARNING
```

### 2. Log Aggregation
Consider using services like:
- **AWS CloudWatch**
- **Google Cloud Logging**
- **Papertrail**
- **Loggly**

### 3. Sensitive Data
Never log:
- Passwords
- API keys
- Personal information (emails should be masked)
- Credit card numbers

Example:
```python
# Bad
logger.info(f'User password: {password}')

# Good
logger.info(f'User authenticated: {email[:3]}***')
```

### 4. Performance
Logging can impact performance:
- Use appropriate log levels
- Avoid logging in tight loops
- Consider async logging for high-traffic apps

## Monitoring & Alerts

### Set Up Alerts
Monitor log files for critical errors:

**Linux cron example**:
```bash
# Check for errors every hour
0 * * * * grep "ERROR\|CRITICAL" /path/to/logs/app.log | mail -s "App Errors" admin@example.com
```

**Windows Task Scheduler** or use monitoring tools like:
- Sentry
- Rollbar
- New Relic

## Troubleshooting

### Logs Not Appearing

1. **Check log directory exists**:
```bash
ls logs/
```

2. **Check permissions**:
```bash
# Linux/Mac
chmod 755 logs/
```

3. **Check TESTING mode**:
Logs are disabled when `app.config['TESTING'] = True`

### Log File Growing Too Large

1. **Increase rotation count** in `app/__init__.py`:
```python
file_handler = RotatingFileHandler(
    f'logs/{log_file}',
    maxBytes=10485760,  # 10MB
    backupCount=20      # Keep more backups
)
```

2. **Use time-based rotation**:
```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    f'logs/{log_file}',
    when='midnight',
    interval=1,
    backupCount=30
)
```

## Best Practices

1. **Use appropriate levels**:
   - `DEBUG`: Detailed diagnostic info
   - `INFO`: General information
   - `WARNING`: Something unexpected
   - `ERROR`: Error occurred but app continues
   - `CRITICAL`: Serious error, app may stop

2. **Include context**:
```python
# Bad
logger.error('Failed')

# Good
logger.error(f'Failed to save application {app_id} for user {user.email}: {str(e)}')
```

3. **Don't log in loops** (performance):
```python
# Bad
for item in items:
    logger.info(f'Processing {item}')

# Good
logger.info(f'Processing {len(items)} items')
# ... process items ...
logger.info(f'Completed processing')
```

4. **Use structured logging** for better analysis:
```python
logger.info('user_action', extra={
    'user_id': user.id,
    'action': 'create_application',
    'company': company_name
})
```

## Summary

✅ **Automatic logging** for auth, CRUD, and API operations  
✅ **Log rotation** prevents disk space issues  
✅ **Configurable** via environment variables  
✅ **Test mode** disables file logging  
✅ **Production-ready** with proper levels and formatting  

Logs provide valuable insights into application behavior and help diagnose issues quickly!




