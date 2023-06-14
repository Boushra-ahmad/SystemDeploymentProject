from io import BytesIO
import unittest
from flask import Flask
import sys

sys.path.append("../SystemDeploymentProject")

import functions

class test_unit_routes(unittest.TestCase):
    # def test_add_recipe(self):
    #     app = Flask(__name__)
    #     app.config['TESTING'] = True

    #     with app.test_request_context('/addrecipe', method='POST', data={
    #         'name': 'Test 1',
    #         'description': 'Test',
    #         'category': 'Test',
    #         'cuisine': 'Test',
    #         'instructions': 'Test',
    #         'ingredients': '1, 2',
    #         'image': (BytesIO(b'TestImage'), 'test.jpg')
    #     }):
    #         response = functions.add_recipes()
    #         self.assertEqual(response.status_code, 200)

    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
           
    def test_add_recipe(self):

        with self.app.test_request_context('/addrecipe', method='POST', data={
            'name': 'Test Recipe',
            'description': 'Test description',
            'category': 'Test category',
            'cuisine': 'Test cuisine',
            'instructions': 'Step 1. Test instruction',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }, content_type='multipart/form-data'):
            # Call the add_recipe_function()
            result = functions.add_recipe_function()

            # Assert the expected result
            self.assertEqual(result, 'Success')


if __name__ == '__main__':
    unittest.main()