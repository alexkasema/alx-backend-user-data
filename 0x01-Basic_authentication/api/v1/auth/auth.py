#!/usr/bin/env python3
""" API Authentication """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Manage API Authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check for authentication requirement """
        return False

    def authorization_header(self, request=None) -> str:
        """ Checks Authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Checks current user """
        return None
