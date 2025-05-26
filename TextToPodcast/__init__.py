import logging
import json
import azure.functions as func


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
            return func.HttpResponse(
                json.dumps({
                    "error": "Request body is required",
                    "message": "Please provide a JSON body with a 'name' field"
                }),
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
        
        # Extract the name from the request
        name = req_body.get('name')
        
        if not name:
            return func.HttpResponse(
                json.dumps({
                    "error": "Missing required field",
                    "message": "The 'name' field is required in the JSON body"
                }),
                status_code=400,
                headers={"Content-Type": "application/json"}
            )
        
        # Validate name is not empty
        if not name.strip():
            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid name",
                    "message": "The 'name' field cannot be empty"
                }),
                status_code=400,
                headers={"Content-Type": "application/json"}
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
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid JSON",
                "message": "Request body must be valid JSON"
            }),
            status_code=400,
            headers={"Content-Type": "application/json"}
        )
        
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "message": "An unexpected error occurred while processing your request"
            }),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
