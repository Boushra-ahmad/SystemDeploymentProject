from io import BytesIO
import unittest
from flask import Flask
import sys
import json
import os

sys.path.append("../SystemDeploymentProject")

import functions

class test_unit_routes(unittest.TestCase):
    
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        
    def test_view_recipe(self):
        # Define the recipe ID for the test
        recipe_id = 1
        with self.app.test_request_context(f'/view/{recipe_id}', method='GET'):
            # Call the view_recipe function
            recipe = functions.view_recipe(recipe_id)
            # Assert that the recipe is not "not found"
            self.assertNotEqual(recipe, "not found")
            
           
    def test_add_recipe_success(self):
        data = {
            'name': 'Test Recipe',
            'description': 'Test description',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }
        with self.app.test_request_context('/addrecipe', method='POST', data=data, content_type='multipart/form-data'):
            # Call the add_recipe_function()
            result = functions.add_recipe_function('test_recipe.json')
            # Assert the expected result
            self.assertEqual(result, 'Success')


  #search recipe testing
    def test_search_recipe(self):
            # request query
            query = 'butter chicken'

            with open('test_recipe.json', 'r') as file:
                recipedata = json.load(file)
            
            with self.app.test_request_context('/search', method='GET'):
                # Call the add_recipe_function()
                result_recipes = functions.search_recipe_function(query,recipedata)
                # Assert the expected result
                # self.assertEqual(query, query)
                self.assertEqual(len(result_recipes), 1)
                self.assertEqual(result_recipes[0]['name'], 'Butter Chicken')

   
    #edit recipe 
    def test_edit_recipe_success(self):
            # with open('test_recipe.json', 'r') as file:
            #     recipes = json.load(file)
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
            with self.app.test_request_context('/editrecipe/1',method='POST', data=data, content_type='multipart/form-data'):
                # Call the add_recipe_function()
                result = functions.edit_recipe_function(1,data,'test_recipe.json',TEST_UPLOAD_FOLDER)
                # Assert the expected result
                self.assertEqual(result, 'Updated Successfully')



if __name__ == '__main__':
    unittest.main()
