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

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                next_idx_after_slash = excluded_path.rfind('/') + 1
                excluded = excluded_path[next_idx_after_slash:-1]

                next_idx_after_slash = path.rfind('/') + 1
                tmp_path = path[next_idx_after_slash:]

                if excluded in tmp_path:
                    return False

        path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Checks Authorization header """
        if request is None:
            return None

        value = request.headers.get('Authorization')
        return value

    def current_user(self, request=None) -> TypeVar('User'):
        """ Checks current user """
        return None
