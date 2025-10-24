"""Verify database structure and contents."""
from app import app, db
from sqlalchemy import inspect, text

def verify_database():
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("=== DATABASE VERIFICATION ===\n")
        print(f"Database: {db.engine.url}\n")
        
        # Get all tables
        tables = inspector.get_table_names()
        print(f"--- Tables ({len(tables)}) ---")
        
        for table in tables:
            print(f"\n📋 {table.upper()}")
            
            # Show columns
            columns = inspector.get_columns(table)
            print("  Columns:")
            for col in columns:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f" DEFAULT {col['default']}" if col.get('default') else ""
                print(f"    • {col['name']:<20} {str(col['type']):<15} {nullable}{default}")
            
            # Show foreign keys
            fks = inspector.get_foreign_keys(table)
            if fks:
                print("  Foreign Keys:")
                for fk in fks:
                    const_cols = ', '.join(fk['constrained_columns'])
                    ref_cols = ', '.join(fk['referred_columns'])
                    print(f"    • {const_cols} -> {fk['referred_table']}.{ref_cols}")
            
            # Show indexes
            indexes = inspector.get_indexes(table)
            if indexes:
                print("  Indexes:")
                for idx in indexes:
                    cols = ', '.join(idx['column_names'])
                    unique = " (UNIQUE)" if idx['unique'] else ""
                    print(f"    • {idx['name']}: {cols}{unique}")
        
        # Count records
        print("\n\n--- Record Counts ---")
        with db.engine.connect() as conn:
            for table in tables:
                result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
                count = result.scalar()
                print(f"  {table:<20} {count:>5} records")
        
        print("\n✓ Database verification complete!")

if __name__ == '__main__':
    verify_database()
