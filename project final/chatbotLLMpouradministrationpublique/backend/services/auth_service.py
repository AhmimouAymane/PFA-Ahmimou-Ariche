from models.user import User
from database import db
from werkzeug.security import check_password_hash
import re

class AuthService:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        return True, None
    
    @staticmethod
    def register_user(email, username, password, first_name=None, last_name=None, preferred_language='fr'):
        """Register a new user"""
        # Validate email
        if not AuthService.validate_email(email):
            return None, "Invalid email format"
        
        # Validate password
        is_valid, error_msg = AuthService.validate_password(password)
        if not is_valid:
            return None, error_msg
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return None, "Email already registered"
        
        if User.query.filter_by(username=username).first():
            return None, "Username already taken"
        
        # Create user
        user = User(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            preferred_language=preferred_language
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user and return user object"""
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return None, "Invalid email or password"
        
        if not user.is_active:
            return None, "Account is deactivated"
        
        if not user.check_password(password):
            return None, "Invalid email or password"
        
        return user, None

