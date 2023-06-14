from flask import Blueprint,render_template, request, redirect, url_for, make_response, send_file
import json
import sys
from datetime import datetime
import os
import csv
import pandas as pd
import requests

# Specify the directory where the images will be saved
UPLOAD_FOLDER = 'static/images'
UPLOAD_FOLDER2 = 'static/files/imported/'
UPLOAD_FOLDER3 = 'static/files/exported/'

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
        
def convert_xlsx_to_csv(xlsx_file, csv_file):
    # Read the XLSX file
    data_frame = pd.read_excel(xlsx_file)
    
    # Write the DataFrame to CSV file
    data_frame.to_csv(csv_file, index=False)

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
recipes = load_recipes_from_json()


def add_recipe_function(f):
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    cuisine = request.form['cuisine']
    instructions = request.form['instructions'].split('.')
    ingredients = request.form['ingredients'].split(',')
    images = request.files['image']
    date_published = datetime.now().strftime('%Y-%m-%d')

    #validation
    if not name or not description or not category or not cuisine or not instructions or not ingredients or not images:
        message = "All fields are required!"
        return message
    elif any(recipe['name'] == name for recipe in recipes):
        message = 'Recipe already exists.'
        return message
    else:
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
            'image':image_file.filename,
            'date_published': date_published
        }
        # Add the new recipe to the existing recipes
        existing_recipes.append(new_recipe)
        # Write the updated recipes back to the JSON file
        with open(f, 'w') as file:
            json.dump(existing_recipes, file, indent=4)

        if new_recipe in existing_recipes:
            message = "Success"
            return message 
        else:
            return message


def view_recipe(id):
    return get_by_id(id)

def edit_recipe(id):
    recipe = get_by_id(id)
    message = None
    if request.method == 'POST':
        image_file = request.files['image']
        filename = None
        category = request.form['category']
        new_category = None
       
        if image_file:
            existing_image_filename = recipe['image']
            # Get the path of the existing image file
            existing_image_path = os.path.join(UPLOAD_FOLDER, existing_image_filename)
            # Check if the existing image file exists
            if os.path.exists(existing_image_path):
                # Remove the existing image file
                os.remove(existing_image_path)
            
            # Save the image file to the specified directory
            filename = image_file.filename
            image_file.save(os.path.join(UPLOAD_FOLDER, filename))       
        else:
            filename = recipe['image']

        if category:
            new_category = request.form['category']
        else:
            new_category = recipe['category']

        new_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'category':new_category,
            'cuisine': request.form['cuisine'],
            'instructions': request.form['instructions'].split('.'),
            'ingredients': request.form['ingredients'].split(','),
            'image':filename
        }

        with open('recipes.json', 'r') as file:
            recipes = json.load(file)

        # Find the recipe to update based on its ID
        for recipe in recipes:
            if recipe['id'] == id:
                # Update the recipe data with the new values
                recipe.update(new_data)
                message = "Updated Successfully"
                break

        with open('recipes.json', 'w') as file:
            json.dump(recipes, file, indent=4)

    return recipe, message