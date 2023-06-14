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

#homepage
@main.route('/', methods=['GET'])
def home():
    recipes = functions.load_recipes_from_json()
    #print(recipes, file=sys.stderr)
    return render_template('index.html',recipes = recipes)

#add recipe
@main.route('/addrecipe',methods=['GET','POST'])
def add_recipe():
    message = functions.add_recipes()      
        #return to homepage
    if message == 'Success':
        return redirect(url_for('main.home'))
    return render_template('add-recipe.html',message=message)
        
#view recipes
@main.route('/view/<int:id>',methods=['GET'])
def view_recipe(id):
    recipe = functions.view_recipe(id)
    if recipe != "not found":
        #print(recipe, file=sys.stderr)
        return render_template('viewrecipes.html',recipes = recipe)

#editrecipe
@main.route('/editrecipe/<int:id>', methods=['GET','POST'])
def edit_recipe(id):    
    recipe, message = functions.edit_recipe(id)                
    return render_template('editrecipe.html',recipe=recipe,message=message)

#delete recipe
@main.route('/delete_recipe/<int:id>', methods=['GET','POST'])
def delete_recipe(id):    
    functions.delete_recipe(id)
    return redirect(url_for('main.home'))

#search recipe
@main.route('/search',methods=['GET'])
def search_recipe():
    query, search_recipes = functions.search_recipe()
    # print(search_recipes, file=sys.stderr)
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
    response = functions.export_recipes()
    return response