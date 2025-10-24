# Railway Deployment - Quick Reference

## 🚀 One-Command Setup

```bash
# 1. Deploy to Railway (connects your GitHub repo)
railway up

# 2. Add MySQL service in Railway Dashboard
Click "+" → "Database" → "Add MySQL"

# 3. Add environment variables in Railway Dashboard → Variables
(See list below)

# 4. Initialize database (one-time)
railway run python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## 📝 Environment Variables to Add in Railway

Copy/paste these into Railway Dashboard → Your Project → Variables:

```
SECRET_KEY=8fbde59b29c91530935e31bc6aa33f8875b13ac950975c1ce99190c1d3472490
FLASK_DEBUG=0
LOG_LEVEL=INFO
LOG_FILE=app.log
MAILGUN_API_KEY=your-mailgun-api-key-here
MAILGUN_DOMAIN=your-sandbox-domain.mailgun.org
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=postmaster@your-sandbox-domain.mailgun.org
MAIL_PASSWORD=your-mailgun-api-key-here
MAIL_DEFAULT_SENDER=Job Tracker <postmaster@your-sandbox-domain.mailgun.org>
```

**Railway Auto-Provides (don't add these):**
- MYSQL_URL
- MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLPORT, MYSQLDATABASE

---

## ✅ What Your App Does Automatically

1. **Detects Railway:** Checks for `MYSQL_URL` environment variable
2. **Converts Format:** Changes `mysql://` to `mysql+mysqlconnector://`
3. **Connects to MySQL:** Uses Railway's internal network
4. **Falls Back:** Uses SQLite if not on Railway (local dev)

---

## 🧪 Test Locally

```bash
# Start local server (uses SQLite)
flask run

# Check database
python check_db_tables.py

# Test email
python test_mailgun_email.py
```

---

## 🔍 Verify Railway Deployment

```bash
# View logs
railway logs

# Check environment
railway run python -c "from app import create_app; app = create_app(); print(app.config['SQLALCHEMY_DATABASE_URI'])"

# Check database tables
railway run python check_db_tables.py
```

---

## 📊 Expected Database Connection Strings

**Local Development:**
```
sqlite:///app.db
```

**Railway Production:**
```
mysql+mysqlconnector://root:****@container.railway.internal:3306/railway
```

---

## 🎯 Files Already Configured

- ✅ `config.py` - Auto-detects Railway MySQL
- ✅ `requirements.txt` - Has mysql-connector-python
- ✅ `Procfile` - Ready with gunicorn
- ✅ `wsgi.py` - Entry point configured
- ✅ `.env` - Local SQLite setup
- ✅ All models and routes ready

---

## 🚦 Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Railway project
- [ ] Connect GitHub repo to Railway
- [ ] Add MySQL service in Railway
- [ ] Add environment variables (see list above)
- [ ] Wait for deployment to complete
- [ ] Run database initialization command
- [ ] Visit your Railway URL
- [ ] Register first user
- [ ] Test adding job application

---

## 🆘 Quick Troubleshooting

**"No such table: user"**
→ Run: `railway run python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"`

**"Can't connect to MySQL"**
→ Check Railway Dashboard → MySQL service is running

**"Application Error"**
→ Run: `railway logs` to see error details

**"Email not sending"**
→ Check Mailgun sandbox authorized recipients

---

## 📞 Resources

- Railway Docs: https://docs.railway.app
- Mailgun Dashboard: https://app.mailgun.com
- Project Documentation: See `RAILWAY_MYSQL_SETUP.md`

---

## 🎉 You're Ready!

Your app is fully configured for Railway with MySQL. Just push and deploy!




