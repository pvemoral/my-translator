import logging
import json
import azure.functions as func
from builders.response_builder import JsonResponseBuilder


app = func.FunctionApp()
@app.function_name(name="text_to_podcast")
@app.route(route="text-to-podcast", methods=["POST"])
def textToPodcast(req: func.HttpRequest) -> func.HttpResponse:
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
            return (JsonResponseBuilder()
                    .with_status_code(400)
                    .with_error_payload("Request body is required", "Please provide a JSON body with a 'name' field")
                    .build())
        
        # Extract the name from the request
        name = req_body.get('name')
        
        if not name:
            return (JsonResponseBuilder()
                    .with_status_code(400)
                    .with_error_payload("Missing required field", "The 'name' field is required in the JSON body")
                    .build())
        
        # Validate name is not empty
        if not name.strip():
            return (JsonResponseBuilder()
                    .with_status_code(400)
                    .with_error_payload("Invalid name", "The 'name' field cannot be empty")
                    .build())
        
        # Create response message
        response_message = f"Hello, {name.strip()}! Welcome to My Translator service."
        
        # Log successful processing
        logging.info(f'Successfully processed request for name: {name}')
        
        # Return success response
        return (JsonResponseBuilder()
                .with_status_code(200)
                .with_success_payload(response_message, name.strip())
                .build())
        
    except json.JSONDecodeError:
        logging.error('Invalid JSON in request body')
        return (JsonResponseBuilder()
                .with_status_code(400)
                .with_error_payload("Invalid JSON", "Request body must be valid JSON")
                .build())
        
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
        return (JsonResponseBuilder()
                .with_status_code(500)
                .with_error_payload("Internal server error", "An unexpected error occurred while processing your request")
                .build())
