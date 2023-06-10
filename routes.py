from flask import Blueprint,render_template, request, url_for
import json
import sys
main = Blueprint('main',__name__)#routename = main

#load recipes.json
def load_recipes_from_json():
    with open('recipes.json', 'r') as file:
        data = json.load(file)
        return data

def get_by_id(id):
     with open('recipes.json', 'r') as file:
        data = json.load(file)
        for i in data:
            if i['id'] == id*1:
                #print(i, file=sys.stderr)
                return i
        else:
            return "not found"
     
recipes = load_recipes_from_json()


#homepage
@main.route('/', methods=['GET'])
def home():
    recipes = load_recipes_from_json()
    #print(recipes, file=sys.stderr)
    return render_template('index.html',recipes = recipes)

#view recipes
@main.route('/view/<int:id>',methods=['GET'])
def view_recipe(id):
    recipe = get_by_id(id)
    #print(recipe, file=sys.stderr)
    return render_template('viewrecipes.html',recipes = recipe)