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
        
    #View Certain Recipe
    def test_view_recipe(self):
        # Define the recipe ID for the test
        recipe_id = 1
        with self.app.test_request_context(f'/view/{recipe_id}', method='GET'):
            # Call the view_recipe function
            recipe = functions.view_recipe(recipe_id)
            # Assert that the recipe is not "not found"
            self.assertNotEqual(recipe, "not found")
        
    #View All Recipes
    def test_view_all_recipes(self):
        with self.app.test_request_context('/', method='GET'):
            # Call the load_recipes_from_json function to get all recipes
            recipes = functions.load_recipes_from_json()
            # Assert that there are recipes available
            self.assertTrue(len(recipes) > 0)           
    
    #Add Recipe
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
                
    #delete recipe
    def test_delete_recipe_success(self):
        test_recipe_id = 7
        test_recipe_filename = 'test_recipe.json'

        with open(test_recipe_filename, 'r') as file:
            recipedata = json.load(file)

        data = {
            'name': 'Chocolate Chip Cookies',
            'description': 'Classic homemade chocolate chip cookies that are soft and chewy.',
            'category': 'Dessert',
            'cuisine': 'American',
            'instructions': [
                'Preheat the oven to 350°F (175°C).',
                'In a large bowl, cream together the butter, white sugar, and brown sugar until smooth.',
                'Beat in the eggs one at a time, then stir in the vanilla.',
                'Dissolve baking soda in hot water. Add to batter along with salt.',
                'Stir in the flour and chocolate chips.',
                'Drop rounded tablespoons of dough onto ungreased baking sheets.',
                'Bake for 10 to 12 minutes or until edges are golden brown.',
                'Cool on baking sheets for a few minutes before transferring to wire racks to cool completely.'
            ],
            'ingredients': [
                '1 cup unsalted butter, softened',
                '1 cup white sugar',
                '1 cup packed brown sugar',
                '2 eggs',
                '2 teaspoons vanilla extract',
                '1 teaspoon baking soda',
                '2 teaspoons hot water',
                '1/2 teaspoon salt',
                '3 cups all-purpose flour',
                '2 cups semisweet chocolate chips'
            ],
            'image': 'chocolate-chip-cookies.jpg',
            'date_published': '2022-05-10',
            'rating': '4.5'
        }
        
        recipedata.append(data)

        with open(test_recipe_filename, 'w') as file:
            json.dump(recipedata, file)

        functions.delete_recipe(test_recipe_filename, test_recipe_id)

        with open(test_recipe_filename, 'r') as file:
            updated_recipedata = json.load(file)

        self.assertNotIn(data, updated_recipedata)

    #export recipe
    def test_export_recipes(self):
        UPLOAD_FOLDER = 'test_files/export'
        response = functions.export_recipes(UPLOAD_FOLDER)
        # Assert the expected result
        self.assertIsNotNone(response)
        
if __name__ == '__main__':
    unittest.main()
