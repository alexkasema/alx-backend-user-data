#!/usr/bin/env python3
""" Session authentication """

from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Handle Session Authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a session ID for a user_id """

        if not(user_id and isinstance(user_id, str)):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve a user id associated with a session_id """

        if not(session_id and isinstance(session_id, str)):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id
