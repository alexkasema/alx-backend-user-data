#!/usr/bin/env python3
""" A module that handles Authentication functionalities """

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Hash a password for the first time """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """ Generate UUIDs """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize an auth instance """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if user login credentials are valid """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password,
                )
        except NoResultFound:
            return False

        return False

    def create_session(self, email: str) -> str:
        """ Creates a session for a user and stores it in the db """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        if user is None:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id
