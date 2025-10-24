# Railway Deployment Guide for Job Application Tracker

## MySQL Database Setup

Your Railway MySQL database is automatically configured with these environment variables:

**Primary (Recommended):**
- `MYSQL_URL` - Complete MySQL connection URL (easiest to use)

**Individual Variables:**
- `MYSQLUSER` - MySQL username (value: "root")
- `MYSQLPASSWORD` - MySQL password (auto-generated)
- `MYSQLHOST` - Internal Railway hostname (e.g., "container-name.railway.internal")
- `MYSQLPORT` - MySQL port (value: 3306)
- `MYSQLDATABASE` - Database name (value: "railway")
- `MYSQL_ROOT_PASSWORD` - Same as MYSQLPASSWORD
- `MYSQL_DATABASE` - Same as MYSQLDATABASE

## Deployment Steps

### 1. Connect Your Repository to Railway
```bash
# If using Railway CLI:
railway login
railway link
```

### 2. Configure Environment Variables in Railway Dashboard

Go to your Railway project → Variables and add:

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

**Note**: Railway will automatically provide these MySQL variables:
- MYSQL_URL (complete connection string - easiest)
- MYSQLUSER
- MYSQLPASSWORD
- MYSQLHOST
- MYSQLPORT
- MYSQLDATABASE

### 3. Database Initialization

After deployment, you need to create the database tables. Run this command in Railway:

```bash
# Using Railway CLI:
railway run flask db upgrade

# Or use the Railway dashboard shell to run:
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 4. Verify Deployment

Your application will be accessible at the Railway-provided URL (e.g., `https://your-app.up.railway.app`)

## Database Connection String Format

The application uses Railway's `MYSQL_URL` and converts it to SQLAlchemy format:

**Railway provides:**
```
mysql://root:password@hostname.railway.internal:3306/railway
```

**App converts to:**
```
mysql+mysqlconnector://root:password@hostname.railway.internal:3306/railway
```

Alternatively, if MYSQL_URL is not available, it builds from individual variables:
```
mysql+mysqlconnector://${MYSQLUSER}:${MYSQLPASSWORD}@${MYSQLHOST}:${MYSQLPORT}/${MYSQLDATABASE}
```

## Local Development vs Production

### Local Development (SQLite):
```bash
# Use .env file with:
SQLALCHEMY_DATABASE_URI=sqlite:///app.db

# Run locally:
flask run
```

### Railway Production (MySQL):
- Railway automatically sets MySQL environment variables
- `config.py` detects Railway variables and uses MySQL
- No need to modify SQLALCHEMY_DATABASE_URI in Railway

## Troubleshooting

### Connection Issues:
1. Check Railway logs: `railway logs`
2. Verify all environment variables are set in Railway dashboard
3. Ensure MySQL service is running in Railway

### Migration Issues:
```bash
# Reset migrations (if needed):
railway run flask db stamp head
railway run flask db migrate -m "Initial migration"
railway run flask db upgrade
```

### Check Database Connection:
```python
# In Railway shell:
python -c "from app import create_app, db; app = create_app(); print(app.config['SQLALCHEMY_DATABASE_URI'])"
```

## Important Notes

1. **Never commit** `.env` file with production secrets
2. **Always use** Railway dashboard to set production environment variables
3. **Test locally** with SQLite before deploying to Railway
4. **Backup** your MySQL database regularly using Railway dashboard

## Files Required for Railway Deployment

✓ `Procfile` - Defines how to run the app
✓ `requirements.txt` - Python dependencies
✓ `wsgi.py` - WSGI entry point
✓ `.env.example` - Example environment variables (for reference)
✓ `config.py` - Auto-detects Railway MySQL variables

All files are already configured! Just push to Railway.




