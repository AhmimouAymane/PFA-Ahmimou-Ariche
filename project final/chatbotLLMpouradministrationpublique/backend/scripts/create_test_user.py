
import os
import sys

# Add parent directory to path to import app and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database import db
from models.user import User

def create_test_user():
    app = create_app()
    with app.app_context():
        # Check if user exists
        existing_user = User.query.filter_by(email='test@test.com').first()
        if existing_user:
            print("Test user already exists!")
            return

        user = User(
            email='test@test.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            preferred_language='fr'
        )
        user.set_password('password123')
        
        db.session.add(user)
        try:
            db.session.commit()
            print("Test user created successfully!")
            print("Email: test@test.com")
            print("Password: password123")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_test_user()
