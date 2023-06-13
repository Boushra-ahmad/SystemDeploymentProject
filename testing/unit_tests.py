from io import BytesIO
import unittest
from flask import Flask
import sys

sys.path.append("..")

# Import from the parent directory
from SystemDeploymentProject.routes import add_recipe


class test_unit_routes(unittest.TestCase):
    def test_add_recipe(self):
        app = Flask(__name__)
        app.config['TESTING'] = True

        with app.test_request_context('/addrecipe', method='POST', data={
            'name': 'Test 1',
            'description': 'Test',
            'category': 'Test',
            'cuisine': 'Test',
            'instructions': 'Test',
            'ingredients': '1, 2',
            'image': (BytesIO(b'TestImage'), 'test.jpg')
        }):
            response = add_recipe()
            self.assertEqual(response.status_code, 200)
           

if __name__ == '__main__':
    unittest.main()