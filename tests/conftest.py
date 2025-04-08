import pytest
from unittest.mock import Mock
from outline_wiki_api.client import Client
from outline_wiki_api.resources.auth import Auth

@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    client = Mock(spec=Client)
    return client

@pytest.fixture
def mock_response():
    """Create a mock response with common methods."""
    response = Mock()
    response.json.return_value = {"data": {}}
    return response

@pytest.fixture
def auth_resource(mock_client):
    """Create an Auth resource instance for testing."""
    return Auth(mock_client) 