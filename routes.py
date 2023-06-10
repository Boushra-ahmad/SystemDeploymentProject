from flask import Blueprint,render_template, request,redirect,url_for
import json
import sys
from datetime import datetime
main = Blueprint('main',__name__)#routename = main

#load recipes.json
def load_recipes_from_json():
    with open('recipes.json', 'r') as file:
        data = json.load(file)
        return data

recipes = load_recipes_from_json()


#homepage
@main.route('/', methods=['GET'])
def home():
    recipes = load_recipes_from_json()
    #print(recipes, file=sys.stderr)
    return render_template('index.html',recipes = recipes)


#add recipe-get
@main.route('/addrecipe',methods=['GET','POST'])
def add_recipe():
    return render_template('add-recipe.html')

#view recipes
@main.route('/view',methods=['GET'])
def view_recipe():
    return render_template('viewrecipes.html')