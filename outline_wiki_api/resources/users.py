from datetime import datetime
from .base import Resources


class Users(Resources):
    """
    `Users` represent an individual with access to the knowledge base. Users
    can be created automatically when signing in with SSO or when a user is
    invited via email.
    """
    _path: str = 'users'
