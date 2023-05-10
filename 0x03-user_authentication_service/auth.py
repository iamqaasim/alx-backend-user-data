#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt
from db import DB
from db_utils import hash_password
from user import User

def _hash_password(password: str) -> bytes:
    """Hashes the password with bcrypt and returns the salted hash"""
    password = password.encode('utf-8')  # Convert password to bytes
    salt = bcrypt.gensalt()  # Generate a salt
    hashed = bcrypt.hashpw(password, salt)  # Hash the password with the salt
    return hashed


def register_user(self, email: str, password: str) -> User:
    try:
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists.")

        hashed_password = hash_password(password)
        user = self._db.add_user(email=email, hashed_password=hashed_password)
        return user
    except Exception as e:
        raise e