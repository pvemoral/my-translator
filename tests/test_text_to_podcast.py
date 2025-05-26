import unittest
import json
from unittest.mock import Mock
import azure.functions as func

# Assuming 'src' is a top-level package in the PYTHONPATH for tests
from src.__init__ import main

class TestMainFunction(unittest.TestCase):

    def test_successful_request(self):
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = {"name": "Test User"}

        response = main(req)

        self.assertEqual(response.status_code, 200)
        expected_body = {
            "message": "Hello, Test User! Welcome to My Translator service.",
            "status": "success",
            "name": "Test User"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_missing_request_body(self):
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = None # Simulate empty body or failure to parse

        response = main(req)

        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Request body is required",
            "message": "Please provide a JSON body with a 'name' field"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_missing_name_field(self):
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = {"other_field": "some_value"}

        response = main(req)

        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Missing required field",
            "message": "The 'name' field is required in the JSON body"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_empty_name_field(self):
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = {"name": "   "} # Name with only whitespace

        response = main(req)

        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Invalid name",
            "message": "The 'name' field cannot be empty"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_invalid_json_body(self):
        req = Mock(spec=func.HttpRequest)
        # Simulate JSONDecodeError when .get_json() is called
        req.get_json.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)

        response = main(req)

        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Invalid JSON",
            "message": "Request body must be valid JSON"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_unexpected_error(self):
        req = Mock(spec=func.HttpRequest)
        # Simulate a generic exception during the processing.
        # Mocking .get_json() to return a dictionary, then .get() on that dict to raise an Exception.
        # This simulates an error after successfully getting JSON but during its processing.
        mock_dict = Mock(spec=dict)
        mock_dict.get.side_effect = Exception("A very unexpected error occurred")
        req.get_json.return_value = mock_dict
        
        response = main(req)

        self.assertEqual(response.status_code, 500)
        expected_body = {
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

if __name__ == '__main__':
    unittest.main()
