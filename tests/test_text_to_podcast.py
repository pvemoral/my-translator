import unittest
import json
from unittest.mock import Mock
import azure.functions as func

# Import the function to be tested
from TextToPodcast.__init__ import main, _build_error_response

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

    # It's also good practice to test the helper function directly,
    # although it's indirectly tested by the main function tests.
    def test_build_error_response_helper(self):
        error_summary = "Test Error"
        error_message = "This is a test error message."
        status_code = 418  # I'm a teapot

        response = _build_error_response(error_summary, error_message, status_code)

        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.mimetype, "application/json")
        expected_body = {
            "error": error_summary,
            "message": error_message
        }
        self.assertEqual(json.loads(response.get_body()), expected_body)

if __name__ == '__main__':
    unittest.main()
