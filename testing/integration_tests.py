from io import BytesIO
import unittest
from flask import Flask
import sys
import json
import os
import random

sys.path.append("../SystemDeploymentProject")

import functions

class test_unit_routes(unittest.TestCase):
    
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
   
    def test_create_recipe_missing_fields(self):
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
        data2 = {
            'name': 'Test Recipe',
            'description': 'Test description',
            'category': '',
            'cuisine': '',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }
        
        with self.app.test_request_context('/addrecipe', method='POST', data=data2, content_type='multipart/form-data'):
            result = functions.add_recipe_function('test_recipe.json',recipedata)
            self.assertEqual(result, 'All fields are required!')

    #testing search recipe not found
    def test_search_recipe_not_found(self):
        
        query = 'Salad'#request query

        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
            
        with self.app.test_request_context('/search', method='GET'):
            # Call the search_recipe_function()
            result_recipes = functions.search_recipe_function(query,recipedata)
            # Verify that no recipes are found
            self.assertEqual(len(result_recipes), 0)

    #test add recipe with duplicate recipe name 
    def test_create_recipe_duplicate_recipe(self):

        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)

        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))

        data2 = {
            'name': 'Test Recipe '+random_string,
            'description': 'Test description',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }

        recipedata.append(data2)
    
        with self.app.test_request_context('/addrecipe', method='POST', data=data2, content_type='multipart/form-data'):
            result = functions.add_recipe_function('test_recipe.json',recipedata)
            self.assertEqual(result, 'Recipe already exists.')

    def test_edit_recipe_id_not_found(self):
            with open('test_recipe.json', 'r') as file:
                recipes = json.load(file)
            TEST_UPLOAD_FOLDER = 'test_images'

            data = {
                'name': 'Blueberry Pancake',
                'description': 'Delicious blueberry pancakes recipe',
                'category': 'Breakfast',
                'cuisine': 'American',
                'instructions': 'Step 1. Step 2. Step 3.',
                'ingredients': 'flour, milk, eggs, blueberries',
                'image': (BytesIO(b'TestImage'), 'test_pancake.jpeg')
            }
            with self.app.test_request_context('/editrecipe/55',method='POST', data=data, content_type='multipart/form-data'):
                # Call the add_recipe_function()
                result = functions.edit_recipe_function(55,data,'test_recipe.json',TEST_UPLOAD_FOLDER,recipes)
                self.assertIsNone(result)
     
    
     

if __name__ == '__main__':
    unittest.main()