#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> bytes:
    """Hashes the password with bcrypt and returns the salted hash"""
    password = password.encode('utf-8')  # Convert password to bytes
    salt = bcrypt.gensalt()  # Generate a salt
    hashed = bcrypt.hashpw(password, salt)  # Hash the password with the salt
    return hashed

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        Args:
            email (str): new user's email address
            password (str): new user's password
        Return:
            if no user with given email exists, return new user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")
