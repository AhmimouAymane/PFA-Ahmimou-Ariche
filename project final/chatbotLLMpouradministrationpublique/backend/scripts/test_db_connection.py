
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print("❌ ERROR: DATABASE_URL not found in .env")
    exit(1)

print(f"Testing connection to: {db_url.split('@')[-1]}")

try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = connection.execute(text("SHOW DATABASES;"))
        databases = [row[0] for row in result]
        print("✅ Connection successful!")
        print("Databases found:", databases)
        
        if 'chatbot_admin' in databases:
            print("✅ Database 'chatbot_admin' exists.")
        else:
            print("⚠️ Database 'chatbot_admin' does not exist. Attempting to create...")
            connection.execute(text("CREATE DATABASE chatbot_admin;"))
            print("✅ Database created.")
            
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)
