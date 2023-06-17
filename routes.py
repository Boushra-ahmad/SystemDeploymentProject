from flask import Blueprint,render_template, request, redirect, url_for, make_response, send_file
import json
import sys
from datetime import datetime
import os
import csv
import pandas as pd
import requests
import functions

main = Blueprint('main',__name__)#routename = main


recipes = functions.load_recipes_from_json()



#homepage
@main.route('/', methods=['GET'])
def home():
    recipes = functions.load_recipes_from_json()
    #print(recipes, file=sys.stderr)
    return render_template('index.html',recipes = recipes)

#add recipe
@main.route('/addrecipe',methods=['GET','POST'])
def add_recipe():
    message = functions.add_recipe_function('recipes.json',recipes)
 
    if message == 'Success':
        return redirect(url_for('main.home'))
    return render_template('add-recipe.html',message=message)
        
#view recipes
@main.route('/view/<int:id>',methods=['GET','POST','PUT'])
def view_recipe(id):
    recipe = functions.view_recipe(id)
    if recipe != "not found":
        #print(recipe, file=sys.stderr)
        
        return render_template('viewrecipes.html',recipes = recipe)



#editrecipe
@main.route('/editrecipe/<int:id>', methods=['GET','POST'])
def edit_recipe(id):    
    recipe = functions.get_by_id(id)
    message = functions.edit_recipe_function(id,recipe,'recipes.json',functions.UPLOAD_FOLDER,recipes)
    return render_template('editrecipe.html',recipe=recipe,message=message)

#delete recipe
@main.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):    
    functions.delete_recipe(id)
    return redirect(url_for('main.home'))

#search recipe
@main.route('/search',methods=['GET'])
def search_recipe():
    query= request.args.get('search')
    search_recipes = functions.search_recipe_function(query,recipes)
    return render_template('search-results.html', query=query, recipes=search_recipes)

#import recipes
@main.route('/import', methods=['GET','POST'])
def import_recipe():
    if request.method == 'POST':
        if 'import' in request.files:
            functions.import_recipe()                
            return redirect(url_for('main.home'))
        return 'Invalid file'
    return render_template('importRecipes.html')

#export recipes
@main.route('/export', methods=['GET','POST'])
def export_recipes():
    response = functions.export_recipes(functions.UPLOAD_FOLDER3,recipes)
    return response

@main.route('/rate/<int:id>',methods=['POST'])
def rate_recipe(id):
        # rating = request.form.get('rating')
        # tt = request.form.get('tt')
        # print(rating, file=sys.stderr)
        # print('id=',id, file=sys.stderr)

        functions.rating(id)
        return view_recipe(id)
