from flask import Blueprint,render_template, request

#routename = main
main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def home():
    return render_template('index.html')