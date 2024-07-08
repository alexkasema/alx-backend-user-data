#!/usr/bin/env python3
""" Basic auth """

import base64
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
