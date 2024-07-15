# User authentication service
In the industry, you should not implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: Flask-User). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

## user.py
User model
In this task you will create a SQLAlchemy model named User for a database table named users (by using the mapping declaration of SQLAlchemy).

The model will have the following attributes:

* id, the integer primary key
* email, a non-nullable string
* hashed_password, a non-nullable string
* session_id, a nullable string
* reset_token, a nullable string
