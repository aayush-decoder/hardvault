"""
Script to reset database for custom user model migration
Run this before migrating with custom user model
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection details from settings.py
DB_CONFIG = {
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_mNjAw3sZJ4Px",
    "host": "ep-wandering-darkness-a18au3pb-pooler.ap-southeast-1.aws.neon.tech",
    "port": "5432",
    "sslmode": "require"
}

def reset_database():
    """Drop all tables and reset migrations"""
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("Dropping all tables...")
        
        # Get all tables
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = cursor.fetchall()
        
        # Drop each table
        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
        
        print("\n✓ All tables dropped successfully!")
        print("\nNext steps:")
        print("1. Delete all migration files in accounts/migrations/ (except __init__.py)")
        print("2. Delete all migration files in owner/migrations/ (except __init__.py)")
        print("3. Run: python manage.py makemigrations")
        print("4. Run: python manage.py migrate")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    confirm = input("This will DELETE ALL DATA in the database. Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        reset_database()
    else:
        print("Operation cancelled.")
