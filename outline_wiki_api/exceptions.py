from typing import Optional


class OutlineError(Exception):
    """Base exception for Outline API errors"""


class OutlineAPIError(OutlineError):
    """Generic API error"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class OutlineAuthenticationError(OutlineAPIError):
    """Authentication failed"""


class OutlineNotFoundError(OutlineAPIError):
    """Resource not found"""


class OutlineRateLimitError(OutlineAPIError):
    """Rate limit exceeded"""
