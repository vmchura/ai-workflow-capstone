#!/usr/bin/env python
"""
api tests

these tests use the requests package however similar requests can be made with curl

e.g.

data = '{"key":"value"}'
curl -X POST -H "Content-Type: application/json" -d "%s" http://localhost:8080/predict'%(data)
"""

import sys
import os
import unittest
import requests
import re
from ast import literal_eval
import numpy as np

port = 8080

try:
    requests.post('http://127.0.0.1:{}/predict'.format(port))
    server_available = True
except:
    server_available = False
    
## test class for the main window function
class ApiTest(unittest.TestCase):
    """
    test the essential functionality
    """

    @unittest.skipUnless(server_available, "local server is not running")
    def test_01_train(self):
        """
        test the train functionality
        """
      
        request_json = {'mode':'test'}
        r = requests.post('http://127.0.0.1:{}/train'.format(port), json=request_json)
        train_complete = re.sub("\W+", "", r.text)
        self.assertEqual(train_complete, 'true')
    
    @unittest.skipUnless(server_available, "local server is not running")
    def test_02_predict_empty(self):
        """
        ensure appropriate failure types
        """
    
        ## provide no data at all 
        r = requests.post('http://127.0.0.1:{}/predict'.format(port))
        self.assertEqual(re.sub('\n|"', '', r.text), "[]")

        ## provide improperly formatted data
        r = requests.post('http://127.0.0.1:{}/predict'.format(port), json={"key":"value"})
        self.assertEqual(re.sub('\n|"', '', r.text),"[]")
    
    @unittest.skipUnless(server_available,"local server is not running")
    def test_03_predict(self):
        """
        test the predict functionality
        """

        query_data = {'country': 'all', 'year': '2018', 'month': '01', 'day': '05', 'model': 'sl'}

        query_type = 'dict'
        request_json = {'query':query_data, 'type':query_type, 'mode':'test'}

        r = requests.post('http://127.0.0.1:{}/predict'.format(port), json=request_json)
        response = literal_eval(r.text)

        for p in response['y_pred']:
            self.assertTrue(p > 0)

    @unittest.skipUnless(server_available, "local server is not running")
    def test_04_logs(self):
        """
        test the predict functionality
        """

        query_data = {'country': 'all', 'year': '2018', 'month': '01', 'day': '05', 'model': 'sl'}

        query_type = 'dict'
        request_json = {'query':query_data, 'type':query_type, 'mode':'test'}

        r = requests.post('http://127.0.0.1:{}/predict'.format(port), json=request_json)
        response = literal_eval(r.text)

        for p in response['y_pred']:
            self.assertTrue(p > 0)

        
### Run the tests
if __name__ == '__main__':
    unittest.main()
