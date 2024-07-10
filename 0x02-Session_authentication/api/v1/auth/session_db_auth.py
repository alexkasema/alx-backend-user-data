#!/usr/bin/env python3
""" Session Authentication """

from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Handles Session Authentication """
    def create_session(self, user_id=None):
        """ Creates and stores new instance of UserSession and returns
            the Session ID
        """
        session_id = super().create_session(user_id)

        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }

            new_session = UserSession(**kwargs)
            new_session.save()

            return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieves user id associated with session id by requesting
            from UserSession
        """

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if len(sessions) <= 0:
            return None

        current_time = datetime.now()
        time_lapse = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_lapse

        if exp_time < current_time:
            return None

        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy user session based on the Session ID from the request cookie
        """
        session_id = self.session_cookie(request)

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if len(sessions) <= 0:
            return False

        sessions[0].remove()
        return True
