from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..websites.websites_model import Website

def format_response(data):
    """Format the response data for success and error messages."""
    # If `data` is a serializer instance, return its serialized data.
    if isinstance(data, serializers.ModelSerializer):
        return data.data

    # If `data` is a list of serializer instances, return serialized data for each.
    elif isinstance(data, list) and all(isinstance(item, serializers.ModelSerializer) for item in data):
        return [item.data for item in data]

    # If `data` is an object with a `to_dict()` method, call it and return the result.
    elif hasattr(data, 'to_dict') and callable(data.to_dict):
        return data.to_dict()

    # Otherwise, return the data as-is.
    return data

def success_response(data, code):
    """Return a success response with a success indicator."""
    formatted_data = format_response(data=data)
    
    # Ensure formatted_data is a dictionary or convert it to one
    if not isinstance(formatted_data, dict):
        formatted_data = {"data": formatted_data}  # Wrap it in a dictionary if not already one
    
    response_data = {
        'success': 1,
        **formatted_data  # Safely unpack
    }

    return Response(response_data, status=code)

def error_response(message, errors=None, code=status.HTTP_400_BAD_REQUEST):
    """Return an error response with a message and optional errors."""
    response_data = {
        'error': 1,
        'message': message
    }
    if errors:
        response_data['errors'] = errors
    return Response(response_data, status=code)

def check_for_website(web_id: int):
    """Check if the website exists by web_id."""
    try:
        return Website.objects.get(id=web_id)
    except Website.DoesNotExist:
        return None
    
def get_valid_website(data):
    """Validate website ID and retrieve the corresponding Website object.
    
    Returns:
        Website or error_response: The Website object if valid, or an error response.
    """
    web_id = data.get('web_id')
    if not web_id:
        return error_response("Website ID is required", code=status.HTTP_400_BAD_REQUEST)

    website = check_for_website(web_id)
    if website is None:
        return error_response("Website not found", code=status.HTTP_404_NOT_FOUND)

    return website
