#!/usr/bin/env python3
"""
Definition of _hash_password function
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes the password with bcrypt and returns the salted hash"""
    password = password.encode('utf-8')  # Convert password to bytes
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password, salt)  # Hash the password with the salt
    return hashed_password