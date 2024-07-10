#!/usr/bin/env python3
""" Session Authentication Expiration """

import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Handles Session Expirations """
    def __init__(self):
        """ Initialize an instance of Session expiration duration """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session for the user """
        session_id = super().create_session(user_id)

        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieves a user id associated with a session id """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict.get('user_id')

            if 'created_at' not in session_dict:
                return None

            current_time = datetime.now()
            time_lapse = timedelta(seconds=self.session_duration)

            exp_time = session_dict['created_at'] + time_lapse

            if exp_time < current_time:
                return None

            return session_dict['user_id']
