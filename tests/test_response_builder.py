import unittest
import json
import azure.functions as func

# Adjust the import path if necessary based on how tests are run.
# Assuming 'TextToPodcast' is a top-level package in thePYTHONPATH
from TextToPodcast.builders.response_builder import JsonResponseBuilder

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
                    .with_header("X-Custom-Header", "CustomValue")
                    .with_success_payload("Created", "Resource") # Needs a payload for body
                    .build())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers["X-Custom-Header"], "CustomValue")
        self.assertEqual(response.headers["Content-Type"], "application/json") # Default should still be there
        self.assertEqual(response.mimetype, "application/json")


    def test_build_raises_value_error_if_status_not_set(self):
        builder = JsonResponseBuilder()
        with self.assertRaises(ValueError) as context:
            builder.with_success_payload("Hi", "There").build()
        
        self.assertEqual(str(context.exception), "Status code must be set before building the response.")

        builder_for_error = JsonResponseBuilder()
        with self.assertRaises(ValueError) as context_error:
            builder_for_error.with_error_payload("Error", "Msg").build()

        self.assertEqual(str(context_error.exception), "Status code must be set before building the response.")


    def test_override_content_type_header(self):
        builder = JsonResponseBuilder()
        response = (builder
                    .with_status_code(415)
                    .with_header("Content-Type", "application/xml")
                    .with_error_payload("Unsupported Media", "Payload should be XML")
                    .build())

        self.assertEqual(response.status_code, 415)
        # The custom header should override the default Content-Type
        self.assertEqual(response.headers["Content-Type"], "application/xml")
        # Mimetype is set by the builder based on its own logic, might not reflect overridden header
        self.assertEqual(response.mimetype, "application/json") 
        # This ^ assertion confirms the note in the task: mimetype is set independently by the builder.


    def test_payload_methods_chainable(self):
        builder = JsonResponseBuilder()
        # Test with_status_code chainability
        chained_builder = builder.with_status_code(200)
        self.assertIsInstance(chained_builder, JsonResponseBuilder)
        self.assertIs(chained_builder, builder) # Check if it returns self

        # Test with_header chainability
        chained_builder = builder.with_header("X-Test", "TestValue")
        self.assertIsInstance(chained_builder, JsonResponseBuilder)
        self.assertIs(chained_builder, builder)

        # Test with_success_payload chainability
        chained_builder = builder.with_success_payload("Msg", "Name")
        self.assertIsInstance(chained_builder, JsonResponseBuilder)
        self.assertIs(chained_builder, builder)

        # Test with_error_payload chainability
        # Re-initialize for a clean state if needed, though it's fine for this test
        builder_error = JsonResponseBuilder() 
        chained_builder_error = builder_error.with_error_payload("Err", "Msg")
        self.assertIsInstance(chained_builder_error, JsonResponseBuilder)
        self.assertIs(chained_builder_error, builder_error)

if __name__ == '__main__':
    unittest.main()
