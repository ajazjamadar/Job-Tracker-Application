# Email Notifications Setup Guide

## Overview

The Job Application Tracker includes email notification functionality powered by Flask-Mail. This allows the application to send automated emails for:

- **Welcome emails** when users register
- **Follow-up reminders** for job applications
- **Status change notifications** when application status is updated

## Configuration

### 1. Environment Variables

Email notifications require the following environment variables to be set. Copy `.env.example` to `.env` and update the values:

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 2. Gmail Setup (Recommended for Development)

If using Gmail, you **must** use an App Password (not your regular password):

#### Steps:
1. **Enable 2-Factor Authentication** on your Google account
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate an App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Job Tracker" as the name
   - Click "Generate"
   - Copy the 16-character password

3. **Update .env file**
   ```bash
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

### 3. Alternative Email Providers

#### Outlook/Office365
```bash
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

#### Yahoo Mail
```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
```

#### SendGrid (Production Recommended)
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=your-verified-sender@yourdomain.com
```

## Available Email Functions

### 1. Welcome Email
Sent when a user registers for an account.

```python
from app.email import send_welcome_email

# After user registration
send_welcome_email(user)
```

**Email includes:**
- Welcome message
- Feature overview
- Getting started instructions

### 2. Application Reminder
Sent to remind users to follow up on applications.

```python
from app.email import send_application_reminder

# Send reminder for specific application
send_application_reminder(user, application)
```

**Email includes:**
- Company name and position
- Application status
- Date applied and follow-up date
- Application notes

### 3. Status Change Notification
Sent when application status is updated.

```python
from app.email import send_status_change_notification

# Notify user of status change
old_status = "Applied"
new_status = "Interview"
send_status_change_notification(user, application, old_status, new_status)
```

**Email includes:**
- Company and position details
- Old and new status (color-coded)
- Encouragement message

## Integration Examples

### Example 1: Send Welcome Email on Registration

Update `app/auth.py`:

```python
from .email import send_welcome_email

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        send_welcome_email(user)
        
        flash('Account created! Check your email.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)
```

### Example 2: Send Notification on Status Change

Update `app/routes.py`:

```python
from .email import send_status_change_notification

@main_bp.route('/applications/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    app_obj = JobApplication.query.filter_by(id=app_id, user_id=current_user.id).first_or_404()
    
    # Store old status
    old_status = app_obj.status
    
    form = ApplicationForm(obj=app_obj)
    if form.validate_on_submit():
        form.populate_obj(app_obj)
        db.session.commit()
        
        # Send notification if status changed
        if old_status != app_obj.status:
            send_status_change_notification(
                current_user, 
                app_obj, 
                old_status, 
                app_obj.status
            )
        
        flash('Application updated!', 'success')
        return redirect(url_for('main.applications_list'))
    
    return render_template('applications/edit.html', form=form, application=app_obj)
```

### Example 3: Scheduled Reminders (Advanced)

For scheduled reminders, you would need a background task scheduler like Celery or APScheduler:

```python
from datetime import date
from app import app, db
from app.models import JobApplication, User
from app.email import send_application_reminder

def send_daily_reminders():
    """Check for applications needing follow-up and send reminders"""
    with app.app_context():
        today = date.today()
        
        # Find applications with follow-up date = today
        applications = JobApplication.query.filter(
            JobApplication.follow_up_date == today,
            JobApplication.status.in_(['Applied', 'Interview'])
        ).all()
        
        for app in applications:
            user = User.query.get(app.user_id)
            if user:
                send_application_reminder(user, app)
                print(f"Sent reminder to {user.email} for {app.company}")
```

## Email Templates

All emails include both **plain text** and **HTML** versions for maximum compatibility.

### HTML Email Features:
- ✓ Professional styling
- ✓ Color-coded status badges
- ✓ Responsive design
- ✓ Brand colors (#0d6efd - Bootstrap primary)

### Plain Text Fallback:
- ✓ Clean formatting
- ✓ All information included
- ✓ Works with any email client

## Testing Email Configuration

Run the test script to verify your email setup:

```bash
python test_email_config.py
```

This will:
- Display current configuration
- Verify credentials are set
- List available email functions
- Provide usage examples

## Asynchronous Sending

All emails are sent **asynchronously** using Python threads to prevent blocking the main application. This ensures:

- ✓ Fast response times for users
- ✓ No delays during registration or updates
- ✓ Better user experience

## Security Best Practices

1. **Never commit credentials** - Use `.env` file (already in `.gitignore`)
2. **Use App Passwords** - Don't use your main email password
3. **Limit sending rate** - Respect email provider limits (Gmail: 500/day for free accounts)
4. **Verify sender domain** - For production, use a custom domain with SPF/DKIM
5. **Monitor for bounces** - Check for failed deliveries regularly

## Production Recommendations

For production deployments:

1. **Use a dedicated email service:**
   - SendGrid (99% deliverability)
   - Mailgun (good for developers)
   - Amazon SES (cost-effective)
   - Postmark (transactional emails)

2. **Set up proper DNS records:**
   - SPF record
   - DKIM signature
   - DMARC policy

3. **Implement rate limiting:**
   - Queue emails
   - Batch processing
   - Monitor sending volume

4. **Add email preferences:**
   - Allow users to opt-out
   - Email frequency settings
   - Notification preferences

## Troubleshooting

### Emails not sending?

1. **Check credentials:**
   ```bash
   python test_email_config.py
   ```

2. **Verify environment variables are loaded:**
   ```python
   from app import app
   print(app.config.get('MAIL_USERNAME'))
   ```

3. **Check for errors in console:**
   - Email errors are printed to stdout
   - Look for authentication failures

4. **Gmail "Less secure app" blocked:**
   - Use App Password instead
   - Don't disable "Less secure apps" (deprecated)

### Emails going to spam?

1. Use a verified sender domain
2. Set up SPF/DKIM records
3. Avoid spam trigger words
4. Include unsubscribe link
5. Maintain good sender reputation

## Configuration Summary

| Setting | Description | Default | Required |
|---------|-------------|---------|----------|
| `MAIL_SERVER` | SMTP server hostname | smtp.gmail.com | Yes |
| `MAIL_PORT` | SMTP server port | 587 | Yes |
| `MAIL_USE_TLS` | Enable TLS encryption | True | Yes |
| `MAIL_USERNAME` | Email account username | None | Yes |
| `MAIL_PASSWORD` | Email account password/app password | None | Yes |
| `MAIL_DEFAULT_SENDER` | Default "From" address | None | Yes |

## Next Steps

1. ✅ Configuration added to `config.py`
2. ✅ Flask-Mail initialized in `app/__init__.py`
3. ✅ Email functions created in `app/email.py`
4. ✅ Example `.env` file provided
5. ⏭️ Set up your email credentials
6. ⏭️ Integrate email functions into your routes
7. ⏭️ Test with real email addresses
8. ⏭️ Set up scheduled reminders (optional)

Happy emailing! 📧




