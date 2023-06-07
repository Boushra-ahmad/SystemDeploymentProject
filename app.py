from flask import Flask, jsonify, request
from http import HTTPStatus
# jsonify to convert python object to json format
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
