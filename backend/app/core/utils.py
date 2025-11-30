"""
Utility functions for the application.
"""
from typing import Any, Dict


def format_error_response(message: str, details: Any = None) -> Dict[str, Any]:
    """Format an error response."""
    response = {"error": message}
    if details:
        response["details"] = details
    return response

