import logging
import json
import azure.functions as func


def _build_error_response(error_summary: str, error_message: str, status_code: int) -> func.HttpResponse:
    """
    Builds an error HTTP response with a JSON body.

    Args:
        error_summary (str): A summary of the error.
        error_message (str): A detailed message about the error.
        status_code (int): The HTTP status code for the response.

    Returns:
        func.HttpResponse: The HTTP response object.
    """
    return func.HttpResponse(
        json.dumps({
            "error": error_summary,
            "message": error_message
        }),
        status_code=status_code,
        mimetype="application/json",  # Explicitly set mimetype
        headers={"Content-Type": "application/json"}
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that receives a POST request with a JSON containing a name
    and returns a greeting message.
    
    Expected JSON format:
    {
        "name": "John Doe"
    }
    
    Returns:
    {
        "message": "Hello, John Doe! Welcome to My Translator service."
    }
    """
    logging.info('Processing text-to-podcast request.')
    
    try:
        # Get the request body
        req_body = req.get_json()
        
        if not req_body:
            return _build_error_response(
                error_summary="Request body is required",
                error_message="Please provide a JSON body with a 'name' field",
                status_code=400
            )
        
        # Extract the name from the request
        name = req_body.get('name')
        
        if not name:
            return _build_error_response(
                error_summary="Missing required field",
                error_message="The 'name' field is required in the JSON body",
                status_code=400
            )
        
        # Validate name is not empty
        if not name.strip():
            return _build_error_response(
                error_summary="Invalid name",
                error_message="The 'name' field cannot be empty",
                status_code=400
            )
        
        # Create response message
        response_message = f"Hello, {name.strip()}! Welcome to My Translator service."
        
        # Log successful processing
        logging.info(f'Successfully processed request for name: {name}')
        
        # Return success response
        return func.HttpResponse(
            json.dumps({
                "message": response_message,
                "status": "success",
                "name": name.strip()
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
        
    except json.JSONDecodeError:
        logging.error('Invalid JSON in request body')
        return _build_error_response(
            error_summary="Invalid JSON",
            error_message="Request body must be valid JSON",
            status_code=400
        )
        
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
        return _build_error_response(
            error_summary="Internal server error",
            error_message="An unexpected error occurred while processing your request",
            status_code=500
        )
