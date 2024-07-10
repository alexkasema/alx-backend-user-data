#!/usr/bin/env python3
""" User Session Model """

from models.base import Base


class UserSession(Base):
    """ Handles user sessions """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize an instance of UserSession """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
