from flask import Blueprint,render_template, request, redirect, url_for
import json
import sys
from datetime import datetime
import os

main = Blueprint('main',__name__)#routename = main


# Specify the directory where the images will be saved
UPLOAD_FOLDER = 'static/images'

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


#add recipe
@main.route('/addrecipe',methods=['GET','POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        cuisine = request.form['cuisine']
        instructions = request.form['instructions'].split(',')
        ingredients = request.form['ingredients'].split(',')
        date_published = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
         # Check if a file was uploaded
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file:
                # Save the image file to the specified directory
                filename = image_file.filename
                image_file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Load the existing recipes from the JSON file
        with open('recipes.json', 'r') as file:
            existing_recipes = json.load(file)
        
        # Generate a unique ID for the new recipe
        new_recipe_id = len(existing_recipes) + 1

        # Create a new recipe object
        new_recipe = { 
            'id': new_recipe_id, 
            'name': name, 
            'description': description, 
            'category': category, 
            'cuisine': cuisine, 
            'instructions': instructions, 
            'ingredients': ingredients, 
            'date_published': date_published,
            'image':image_file.filename
        }
        # Add the new recipe to the existing recipes
        existing_recipes.append(new_recipe)
        # Write the updated recipes back to the JSON file
        with open('recipes.json', 'w') as file:
            json.dump(existing_recipes, file, indent=4)

        #return to homepage
        return redirect(url_for('main.home'))
    return render_template('add-recipe.html')

#view recipes
@main.route('/view/<int:id>',methods=['GET'])
def view_recipe(id):
    recipe = get_by_id(id)
    #print(recipe, file=sys.stderr)
    return render_template('viewrecipes.html',recipes = recipe)


#search recipe
@main.route('/search',methods=['GET'])
def search_recipe():
    query= request.args.get('search')
    search_recipes = []
    for recipe in recipes:
        if query.lower() in recipe['name'].lower():
            search_recipes.append(recipe)
        elif query.lower() in recipe['category'].lower():
            search_recipes.append(recipe)
        elif query.lower() in recipe['cuisine'].lower():
            search_recipes.append(recipe)
    # print(search_recipes, file=sys.stderr)
    return render_template('search-results.html', query=query, recipes=search_recipes)


