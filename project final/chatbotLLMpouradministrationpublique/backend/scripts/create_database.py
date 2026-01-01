"""
Script to create the chatbot_admin database
Make sure MySQL is running before executing this script
"""
import pymysql
import sys

def create_database():
    """Create the chatbot_admin database"""
    # Connection parameters - modify these if needed
    # Default MySQL connection
    conn_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': None,  # Will prompt if needed
        'charset': 'utf8mb4'
    }
    
    # Try to get password from environment or prompt
    import os
    password = os.getenv('MYSQL_PASSWORD') or os.getenv('MYSQL_ROOT_PASSWORD')
    
    if not password:
        print("Enter your MySQL root password:")
        password = input().strip()
    
    conn_params['password'] = password
    
    db_name = 'chatbot_admin'
    
    try:
        # Connect to MySQL server
        print(f"Connecting to MySQL server...")
        conn = pymysql.connect(**conn_params)
        
        cursor = conn.cursor()
        
        # Check if database already exists
        cursor.execute(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
            (db_name,)
        )
        
        if cursor.fetchone():
            print(f"Database '{db_name}' already exists!")
            response = input("Do you want to drop it and recreate? (yes/no): ").strip().lower()
            if response == 'yes':
                cursor.execute(f"DROP DATABASE `{db_name}`")
                print(f"Database '{db_name}' dropped.")
            else:
                print("Keeping existing database.")
                cursor.close()
                conn.close()
                return
        
        # Create database
        print(f"Creating database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ Database '{db_name}' created successfully!")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\nYou can now use this database in your .env file:")
        print(f"DATABASE_URL=mysql+pymysql://root:{password}@localhost:3306/{db_name}")
        
    except pymysql.OperationalError as e:
        print(f"Error connecting to MySQL: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL service is running")
        print("2. Check your username and password")
        print("3. Verify MySQL is running on localhost:3306")
        print("4. Make sure pymysql is installed: pip install pymysql")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_database()
