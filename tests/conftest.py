import pytest
from unittest.mock import Mock
from uuid import uuid4
from outline_wiki_api.client import Client
from outline_wiki_api.resources.auth import Auth
from outline_wiki_api.resources.documents import Documents
from outline_wiki_api.models.document import Document


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


@pytest.fixture
def documents_resource(mock_client):
    """Create a Documents resource instance for testing."""
    return Documents(mock_client)


# region Data


@pytest.fixture
def mock_document_data():
    """Create a Document json response for testing"""
    data = {
        "ok": True,
        "status": 200,
        "data": {
            "id": "36b0503e-ff65-428c-99f1-f5d2895523ef",
            "collectionId": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Test Document",
            "text": "# Test Content",
            "url": "https://example.com/test-doc",
            "urlId": "test-doc-1234567",  # At least 8 chars
            "revision": 1,
            "createdAt": "2023-01-15T09:30:00Z",
            "updatedAt": "2023-06-20T14:25:00Z",
            "publishedAt": "2023-06-20T14:25:00Z",
            "archivedAt": None,
            "deletedAt": None,
            "tasks": {"completed": 0, "total": 0},
            "icon": "📄",
            "createdBy": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Test User",
                "avatarUrl": "https://example.com/avatar.jpg",
                "email": "test@example.com",
                "isSuspended": False,
                "createdAt": "2023-01-15T09:30:00Z",
                "updatedAt": "2023-06-20T14:25:00Z",
            },
            "updatedBy": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Test User",
                "avatarUrl": "https://example.com/avatar.jpg",
                "email": "test@example.com",
                "isSuspended": False,
                "createdAt": "2023-01-15T09:30:00Z",
                "updatedAt": "2023-06-20T14:25:00Z",
            },
        },
        "pagination": {"offset": 0, "limit": 100, "total": 1},
        "policies": [{"id": str(uuid4()), "abilities": {"read": True, "write": True}}],
    }
    return data


@pytest.fixture
def mock_document_search_results_data(mock_document_data):
    """Create a Document import json response for testing"""
    data = {
        "ok": True,
        "status": 200,
        "data": [
            {
                "ranking": 0.95,
                "context": "This is a test document with the query term.",
                "document": Document(**mock_document_data["data"]),
            }
        ],
        "pagination": {"offset": 0, "limit": 10, "total": 1},
    }
    return data


# endregion Data
