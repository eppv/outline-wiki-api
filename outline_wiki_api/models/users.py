from datetime import datetime
from outline_wiki_api.base import EntityCollection


class Users(EntityCollection):
    _path: str = 'users'


class User:
    id: str
    name: str
    avatar_url: str
    email: str
    color: str
    role: str
    is_suspended: bool
    last_active_at: datetime
    created_at: datetime
