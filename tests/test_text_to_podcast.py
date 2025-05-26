import unittest
import json
from unittest.mock import Mock
import azure.functions as func

# Import the function to be tested
from TextToPodcast.__init__ import main

class TestTextToPodcast(unittest.TestCase):

    def test_successful_request(self):
        # Mock HttpRequest
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = {"name": "Test User"}

        # Call the function
        response = main(req)

        # Assertions
        self.assertEqual(response.status_code, 200)
        expected_body = {
            "message": "Hello, Test User! Welcome to My Translator service.",
            "status": "success",
            "name": "Test User"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_missing_request_body(self):
        # Mock HttpRequest
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = None

        # Call the function
        response = main(req)

        # Assertions
        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Request body is required",
            "message": "Please provide a JSON body with a 'name' field"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_missing_name_field(self):
        # Mock HttpRequest
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = {"other_field": "some_value"}

        # Call the function
        response = main(req)

        # Assertions
        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Missing required field",
            "message": "The 'name' field is required in the JSON body"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_empty_name_field(self):
        # Mock HttpRequest
        req = Mock(spec=func.HttpRequest)
        req.get_json.return_value = {"name": "   "}

        # Call the function
        response = main(req)

        # Assertions
        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Invalid name",
            "message": "The 'name' field cannot be empty"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_invalid_json_body(self):
        # Mock HttpRequest
        req = Mock(spec=func.HttpRequest)
        req.get_json.side_effect = json.JSONDecodeError("Error", "doc", 0)

        # Call the function
        response = main(req)

        # Assertions
        self.assertEqual(response.status_code, 400)
        expected_body = {
            "error": "Invalid JSON",
            "message": "Request body must be valid JSON"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_unexpected_error(self):
        # Mock HttpRequest
        req = Mock(spec=func.HttpRequest)
        req.get_json.side_effect = Exception("Unexpected error")

        # Call the function
        response = main(req)

        # Assertions
        self.assertEqual(response.status_code, 500)
        expected_body = {
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

if __name__ == '__main__':
    unittest.main()
