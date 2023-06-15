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
    data = load_recipes_from_json()
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

#Add Recipes
def add_recipe_function(f):
    if request.method == "POST":
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
                existing_recipes = load_recipes_from_json()
                
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
                    'date_published': date_published,
                    'rating' : 0
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


#View Recipes
def view_recipe(id):
    return get_by_id(id)

#Edit Recipes
def edit_recipe_function(id,recipe,f,UPLOAD_FOLDER):
    # recipe = get_by_id(id)
    image_file=None
    message = None
    if request.method == 'POST':
        image_file = request.files['image']
        filename = None
        category = request.form['category']
        new_category = None
       
        if image_file:
            existing_image_filename = recipe['image']
            # Get the path of the existing image file
            if recipe['image'] == image_file.filename:
                existing_image_path = os.path.join(UPLOAD_FOLDER, existing_image_filename)
                # Check if the existing image file exists
                if os.path.exists(existing_image_path):
                    # Remove the existing image file
                    os.remove(existing_image_path)
            else:
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

        recipes = load_recipes_from_json()

        # Find the recipe to update based on its ID
        for recipe in recipes:
            if recipe['id'] == id:
                # Update the recipe data with the new values
                recipe.update(new_data)
                message = "Updated Successfully"
                break

        with open(f, 'w') as file:
            json.dump(recipes, file, indent=4)

        return message

#Delete Recipes    
def delete_recipe(id):
    #Get the recipes from the recipes.json file
    existing_recipes = load_recipes_from_json()
        
    filtered_data = [existing_recipes.remove(recipe) for recipe in existing_recipes if recipe['id'] == id]

    # Save the updated recipes back to the JSON file
    with open('recipes.json', 'w') as file:
        json.dump(existing_recipes, file, indent=4)

#Search Recipes   
def search_recipe_function(query,recipes):
    search_recipes = []
    for recipe in recipes:
        print(recipe['rating'], file=sys.stderr)
        if query.lower() in recipe['name'].lower():
            search_recipes.append(recipe)
        elif query.lower() in recipe['category'].lower():
            search_recipes.append(recipe)
        elif query.lower() in recipe['cuisine'].lower():
            search_recipes.append(recipe)
        elif recipe['rating'] == query:
            search_recipes.append(recipe)
    return search_recipes

#Import Recipes
def import_recipe():
    csvFile = request.files['import']
    filename = csvFile.filename
           
    #Create the folder 'static/files/imported' if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER2):
        os.makedirs(UPLOAD_FOLDER2)
    csvFile.save(os.path.join(UPLOAD_FOLDER2, filename))
    if filename.endswith('.xlsx'):
        # Handle XLSX file
        csvFile = 'static/files/imported/xlsxToCSV.csv'
        convert_xlsx_to_csv(UPLOAD_FOLDER2 + filename, csvFile)
         
    existingRecipes = load_recipes_from_json()

    # Open a csv reader called DictReader
    with open(csvFile) as csvf:
        save_directory = 'static/images'             

        # Convert each row into a dictionary and add it to data
        csvReader = csv.DictReader(csvf)                    
        for rows in csvReader:                    
            image_filename = rows['name'] + '.jpg'
                    
            # Combine the save directory and image filename to create the save path
            save_path = os.path.join(save_directory, image_filename)
                    
            # Create the save directory if it doesn't exist
            os.makedirs(save_directory, exist_ok=True)
            download_image(rows['image'], save_path)
                    
            # Generate a unique ID for the new recipe
            rows['id'] = len(existingRecipes) + 1
            rows['instructions'] = list(rows['instructions'].split(". "))
            rows['instructions'] = [instruction + '.' if index != len(rows['instructions']) - 1 else instruction for index, instruction in enumerate(rows['instructions'])]
            rows['ingredients'] = list(rows['ingredients'].split(', '))
            rows['image'] = rows['name'] + '.jpg'
                    
            # Add the new recipe to the existing recipes
            existingRecipes.append(rows)

        # Write the updated recipes back to the JSON file
    with open('recipes.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(existingRecipes, indent=4))

#Export Recipes
def export_recipes():
    jsonData = load_recipes_from_json()
        
    #Create the folder 'static/files/exported if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER3):
        os.makedirs(UPLOAD_FOLDER3)
    
    file_name = 'recipes.csv'
    csv_file_path = os.path.join(UPLOAD_FOLDER3, file_name)

    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        count = 0

        for data in jsonData:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            data['instructions'] = " ".join(data['instructions'])
            data['ingredients'] = ", ".join(data['ingredients'])
            csv_writer.writerow(data.values())

    # Create a response with the file
    response = make_response(send_file(csv_file_path, as_attachment=False))
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def rating(id):
    recipe = get_by_id(id)

    rating = rating = request.form.get('rating')
    print(rating, file=sys.stderr)

    new_data = {
            'name': recipe['name'],
            'description': recipe['description'],
            'category':recipe['category'],
            'cuisine': recipe['cuisine'],
            'instructions': recipe['instructions'],
            'ingredients': recipe['ingredients'],
            'image':recipe['image'],
            'date_published': recipe['date_published'],
            'rating': rating
        }

    recipes = load_recipes_from_json()

    # Find the recipe to update based on its ID
    for recipe in recipes:
        if recipe['id'] == id:
            # Update the recipe data with the new values
            recipe.update(new_data)
            message = "Updated Successfully"
            break

    with open('recipes.json', 'w') as file:
        json.dump(recipes, file, indent=4)
    
    return recipe