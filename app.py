import sys
from flask import Flask, jsonify, request,render_template
from flask_restful import Api
from http import HTTPStatus


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')
    
    register_resources(app)

    return app

def register_resources(app):
    api = Api(app)


if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)
