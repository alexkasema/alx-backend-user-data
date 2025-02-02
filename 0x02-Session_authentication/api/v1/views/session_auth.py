#!/usr/bin/env python3
""" Session Authentication View """

import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from typing import Tuple

from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ retrieves the user object """
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv('SESSION_NAME'), session_id)

        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """ destroy the session of the logged in user """
    from api.v1.app import auth

    destroy_session = auth.destroy_session(request)

    if not destroy_session:
        abort(404)
    return jsonify({}), 200
