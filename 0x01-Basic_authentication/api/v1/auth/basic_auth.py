#!/usr/bin/env python3
""" Basic auth """

from api.v1.auth.auth import Auth


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
