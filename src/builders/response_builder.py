import json
import azure.functions as func

class JsonResponseBuilder:
    """
    A builder class for creating Azure Function HTTP responses with JSON payloads.
    """
    def __init__(self):
        """
        Initializes the JsonResponseBuilder with default empty values.
        """
        self._body_dict = {}
        self._headers = {}
        self._status_code = None

    def with_status_code(self, status_code: int) -> 'JsonResponseBuilder':
        """
        Sets the HTTP status code for the response.

        Args:
            status_code (int): The HTTP status code.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._status_code = status_code
        return self

    def with_header(self, key: str, value: str) -> 'JsonResponseBuilder':
        """
        Adds or updates a header for the response.

        Args:
            key (str): The header key.
            value (str): The header value.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._headers[key] = value
        return self

    def with_success_payload(self, greeting: str, name_provided: str) -> 'JsonResponseBuilder':
        """
        Sets the response body for a successful operation.

        Args:
            greeting (str): The greeting message.
            name_provided (str): The name that was provided in the request.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._body_dict = {
            "message": greeting,
            "status": "success",
            "name": name_provided
        }
        return self

    def with_error_payload(self, error_summary: str, error_message: str) -> 'JsonResponseBuilder':
        """
        Sets the response body for an error.

        Args:
            error_summary (str): A summary of the error.
            error_message (str): A detailed message about the error.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._body_dict = {
            "error": error_summary,
            "message": error_message
        }
        return self

    def build(self) -> func.HttpResponse:
        """
        Builds and returns the func.HttpResponse object.

        Raises:
            ValueError: If the status code has not been set.

        Returns:
            func.HttpResponse: The constructed HTTP response.
        """
        if self._status_code is None:
            raise ValueError("Status code must be set before building the response.")

        # Ensure Content-Type is application/json if not already set
        self._headers.setdefault("Content-Type", "application/json")

        return func.HttpResponse(
            body=json.dumps(self._body_dict),
            status_code=self._status_code,
            headers=self._headers,
            mimetype="application/json"  # Ensure mimetype is also set for consistency
        )
