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
   
    
     

if __name__ == '__main__':
    unittest.main()