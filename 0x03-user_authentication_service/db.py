#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
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
        """ Adds user to the database. """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Find users in the database. """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except (NoResultFound, InvalidRequestError):
            raise

    def update_user(self, user_id, **kwargs):
        """Updates user in database"""
        user = self.find_user_by(id=user_id)
        columns = User.__table__.columns.keys()
        for key, value in kwargs.items():
            if key not in columns:
                raise ValueError
            setattr(user, key, value)
        self._session.add(user)
        self._session.commit()
