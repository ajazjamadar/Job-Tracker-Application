"""
Test MySQL Database Connection
Use this script to verify your MySQL connection works before deploying
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL database connection"""
    print("=" * 60)
    print("MYSQL CONNECTION TEST")
    print("=" * 60)
    
    # Check if Railway variables are set
    mysql_url = os.environ.get('MYSQL_URL')
    mysqluser = os.environ.get('MYSQLUSER')
    mysql_password = os.environ.get('MYSQLPASSWORD')
    mysql_host = os.environ.get('MYSQLHOST')
    mysql_port = os.environ.get('MYSQLPORT', '3306')
    mysql_database = os.environ.get('MYSQLDATABASE')
    
    print(f"\n--- Railway MySQL Configuration ---")
    print(f"MYSQL_URL: {mysql_url[:50] + '...' if mysql_url else '(Not set)'}")
    print(f"MYSQLUSER: {mysqluser or '(Not set)'}")
    print(f"MYSQLPASSWORD: {'*' * 20 if mysql_password else '(Not set)'}")
    print(f"MYSQLHOST: {mysql_host or '(Not set)'}")
    print(f"MYSQLPORT: {mysql_port}")
    print(f"MYSQLDATABASE: {mysql_database or '(Not set)'}")
    
    if not all([mysqluser, mysql_password, mysql_host, mysql_database]):
        print("\n❌ ERROR: Railway MySQL variables not set!")
        print("\nTo set them manually for testing, add to your .env file:")
        print("MYSQLUSER=root")
        print("MYSQLPASSWORD=your_password")
        print("MYSQLHOST=your-host.railway.internal")
        print("MYSQLPORT=3306")
        print("MYSQLDATABASE=railway")
        print("\nOr use the simplified MYSQL_URL:")
        print("MYSQL_URL=mysql://root:password@host.railway.internal:3306/railway")
        print("\nNote: Railway will set these automatically when deployed")
        return False
    
    # Build connection string
    connection_string = (
        f"mysql+mysqlconnector://{mysqluser}:{mysql_password}@"
        f"{mysql_host}:{mysql_port}/{mysql_database}"
    )
    
    print(f"\n--- Connection String ---")
    print(f"mysql+mysqlconnector://{mysqluser}:****@{mysql_host}:{mysql_port}/{mysql_database}")
    
    try:
        print(f"\n--- Testing Connection ---")
        print(f"Connecting to MySQL at {mysql_host}:{mysql_port}...")
        
        # Create engine
        engine = create_engine(connection_string)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✓ Connected successfully!")
            print(f"✓ MySQL Version: {version}")
            
            # Check if database exists
            result = connection.execute(text("SELECT DATABASE()"))
            current_db = result.fetchone()[0]
            print(f"✓ Current Database: {current_db}")
            
            # List tables
            result = connection.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print(f"\n--- Tables in Database ---")
            if tables:
                for table in tables:
                    print(f"  • {table[0]}")
                print(f"\nTotal: {len(tables)} table(s)")
            else:
                print("  No tables found (database is empty)")
                print("\n  To create tables, run:")
                print("  python -c \"from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()\"")
        
        print("\n" + "=" * 60)
        print("✓ MySQL CONNECTION TEST PASSED!")
        print("=" * 60)
        return True
        
    except OperationalError as e:
        print(f"\n❌ CONNECTION ERROR: {e}")
        print("\nPossible issues:")
        print("1. MySQL server is not running")
        print("2. Incorrect credentials")
        print("3. Host is not accessible (check RAILWAY_PRIVATE_DOMAIN)")
        print("4. Database does not exist")
        print("5. Firewall blocking connection")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def test_app_config():
    """Test that app config correctly uses MySQL"""
    print("\n" + "=" * 60)
    print("APP CONFIGURATION TEST")
    print("=" * 60)
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"\nConfigured Database URI:")
            # Mask password in output
            if '@' in db_uri:
                parts = db_uri.split('@')
                credentials = parts[0].split('://')[-1].split(':')
                masked_uri = db_uri.replace(credentials[1], '****')
                print(f"  {masked_uri}")
            else:
                print(f"  {db_uri}")
            
            if 'mysql' in db_uri:
                print("\n✓ App is configured to use MySQL")
            elif 'sqlite' in db_uri:
                print("\n⚠ App is configured to use SQLite (local development)")
            else:
                print(f"\n⚠ Unknown database type: {db_uri}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR loading app config: {e}")
        return False

if __name__ == "__main__":
    # Test MySQL connection
    mysql_ok = test_mysql_connection()
    
    # Test app configuration
    app_ok = test_app_config()
    
    print("\n" + "=" * 60)
    if mysql_ok and app_ok:
        print("✓ ALL TESTS PASSED - Ready for Railway deployment!")
    elif not mysql_ok:
        print("⚠ MySQL connection failed - Check Railway variables")
    else:
        print("⚠ Some tests failed - Check configuration")
    print("=" * 60)
