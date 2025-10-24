"""
Check if database tables are properly created
"""
from app import create_app, db
from app.models import User, JobApplication
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    # Get database inspector
    inspector = inspect(db.engine)
    
    print("=" * 60)
    print("DATABASE TABLES CHECK")
    print("=" * 60)
    
    # Get all table names
    tables = inspector.get_table_names()
    
    print(f"\nDatabase: {db.engine.url}")
    print(f"\nTables found: {len(tables)}")
    
    for table in tables:
        print(f"\n📋 Table: {table}")
        columns = inspector.get_columns(table)
        print(f"   Columns: {len(columns)}")
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"   - {col['name']:<20} {col['type']!s:<15} {nullable}")
    
    # Check if required tables exist
    print("\n" + "=" * 60)
    print("REQUIRED TABLES CHECK")
    print("=" * 60)
    
    required_tables = ['user', 'job_application']
    
    for table in required_tables:
        if table in tables:
            print(f"✓ {table} - EXISTS")
        else:
            print(f"✗ {table} - MISSING")
    
    # Try to query tables
    print("\n" + "=" * 60)
    print("TABLE QUERY TEST")
    print("=" * 60)
    
    try:
        user_count = User.query.count()
        print(f"✓ User table accessible - {user_count} users")
    except Exception as e:
        print(f"✗ User table error: {e}")
    
    try:
        app_count = JobApplication.query.count()
        print(f"✓ JobApplication table accessible - {app_count} applications")
    except Exception as e:
        print(f"✗ JobApplication table error: {e}")
    
    print("\n" + "=" * 60)
    
    if len(tables) < 2:
        print("\n⚠ WARNING: Tables are missing!")
        print("\nTo create tables, run:")
        print("  flask db upgrade")
        print("\nOr if migrations don't work:")
        print("  python -c \"from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()\"")
    else:
        print("\n✓ Database is properly set up!")
