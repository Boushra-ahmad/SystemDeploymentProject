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
         
    #add recipe
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

    def test_create_recipe_missing_fields(self):
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
            result = functions.add_recipe_function('test_recipe.json')
            self.assertEqual(result, 'All fields are required!')


if __name__ == '__main__':
    unittest.main()