#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union

def _hash_password(password: str) -> bytes:
    """Hashes the password with bcrypt and returns the salted hash"""
    password = password.encode('utf-8')  # Convert password to bytes
    salt = bcrypt.gensalt()  # Generate a salt
    hashed = bcrypt.hashpw(password, salt)  # Hash the password with the salt
    return hashed

def _generate_uuid() -> str:
    """
    Generate a uuid and return its string representation
    """
    return str(uuid4())

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
        db = self._db
        try:
            db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            user = db.add_user(email, hashed)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials
        Args:
            email (str): user's email address
            password (str): user's password
            bool: return true if validated and false if not
        Return:
            True if credentials are correct, else False
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        input_password = password.encode("utf-8")
        return bcrypt.checkpw(input_password, user.hashed_password)

    def create_session(self, email: str) -> Union[None,str]:
        """
        Create a session_id for an existing user and update the user's
        session_id attribute
        Args:
            email (str): user's email address
        Returns:
            str: session_id
            None: if user is not found
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        
        session_id = _generate_uuid()
        db.update_user(user.id, session_id=session_id)
        return session_id