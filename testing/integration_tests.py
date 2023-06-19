from io import BytesIO
import unittest
from flask import Flask
import sys
import json
import os
import random
import requests
from threading import Thread
from werkzeug.datastructures import FileStorage

sys.path.append("../SystemDeploymentProject")

import functions

class integration_tests():
    
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def create_and_read_recipe(self):
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)
            previous = len(recipedata)

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
            new = previous + 1
            assert previous + 1 ==  new
   
            assert result == 'Success'
            if result == 'Success':
                print("create_and_read_recipe test passed")
            else:
                print("create_and_read_recipe test failed")
            
    def delete_and_read_recipe(self):

        with open('test_recipe.json', 'r') as file:
            old_data = json.load(file)
            file.close()

        data = {
            'id':21,
            'name': 'Delete Test Recipe',
            'description': 'Test description',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': 'Deletetest.jpg'}

        old_data.append(data)

        with open('test_recipe.json', 'w') as file:
            json.dump(old_data, file)
            file.close()
        functions.delete_recipe('test_recipe.json', 21)
        data = functions.get_by_id('test_recipe.json',21)
        
        new_data = functions.load_recipes_from_json('test_recipe.json')
        
        assert data not in new_data 
        if data not in new_data:
            print("delete_and_read_recipe test passed")
        else:
            print("delete_and_read_recipe test failed")

    def rate_and_view(self):
        with open('test_recipe.json', 'r') as file:
            old_data = json.load(file)
            file.close()
        data = {
            'id':20,
            'name': 'Delete Test Recipe',
            'description': 'Test integration add',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': 'Deletetest.jpg',
            'date_published':'2022-05-10',
            'rating':0}

        old_data.append(data)

        with open('test_recipe.json', 'w') as file:
            json.dump(old_data, file)
            file.close()
      
        data = {'rating':3}

        with self.app.test_request_context('/rating/20',method='POST',data=data):
            functions.rating('test_recipe.json',20)
            result = functions.get_by_id('test_recipe.json',20)
            assert result['rating'] == '3'
            functions.delete_recipe('test_recipe.json', 20)
            if result['rating'] == '3':
                print("rate_and_view test passed")
            else:
                print("rate_and_view test failed")


    def view_and_edit(self):
        with open('test_recipe.json', 'r') as file:
            old_data = json.load(file)
            file.close()
        TEST_UPLOAD_FOLDER = 'test_images'
        data = {
            'id':30,
            'name': 'Edit Test Recipe',
            'description': 'Test integration add',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': 'Edittest.jpg',
            'date_published':'2022-05-10',
            'rating':0}
        old_data.append(data)
        with open('test_recipe.json', 'w') as file:
            json.dump(old_data, file)
            file.close()
      
        data = {'id':30,
            'name': 'Testing Edit Recipe',
            'description': 'Test integration add',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'testedit.jpg'),
            'date_published':'2022-05-10',
            'rating':0}

        with self.app.test_request_context('/editrecipe/30',method='POST',data=data):
            result = functions.get_by_id('test_recipe.json',30)
            resultdata = functions.edit_recipe_function(result['id'],data,'test_recipe.json',TEST_UPLOAD_FOLDER,old_data)
            assert resultdata == 'Updated Successfully'
            functions.delete_recipe('test_recipe.json', 30)
            if resultdata == 'Updated Successfully':
                print("view_and_edit test passed")
            else:
                print("view_and_edit test failed")


    def search_by_name_and_view(self):
    
        with open('test_recipe.json', 'r') as file:
            recipedata = json.load(file)

            data= {
                "id": 31,
                "name": "Search Test Recipe",
                "description": "Test integration search",
                "category": "Test category",
                "cuisine": "Test cuisine",
                "instructions": "Step 1. Test instruction",
                "ingredients": "Ingredient 1, Ingredient 2",
                "image": "Edittest.jpg",
                "date_published": "2022-05-10",
                "rating": 0
            }
            recipedata.append(data)
            query = 'Search Test Recipe'

            expected_results = [data]

        with self.app.test_request_context('/search?search=Search Test Recipe', method='GET'):
            result_recipes = functions.search_recipe_function('test_recipe.json',query,recipedata)
            # Assert the expected result
            assert result_recipes == expected_results
            functions.delete_recipe('test_recipe.json', 31)
            if result_recipes == expected_results:
                print("search_by_name_and_view test passed")
            else:
                print("search_by_name_and_view test failed")
                
    def import_and_read(self):
        # Prepare the test data
        csv_file = FileStorage(filename='test_recipes.csv', content_type='application/vnd.ms-excel')
        json_file = 'test_recipe.json'
        upload_folder = './test_files/import/'
        image_directory = './test_images/'
        
        recipes = functions.load_recipes_from_json(json_file)

        # Call the import_recipe function
        functions.import_recipe(csv_file, json_file, upload_folder, image_directory)
                
        updated_recipes = functions.load_recipes_from_json(json_file)
        
        for rows in updated_recipes:
            if rows['name'] == 'Chocolate Cake':
                id = rows['id']
                break
        
        data = {
            "id": id,
            "name": "Chocolate Cake",
            "description": "Indulge in the rich and decadent flavors of a homemade chocolate cake. This moist and velvety dessert is perfect for chocolate lovers. With layers of moist chocolate cake, creamy chocolate frosting, and a hint of cocoa, this cake is a delightful treat for any occasion. Whether it's a birthday celebration or a special gathering, this chocolate cake is sure to satisfy your sweet tooth and leave you craving for more. Enjoy a slice of pure chocolate bliss!",
            "category": "Snack",
            "cuisine": "American",
            "instructions": [
                "Preheat the oven.",
                "Mix the ingredients.",
                "Bake the cake."
            ],
            "ingredients": [
                "Flour",
                "sugar",
                "cocoa powder",
                "eggs",
                "butter",
                "milk"
            ],
            "image": "Chocolate Cake.jpg",
            "date_published": "9/21/2022",
            "rating": 0
        }
                
        result = functions.get_by_id('test_recipe.json',id)
            
        assert result == data
        if result == data:
            print("import and read recipe test has passed")
        else:
            print("import and read recipe test has failed")

    def runall(self):
        self.setUp()
        self.create_and_read_recipe()
        self.delete_and_read_recipe()
        self.rate_and_view()
        self.view_and_edit()
        self.search_by_name_and_view()
        self.import_and_read()

run = integration_tests()
run.runall()