from typing import Any


def success_response(data: Any, message: str = "Success") -> dict:
    """Wraps any data in a standard success envelope."""
    return {
        "success": True,
        "message": message,
        "data":    data,
    }


def error_response(message: str, code: int = 400) -> dict:
    """Standard error envelope (used in custom error handlers)."""
    return {
        "success": False,
        "message": message,
        "code":    code,
    }
