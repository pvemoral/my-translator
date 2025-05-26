import unittest
import json
import azure.functions as func

# Assuming 'src' is a top-level package in the PYTHONPATH for tests
# (e.g. tests are run from project root)
from src.builders.response_builder import JsonResponseBuilder

class TestJsonResponseBuilder(unittest.TestCase):

    def test_build_success_response(self):
        builder = JsonResponseBuilder()
        response = (builder
                    .with_status_code(200)
                    .with_success_payload("Hello", "Test")
                    .build())

        self.assertIsInstance(response, func.HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.headers["Content-Type"], "application/json")
        
        expected_body = {"message": "Hello", "status": "success", "name": "Test"}
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_build_error_response(self):
        builder = JsonResponseBuilder()
        response = (builder
                    .with_status_code(400)
                    .with_error_payload("Err Summary", "Err Message")
                    .build())

        self.assertIsInstance(response, func.HttpResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.headers["Content-Type"], "application/json")

        expected_body = {"error": "Err Summary", "message": "Err Message"}
        self.assertEqual(json.loads(response.get_body()), expected_body)

    def test_build_with_custom_header(self):
        builder = JsonResponseBuilder()
        response = (builder
                    .with_status_code(201)
                    .with_header("X-Custom", "Value")
                    .with_success_payload("Created", "Resource") # Body needed for valid response
                    .build())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers["X-Custom"], "Value")
        # Default Content-Type should still be applied
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.mimetype, "application/json")

    def test_build_raises_value_error_if_status_not_set(self):
        builder = JsonResponseBuilder()
        # Test with success payload
        with self.assertRaises(ValueError) as context_success:
            builder.with_success_payload("Hi", "There").build()
        self.assertEqual(str(context_success.exception), "Status code must be set before building the response.")

        # Test with error payload (reset builder or use new one for clarity)
        builder_error = JsonResponseBuilder() 
        with self.assertRaises(ValueError) as context_error:
            builder_error.with_error_payload("Error", "Msg").build()
        self.assertEqual(str(context_error.exception), "Status code must be set before building the response.")

    def test_payload_methods_chainable(self):
        builder = JsonResponseBuilder()

        # Test with_status_code chainability
        self.assertIs(builder.with_status_code(200), builder, "with_status_code should be chainable")

        # Test with_header chainability
        self.assertIs(builder.with_header("X-Test", "TestValue"), builder, "with_header should be chainable")

        # Test with_success_payload chainability
        self.assertIs(builder.with_success_payload("Msg", "Name"), builder, "with_success_payload should be chainable")

        # Test with_error_payload chainability
        # Create a new builder instance for a clean test of with_error_payload
        builder_for_error = JsonResponseBuilder()
        self.assertIs(builder_for_error.with_error_payload("Err", "Msg"), builder_for_error, "with_error_payload should be chainable")

    def test_override_content_type_header(self):
        builder = JsonResponseBuilder()
        response = (builder
                    .with_status_code(415)
                    .with_header("Content-Type", "application/xml")
                    .with_error_payload("Unsupported Media", "Payload should be XML, not JSON") # Body needed
                    .build())

        self.assertEqual(response.status_code, 415)
        # The custom Content-Type header should override the default
        self.assertEqual(response.headers["Content-Type"], "application/xml")
        # The mimetype is set by the builder to "application/json" regardless of the Content-Type header override.
        # This confirms the builder's behavior: it sets mimetype based on its assumption of building JSON responses.
        self.assertEqual(response.mimetype, "application/json")

if __name__ == '__main__':
    unittest.main()
