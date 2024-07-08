#!/usr/bin/env python3
""" API Authentication """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Manage API Authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check if path requires authentication """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] == '/':
            path = path[:-1]

        path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Checks Authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Checks current user """
        return None
