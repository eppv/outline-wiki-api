from unittest.mock import Mock
from uuid import UUID
from outline_wiki_api.models.document import (
    Document,
    DocumentListResponse,
    DocumentResponse,
    DocumentSearchResultResponse,
    DocumentMoveResponse,
    DocumentUsersResponse,
)
from outline_wiki_api.models.response import Pagination, Sort


def test_info(documents_resource, mock_client, mock_document_data):
    """Test retrieving a document by ID."""
    # Setup
    doc_id = mock_document_data["data"]["id"]
    mock_response = Mock()
    mock_response.json.return_value = mock_document_data
    mock_client.request.return_value = mock_response
    print(mock_client.request)

    # Execute
    result = documents_resource.info(doc_id).data

    # Assert
    assert isinstance(result, Document)
    assert isinstance(result.id, UUID)
    assert result.title == "Test Document"
    mock_client.request.assert_called_once_with(
        method="POST",
        endpoint="/documents.info",
        params=None,
        data={"id": doc_id},
        files=None,
    )


def test_info_with_share_id(documents_resource, mock_client, mock_document_data):
    """Test retrieving a document by ID with share ID."""
    # Setup
    doc_id = mock_document_data["data"]["id"]
    share_id = "550e8400-e29b-41d4-a716-446655440000"
    mock_response = Mock()
    mock_document_data["data"]["id"] = share_id
    mock_response.json.return_value = mock_document_data
    mock_client.request.return_value = mock_response

    # Execute
    result = documents_resource.info(doc_id, share_id).data

    # Assert
    assert isinstance(result, Document)
    assert result.id == UUID(share_id)
    mock_client.request.assert_called_once_with(
        method="POST",
        endpoint="/documents.info",
        params=None,
        data={"id": doc_id, "shareId": str(share_id)},
        files=None,
    )


def test_export(documents_resource, mock_client):
    """Test exporting a document as markdown."""
    # Setup
    doc_id = "test-doc-id"
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": "# Test Content\n\nThis is a test document."
    }
    mock_client.request.return_value = mock_response

    # Execute
    result = documents_resource.export(doc_id)

    # Assert
    assert result == "# Test Content\n\nThis is a test document."
    mock_client.request.assert_called_once_with(
        method="POST",
        endpoint="/documents.export",
        params=None,
        data={"id": doc_id},
        files=None,
    )


def test_search(documents_resource, mock_client, mock_document_search_results_data):
    """Test searching documents."""
    # Setup
    query = "test query"
    collection_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    pagination = {"offset": 0, "limit": 10}

    mock_response = Mock()
    mock_response.json.return_value = mock_document_search_results_data
    mock_client.request.return_value = mock_response

    # Execute
    result = documents_resource.search(
        query=query,
        collection_id=collection_id,
        status_filter="published",
        date_filter="month",
        pagination=pagination,
    )

    # Assert
    assert isinstance(result, DocumentSearchResultResponse)
    assert len(result.data) == 1
    assert result.data[0].ranking == 0.95
    assert result.data[0].context == "This is a test document with the query term."
    assert result.data[0].document.title == "Test Document"
    mock_client.request.assert_called_once_with(
        method="POST",
        endpoint="/documents.search",
        params=None,
        data={
            "query": query,
            "collectionId": str(collection_id),
            "statusFilter": "published",
            "dateFilter": "month",
            "offset": 0,
            "limit": 10,
        },
        files=None,
    )


def test_users(documents_resource, mock_client):
    """Test listing users with access to a document."""
    # Setup
    doc_id = UUID("550e8400-e29b-41d4-a716-446655440000")
    query = "test"

    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 200,
        "ok": True,
        "data": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Test User 1",
                "email": "test1@example.com",
                "avatarUrl": "https://example.com/avatar1.jpg",
                "createdAt": "2023-01-15T09:30:00Z",
                "updatedAt": "2023-06-20T14:25:00Z",
                "isSuspended": False,
            },
            {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Test User 2",
                "email": "test2@example.com",
                "avatarUrl": "https://example.com/avatar2.jpg",
                "createdAt": "2023-01-15T09:30:00Z",
                "updatedAt": "2023-06-20T14:25:00Z",
                "isSuspended": False,
            },
        ],
        "pagination": {"offset": 0, "limit": 10, "total": 2},
        "policies": [],
    }
    mock_client.request.return_value = mock_response

    # Execute
    result = documents_resource.users(doc_id, query)

    # Assert
    assert isinstance(result, DocumentUsersResponse)
    assert len(result.data) == 2
    assert result.data[0].name == "Test User 1"
    assert result.data[1].name == "Test User 2"
    mock_client.request.assert_called_once_with(
        method="POST",
        endpoint="/documents.users",
        params=None,
        data={"id": str(doc_id), "query": query},
        files=None,
    )


def test_memberships(documents_resource, mock_client):
    """Test listing users with direct membership to a document."""
    # Setup
    doc_id = UUID("550e8400-e29b-41d4-a716-446655440000")
    query = "test"

    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 200,
        "ok": True,
        "data": {
            "users": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "Test User 1",
                    "email": "test1@example.com",
                    "avatarUrl": "https://example.com/avatar1.jpg",
                    "createdAt": "2023-01-15T09:30:00Z",
                    "updatedAt": "2023-06-20T14:25:00Z",
                    "isSuspended": False,
                }
            ],
            "memberships": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440002",
                    "userId": "550e8400-e29b-41d4-a716-446655440001",
                    "collectionId": "550e8400-e29b-41d4-a716-446655440000",
                    "permission": "read_write",
                    "createdAt": "2023-01-15T09:30:00Z",
                    "updatedAt": "2023-06-20T14:25:00Z",
                }
            ],
        },
        "pagination": {"offset": 0, "limit": 10, "total": 1},
        "policies": [],
    }
    mock_client.request.return_value = mock_response

    # Execute
    result = documents_resource.memberships(doc_id, query)

    # Assert
    assert result.status == 200
    assert result.ok is True
    assert len(result.data.users) == 1
    assert len(result.data.memberships) == 1
    assert result.data.users[0].name == "Test User 1"
    assert result.data.memberships[0].permission == "read_write"
    mock_client.request.assert_called_once_with(
        method="POST",
        endpoint="/documents.memberships",
        params=None,
        data={"id": str(doc_id), "query": query},
        files=None,
    )
