from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.User import User
import bcrypt

load_dotenv()

# Load JWT secret from environment variables or fallback to a default (not recommended for production)
JWT_SECRET = os.getenv('JWT_SECRET', 'your_jwt_secret_here')


class AuthService:

    @staticmethod
    def register(db: Session, username: str, email: str, password: str, re_pass: str):
        # Check if passwords match
        if password != re_pass:
            raise ValueError('Password mismatch')

        # Check if user exists by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()  # get first match

        if user:
            raise ValueError('User already exists')

        # Create new user and hash password
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.add(new_user)
        db.commit()  # save changes to DB
        db.refresh(new_user)  # refresh instance with new data

        # Return JWT token
        return AuthService.generate_token(new_user)

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter_by(email=email).first()

        if not user or not user.check_password(password):
            raise ValueError('Invalid user or password')

        token = AuthService.generate_token(user)
        return user, token  # Return both user and token

    @staticmethod
    def generate_token(user: User):
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=2)
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return token if isinstance(token, str) else token.decode('utf-8')
