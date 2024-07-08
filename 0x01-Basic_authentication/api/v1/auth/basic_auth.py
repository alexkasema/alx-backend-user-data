#!/usr/bin/env python3
""" Basic auth """

import base64
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic authentication handler """
    def extract_base64_authorization_header(
            self,
            authorization_header: str,
            ) -> str:
        """
        returns the Base64 part of the Authorization header
        """
        if not(authorization_header and isinstance(authorization_header, str)):
            return None
        if not(authorization_header.startswith('Basic ')):
            return None

        base64 = authorization_header[6:]

        return base64

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """ returns the decoded value of a Base64 string """
        if not(base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            return None

        try:
            decoded_value = base64.b64decode(base64_authorization_header)
            return decoded_value.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """ returns the user email and password from the Base64 decoded value.
        """
        if not(decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str) and
                ':' in decoded_base64_authorization_header):
            return(None, None)
        email, password = decoded_base64_authorization_header.split(":", 1)

        return (email, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str,
            ) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """
        if not(user_email and isinstance(user_email, str) and
                user_pwd and isinstance(user_pwd, str)):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """  retrieves the User instance for a request """
        try:
            auth_header = self.authorization_header(request)
            base64 = self.extract_base64_authorization_header(auth_header)
            decoded_value = self.decode_base64_authorization_header(base64)
            email, password = self.extract_user_credentials(decoded_value)
            user = self.user_object_from_credentials(email, password)

            return user
        except Exception:
            return None
