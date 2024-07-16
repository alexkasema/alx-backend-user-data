#!/usr/bin/env python3
""" End-to-end integration test """

import requests

BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test to validate user registration """

    body = {
        'email': email,
        'password': password,
    }

    response = requests.post(f'{BASE_URL}/users', data=body)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(f'{BASE_URL}/users', data=body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test for login with wrong password """

    body = {
        'email': email,
        'password': password,
    }

    response = requests.post(f'{BASE_URL}/sessions', data=body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test for successful login """

    body = {
        'email': email,
        'password': password
    }
    response = requests.post(f'{BASE_URL}/sessions', data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    session_id = response.cookies.get('session_id')

    return session_id


def profile_unlogged() -> None:
    """ Test for trying to access profile while logged out """

    cookies = {
        "session_id": ""
    }

    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test for user accessing thier profile """

    cookies = {
        "session_id": session_id
    }

    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Test for user logout and redirect to index/home page """

    cookies = {
        "session_id": session_id
    }

    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ Test to validate reset password token """

    body = {
        "email": email
    }

    response = requests.post(f'{BASE_URL}/reset_password', data=body)

    assert response.status_code == 200

    assert "email" in response.json()
    assert response.json()['email'] == email

    assert "reset_token" in response.json()

    reset_token = response.json().get('reset_token')

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test for validating password reset """

    body = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    response = requests.put(f'{BASE_URL}/reset_password', data=body)

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
