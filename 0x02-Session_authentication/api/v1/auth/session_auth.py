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
