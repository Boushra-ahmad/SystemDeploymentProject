from io import BytesIO
import unittest
from flask import Flask
import sys
import json
import os
import random
from werkzeug.datastructures import FileStorage
import openpyxl

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
            recipe = functions.view_recipe('test_recipe.json',recipe_id)
            # Assert that the recipe is not "not found"
            self.assertNotEqual(recipe, "not found")
            # Assert that the recipe has the expected keys
            expected_keys = ['id', 'name', 'description', 'category', 'cuisine', 'instructions', 'ingredients', 'image', 'date_published', 'rating']
            self.assertListEqual(list(recipe.keys()), expected_keys)

            #assert specific properties of the recipe
            self.assertEqual(recipe['id'], recipe_id)
            self.assertEqual(recipe['name'], 'Blueberry Pancake')
            self.assertEqual(recipe['category'], 'Breakfast')
    
    #View All Recipes
    def test_view_all_recipes(self):
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
            reps = len(recipedata)
        with self.app.test_request_context('/', method='GET'):
            # Call the load_recipes_from_json function to get all recipes
            recipes = functions.load_recipes_from_json('test_recipe.json')
            # Assert that there are recipes available
            # print("The total is",reps)
            # print("the length of recipes",len(recipes))
            self.assertTrue(len(recipes) == reps)    

            # Assert that each recipe has the expected keys
            expected_keys = ['id', 'name', 'description', 'category', 'cuisine', 'instructions', 'ingredients', 'image', 'date_published', 'rating']
            for recipe in recipes:
                self.assertListEqual(list(recipe.keys()), expected_keys)
                
            # Add additional assertions
            # assert specific properties of the recipes
            for recipe in recipes:
                self.assertIsNotNone(recipe['id'])
                self.assertIsNotNone(recipe['name'])
                self.assertIsNotNone(recipe['category'])

    #Add Recipe
    def test_add_recipe_success(self):
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))
        # with open('test_recipe.json', 'r') as file:
        #     recipedata = json.load(file)
        data = {
            'name': 'Test Recipes '+random_string,
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

    def test_add_recipe_missing(self):
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))
        # with open('test_recipe.json', 'r') as file:
        #     recipedata = json.load(file)
        data = {
            'name': 'Test Recipes '+random_string,
            'description': 'Test description',
            'category': 'Test category',
            'cuisine': '',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }
        with self.app.test_request_context('/addrecipe', method='POST', data=data, content_type='multipart/form-data'):
            result = functions.add_recipe_function('test_recipe.json')
            self.assertEqual(result, 'All fields are required!')
            
    def test_add_recipe_existing(self):
        # with open('test_recipe.json', 'r') as file:
        #     recipedata = json.load(file)
        data = {
            'name': 'Blueberry Pancake',
            'description': 'Test description',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }
        with self.app.test_request_context('/addrecipe', method='POST', data=data, content_type='multipart/form-data'):
            result = functions.add_recipe_function('test_recipe.json')
            self.assertEqual(result, 'Recipe already exists.')

    #search recipe testing
    def test_search_recipe(self):
        # request query
        query = 'butter chicken'

        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
            
        with self.app.test_request_context('/search', method='GET'):
            # Call the add_recipe_function()
            result_recipes = functions.search_recipe_function('test_recipe.json',query,recipedata)
            # Assert the expected result
            # self.assertEqual(query, query)
            self.assertEqual(len(result_recipes), 1)
            self.assertEqual(result_recipes[0]['name'], 'Butter Chicken')

   
    #edit recipe 
    def test_edit_recipe_success(self):
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
            with self.app.test_request_context('/editrecipe/1',method='POST', data=data, content_type='multipart/form-data'):
                # Call the add_recipe_function()
                result = functions.edit_recipe_function(1,data,'test_recipe.json',TEST_UPLOAD_FOLDER,recipes)
                # Assert the expected result
                self.assertEqual(result, 'Updated Successfully')

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
                # self.assertIsNone(result)
                self.assertEqual(result, 'Recipe not found.')
                
    #delete recipe
    def test_delete_recipe_success(self):
        test_recipe_id = 20
        test_recipe_filename = 'test_recipe.json'

        with open(test_recipe_filename, 'r') as file:
            recipedata = json.load(file)

        data = {
            'id':20,
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
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)

        response = functions.export_recipes(UPLOAD_FOLDER,recipedata)
        # Assert the expected result
        self.assertIsNotNone(response)
        
    def test_rating_success(self):
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
        rec = {
                'id':20,
                'name': 'Blueberry Pancake',
                'description': 'Delicious blueberry pancakes recipe',
                'category': 'Breakfast',
                'cuisine': 'American',
                'instructions': 'Step 1. Step 2. Step 3.',
                'ingredients': 'flour, milk, eggs, blueberries',
                'image': 'test_pancake.jpeg',
                'date_published':'2022-05-10',
                'rating':0
            }        
        recipedata.append(rec)
        with open('test_recipe.json', 'w') as file:
            json.dump(recipedata, file)
        data = {'rating':3}
        with self.app.test_request_context('/rating/20',method='POST',data=data):
            result = functions.rating('test_recipe.json',20)
            self.assertEqual(result['rating'],'3')
            functions.delete_recipe('test_recipe.json', 20)

    def test_rating_unsuccessful(self):
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
        rec = {
                'id':20,
                'name': 'Blueberry Pancake',
                'description': 'Delicious blueberry pancakes recipe',
                'category': 'Breakfast',
                'cuisine': 'American',
                'instructions': 'Step 1. Step 2. Step 3.',
                'ingredients': 'flour, milk, eggs, blueberries',
                'image': 'test_pancake.jpeg',
                'date_published':'2022-05-10',
                'rating':2
            }        
        recipedata.append(rec)
        with open('test_recipe.json', 'w') as file:
            json.dump(recipedata, file)
        data = {'rating':3}
        with self.app.test_request_context('/rating/20',method='POST',data=data):
            result = functions.rating('test_recipe.json',20)
            self.assertEqual(result,'Recipe already rated.')
            functions.delete_recipe('test_recipe.json', 20)
            

    #import recipe from a csv file
    def test_import__csv_recipe(self):
        # Prepare a test CSV file
        csv_file = FileStorage(filename='test_recipes.csv', content_type='application/vnd.ms-excel')
        
        #Specify the folder the imported file be saved to
        UPLOAD_FOLDER2 = './test_files/import/'
        
        #Specify JSON file
        json_file = 'test_recipe.json'

        with open(json_file, 'r') as file:
            recipes = json.load(file)
            
        initial_recipe_count = len(recipes)
            
        #Save all the recipes in an expected data file
        with open('./test_files/import/expected_data.json', 'w') as file:
            json.dump(recipes, file, indent=4)
            
        # Call the import_recipe function
        functions.import_recipe(csv_file, json_file, UPLOAD_FOLDER2)
        
        with open('./test_files/import/expected_data.json', 'r+') as file:
            expected_recipes = json.load(file)   
            
        final_recipe_count = len(expected_recipes)    
        
        total_recipes_imported = final_recipe_count - initial_recipe_count

        self.assertEqual(final_recipe_count, initial_recipe_count + total_recipes_imported)
        
    # #import recipe from a xlsx file
    # def test_import__xlsx_recipe(self):
    #     # Prepare a test CSV file
    #     csv_file = FileStorage(filename='test_recipes.xlsx', content_type='application/vnd.ms-excel')
        
    #     #Specify the folder the imported file be saved to
    #     UPLOAD_FOLDER2 = './test_files/import/'
        
    #     json_file = 'test_recipe.json'

    #     with open(json_file, 'r') as file:
    #         recipes = json.load(file)
            
    #     with open('./test_files/import/expected_data.json', 'w') as file:
    #         json.dump(recipes, file, indent=4)
            
    #     csv_file.save(os.path.join(UPLOAD_FOLDER2, csv_file.filename))

    #     # Call the import_recipe function
    #     functions.import_recipe(csv_file, json_file, UPLOAD_FOLDER2)
        
    #     with open('./test_files/import/expected_data.json', 'r+') as file:
    #         expected_recipes = json.load(file)       

    #     self.assertEqual(recipes, expected_recipes)

if __name__ == '__main__':
    unittest.main()
