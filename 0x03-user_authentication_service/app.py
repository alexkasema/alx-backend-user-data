#!/usr/bin/env python3
""" A Basic Flask Application """

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """ Return a JSON payload """

    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
