import json
import azure.functions as func
from datetime import datetime
from typing import Optional, Dict, Any

class JsonResponseBuilder:
    """
    A builder class for creating Azure Function HTTP responses with JSON payloads
    that include request information.
    """
    def __init__(self):
        """
        Initializes the JsonResponseBuilder with default empty values.
        """
        self._body_dict = {}
        self._headers = {}
        self._status_code = None
        self._request_info = {}

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

    def with_request_info(self, req: func.HttpRequest) -> 'JsonResponseBuilder':
        """
        Captures information from the HTTP request.

        Args:
            req (func.HttpRequest): The Azure Functions HTTP request object.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._request_info = {
            "method": req.method,
            "url": req.url,
            "headers": dict(req.headers),
            "params": dict(req.params),
            "route_params": dict(req.route_params) if req.route_params else {},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Incluir el body si es POST/PUT/PATCH
        if req.method.upper() in ['POST', 'PUT', 'PATCH']:
            try:
                body_json = req.get_json()
                if body_json:
                    self._request_info["body"] = body_json
            except:
                # Si no es JSON válido, capturar como string
                try:
                    body_text = req.get_body().decode('utf-8')
                    if body_text:
                        self._request_info["body"] = body_text
                except:
                    self._request_info["body"] = None
        
        return self

    def with_success_payload(self, message: str, data: Any = None) -> 'JsonResponseBuilder':
        """
        Sets the response body for a successful operation.

        Args:
            message (str): The success message.
            data (Any): Optional data to include in the response.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._body_dict = {
            "status": "success",
            "message": message,
            "data": data,
            "request": self._request_info,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return self

    def with_error_payload(self, error_summary: str, error_message: str, error_code: str = None) -> 'JsonResponseBuilder':
        """
        Sets the response body for an error.

        Args:
            error_summary (str): A summary of the error.
            error_message (str): A detailed message about the error.
            error_code (str): Optional error code for categorization.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._body_dict = {
            "status": "error",
            "error": {
                "summary": error_summary,
                "message": error_message,
                "code": error_code
            },
            "request": self._request_info,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return self

    def with_custom_payload(self, payload: Dict[str, Any]) -> 'JsonResponseBuilder':
        """
        Sets a completely custom payload while still including request info.

        Args:
            payload (Dict[str, Any]): Custom payload dictionary.

        Returns:
            JsonResponseBuilder: The instance of the builder.
        """
        self._body_dict = {
            **payload,
            "request": self._request_info,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        return self

    def build(self) -> func.HttpResponse:
        """
        Builds and returns the func.HttpResponse object with JSON including request info.

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
            body=json.dumps(self._body_dict, indent=2),
            status_code=self._status_code,
            headers=self._headers,
            mimetype="application/json"
        )