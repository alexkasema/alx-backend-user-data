#!/usr/bin/env python3
""" A module that handles Authentication functionalities """

import bcrypt


def _hash_password(password: str) -> bytes:
    """ Hash a password for the first time """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed
