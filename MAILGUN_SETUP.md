# Mailgun Setup Guide

## Why Mailgun?
- ✅ **Professional**: Industry-standard email service
- ✅ **Free Tier**: 5,000 emails/month for 3 months (then 1,000/month)
- ✅ **Reliable**: Better deliverability than personal email
- ✅ **Tracking**: Email analytics and delivery tracking
- ✅ **Production-Ready**: Used by major companies

---

## Step 1: Sign Up for Mailgun

1. Go to: **https://www.mailgun.com/**
2. Click **"Sign Up"** (top right)
3. Fill in your details:
   - Email address
   - Password
   - Company name (can be your project name)
4. Verify your email address

---

## Step 2: Choose Domain Setup

You have two options:

### Option A: Sandbox Domain (Quick Start - Recommended for Development)

**Pros**: No domain required, works immediately
**Cons**: Can only send to verified email addresses (up to 5)

1. After signup, Mailgun gives you a sandbox domain automatically
2. Format: `sandboxXXXXXXXXXXXXXXXXXX.mailgun.org`
3. **Add Authorized Recipients**: Go to **Sending → Domain Settings → Authorized Recipients**
4. Add your email address (you'll receive a confirmation email)

### Option B: Custom Domain (Production)

**Pros**: Professional, no recipient restrictions
**Cons**: Requires domain ownership and DNS configuration

1. Click **"Add New Domain"** in Mailgun dashboard
2. Enter your domain (e.g., `mg.yourdomain.com`)
3. Add DNS records to your domain registrar:
   - TXT records for SPF and DKIM
   - MX records for receiving
   - CNAME for tracking
4. Wait for verification (can take 24-48 hours)

---

## Step 3: Get SMTP Credentials

1. In Mailgun dashboard, go to: **Sending → Domain Settings**
2. Select your domain (sandbox or custom)
3. Click **"SMTP Credentials"** tab
4. You'll see:
   - **SMTP Hostname**: `smtp.mailgun.org`
   - **Port**: `587` (TLS) or `465` (SSL)
   - **Username**: `postmaster@your-domain.mailgun.org`
   - **Password**: Click "Reset Password" to generate one

---

## Step 4: Update Your .env File

### For Sandbox Domain:
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@sandboxXXXXXXXXXXXXXXXXXX.mailgun.org
MAIL_PASSWORD=your-mailgun-smtp-password
MAIL_DEFAULT_SENDER=noreply@sandboxXXXXXXXXXXXXXXXXXX.mailgun.org
```

### For Custom Domain:
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@mg.yourdomain.com
MAIL_PASSWORD=your-mailgun-smtp-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

**Example with Real Values:**
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USERNAME=postmaster@sandbox1a2b3c4d5e6f7g8h.mailgun.org
MAIL_PASSWORD=a1b2c3d4e5f6g7h8
MAIL_DEFAULT_SENDER=Job Tracker <noreply@sandbox1a2b3c4d5e6f7g8h.mailgun.org>
```

---

## Step 5: Test Your Configuration

Run the test script:
```powershell
.\.venv\Scripts\Activate.ps1
python test_email_config.py
```

---

## Mailgun Dashboard Features

### Send Test Email
1. Go to **Sending → Overview**
2. Click **"Send a Test Message"**
3. Enter recipient email
4. Send and verify delivery

### View Email Logs
1. Go to **Sending → Logs**
2. See all sent emails with delivery status
3. Filter by date, recipient, or status

### Check Statistics
1. Go to **Analytics**
2. View delivery rates, opens, clicks
3. Monitor email performance

---

## Troubleshooting

### Issue 1: "Sandbox Domain - Authorized Recipients Only"
**Solution**: 
- Add recipient email to Authorized Recipients list
- Or upgrade to custom domain

### Issue 2: "Authentication Failed"
**Solution**:
- Verify SMTP username is correct (includes @domain)
- Reset SMTP password in Mailgun dashboard
- Check for typos in .env file

### Issue 3: "Connection Timeout"
**Solution**:
- Verify port 587 is not blocked by firewall
- Try port 465 with `MAIL_USE_SSL=True` instead of `MAIL_USE_TLS=True`

### Issue 4: Emails Not Arriving
**Solution**:
- Check Mailgun logs for delivery status
- Verify recipient email is authorized (sandbox)
- Check spam folder
- Verify domain DNS records (custom domain)

---

## Best Practices

### Sender Name Format
Use a friendly name with email:
```bash
MAIL_DEFAULT_SENDER=Job Application Tracker <noreply@yourdomain.com>
```

### Email Templates
Mailgun supports:
- Plain text emails ✓ (currently used)
- HTML emails ✓ (currently used)
- Email templates (advanced)

### Rate Limits
- Free tier: 5,000 emails/month (first 3 months)
- After trial: 1,000 emails/month free
- Upgrade plans available for higher volumes

### Production Checklist
- [ ] Use custom domain (not sandbox)
- [ ] Verify all DNS records
- [ ] Test deliverability to major providers (Gmail, Outlook)
- [ ] Monitor bounce rates in Mailgun dashboard
- [ ] Set up webhooks for delivery tracking (advanced)

---

## API Alternative (Optional)

Instead of SMTP, you can use Mailgun's HTTP API:

```python
import requests

def send_email_via_api():
    return requests.post(
        "https://api.mailgun.net/v3/YOUR_DOMAIN/messages",
        auth=("api", "YOUR_API_KEY"),
        data={
            "from": "Job Tracker <noreply@yourdomain.com>",
            "to": ["user@example.com"],
            "subject": "Hello",
            "text": "Testing Mailgun API"
        }
    )
```

---

## Pricing (as of 2025)

| Plan | Price | Emails/Month |
|------|-------|--------------|
| Free Trial | $0 | 5,000 (3 months) |
| Foundation | $0 | 1,000 |
| Growth | $35 | 50,000 |
| Scale | $90 | 100,000 |

---

## Resources

- **Dashboard**: https://app.mailgun.com/
- **Documentation**: https://documentation.mailgun.com/
- **SMTP Guide**: https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#smtp-relay
- **Support**: https://help.mailgun.com/

---

## Quick Start Summary

1. ✅ Sign up at mailgun.com
2. ✅ Note your sandbox domain (automatic)
3. ✅ Add authorized recipient emails
4. ✅ Get SMTP credentials from dashboard
5. ✅ Update .env file with credentials
6. ✅ Run test_email_config.py
7. ✅ Send test emails!

**Your Mailgun setup is complete! 🚀📧**




