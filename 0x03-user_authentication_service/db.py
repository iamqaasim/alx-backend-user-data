#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        Args:
            email (str): User's email address
            hashed_password (str): Hashed password for the user
        Returns:
            User: The created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Return a user who has an attribute
        matching the attributes passed as arguments
        Args:
            kwargs (dict): dict of key (k), value (v) pairs representing the
            attributes to update and the values to update them with
        Return:
            matching user or raise error
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        session = self._session
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
            else:
                raise ValueError()

        session.commit()