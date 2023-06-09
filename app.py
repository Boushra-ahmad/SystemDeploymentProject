import sys
from flask import Flask, jsonify, request,render_template
from flask_restful import Api
from http import HTTPStatus
from routes import main


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)
