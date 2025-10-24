"""
Verify Railway MySQL database tables
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

# Load environment variables
load_dotenv()

# Get MySQL URL
mysql_url = os.environ.get('MYSQL_URL')

if not mysql_url:
    print("❌ MYSQL_URL not set")
    exit(1)

# Convert to SQLAlchemy format
db_uri = mysql_url.replace('mysql://', 'mysql+mysqlconnector://')

print("=" * 60)
print("RAILWAY MYSQL DATABASE VERIFICATION")
print("=" * 60)
print(f"\nConnecting to: {mysql_url.split('@')[1]}")

try:
    # Create engine
    engine = create_engine(db_uri)
    inspector = inspect(engine)
    
    # Get tables
    tables = inspector.get_table_names()
    
    print(f"\n✓ Connected successfully!")
    print(f"\nDatabase: railway")
    print(f"Tables found: {len(tables)}")
    
    if not tables:
        print("\n⚠ No tables found!")
        print("\nRun this to create tables:")
        print('python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"')
    else:
        print("\n--- Tables ---")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"\n📋 {table}")
            print(f"   Columns: {len(columns)}")
            for col in columns:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                print(f"   - {col['name']:<20} {str(col['type']):<15} {nullable}")
        
        # Test queries
        print("\n" + "=" * 60)
        print("TABLE QUERY TEST")
        print("=" * 60)
        
        with engine.connect() as conn:
            if 'user' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM user"))
                count = result.fetchone()[0]
                print(f"✓ user table - {count} records")
            
            if 'job_application' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM job_application"))
                count = result.fetchone()[0]
                print(f"✓ job_application table - {count} records")
    
    print("\n" + "=" * 60)
    print("✓ RAILWAY MYSQL DATABASE IS READY!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    exit(1)
