from flask import Blueprint,render_template, request
import json
import sys
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

#view recipes
@main.route('/view',methods=['GET'])
def view_recipe():
    return render_template('viewrecipes.html')