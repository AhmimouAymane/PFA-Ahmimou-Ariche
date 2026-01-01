"""
Simple script to create the chatbot_admin database
Usage: python create_db_simple.py [password]
Or set MYSQL_PASSWORD or MYSQL_ROOT_PASSWORD environment variable
"""
import pymysql
import sys
import os

def create_database(password=None):
    """Create the chatbot_admin database"""
    if password is None:
        password = os.getenv('MYSQL_PASSWORD') or os.getenv('MYSQL_ROOT_PASSWORD')
        if password is None:
            print("Usage: python create_db_simple.py YOUR_PASSWORD")
            print("Or set MYSQL_PASSWORD or MYSQL_ROOT_PASSWORD environment variable")
            print("\nExample:")
            print('  python create_db_simple.py mypassword')
            print("Or:")
            print('  $env:MYSQL_PASSWORD="mypassword"; python create_db_simple.py')
            sys.exit(1)
    
    conn_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': password,
        'charset': 'utf8mb4'
    }
    
    db_name = 'chatbot_admin'
    
    try:
        print(f"Connecting to MySQL server...")
        conn = pymysql.connect(**conn_params)
        cursor = conn.cursor()
        
        # Check if database already exists
        cursor.execute(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
            (db_name,)
        )
        
        if cursor.fetchone():
            print(f"✓ Database '{db_name}' already exists!")
            print(f"You can use it directly in your .env file.")
        else:
            # Create database
            print(f"Creating database '{db_name}'...")
            cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
            print(f"✓ Database '{db_name}' created successfully!")
        
        cursor.close()
        conn.close()
        
        print(f"\nDatabase connection string for .env file:")
        print(f"DATABASE_URL=mysql+pymysql://root:{password}@localhost:3306/{db_name}")
        
    except pymysql.OperationalError as e:
        print(f"\n✗ Error connecting to MySQL: {e}")
        print("\nPossible issues:")
        print("1. MySQL service is not running")
        print("2. Wrong password")
        print("3. MySQL not installed or not accessible on localhost:3306")
        print("4. pymysql not installed (run: pip install pymysql)")
        print("\nTo start MySQL service:")
        print("  - Open Services (services.msc)")
        print("  - Find 'MySQL' service")
        print("  - Start it if it's stopped")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    password = sys.argv[1] if len(sys.argv) > 1 else None
    create_database(password)
