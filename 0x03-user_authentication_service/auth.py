#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import (
    Union,
    TypeVar
)

from user import User

U = TypeVar(User)


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

    def create_session(self, email: str) -> Union[None, str]:
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

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """
        Takes a session_id and returns the corresponding user
        Args:
            session_id (str): session id for user
        Returns:
            U: user that corresponds to session_id
        """
        db = self._db
        if session_id is None:
            return None

        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        sets the session_id to None
        Args:
            user_id (int): user id
        """
        db = self._db
        db.update_user(user_id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset_token uuid for a user
        Args:
            email (str): user's email address
        Returns:
            str: generated reset_token
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        db.update_user(user.id, reset_token=reset_token)
        return reset_token
     
    def update_password(self, reset_token: str, password: str) -> None:
        """_summary_

        Args:
            reset_token (str): _description_
            password (str): _description_
        """
        db = self._db
        try:
            user = db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        
        new_password = _hash_password(password)
        db.update_user(user.id, hashed_password=new_password, reset_token=None)
