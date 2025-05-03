from unittest.mock import Mock
from uuid import uuid4
from outline_wiki_api.models.auth import AuthResponse
from outline_wiki_api.models.user import User
from outline_wiki_api.models.team import Team


def test_info(auth_resource, mock_client):
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "status": 200,
        "data": {
            "user": {
                "id": str(uuid4()),
                "name": "Test User",
                "email": "test@example.com",
                "avatarUrl": "https://example.com/avatar.jpg",
                "isSuspended": False,
                "createdAt": "2023-01-01T00:00:00Z",
                "updatedAt": "2023-01-01T00:00:00Z"
            },
            "team": {
                "id": str(uuid4()),
                "name": "Test Team",
                "sharing": True,
                "memberCollectionCreate": True,
                "memberTeamCreate": False,
                "documentEmbeds": True,
                "guestSignin": False,
                "inviteRequired": True,
                "url": "https://app.getoutline.com"
            },
            "groups": [],
            "groupUsers": [],
            "collaborationToken": "collab_token",
            "availableTeams": []
        },
        "pagination": {
            "offset": 0,
            "limit": 100,
            "total": 1
        },
        "policies": [
            {
                "id": str(uuid4()),
                "abilities": {"read": True, "write": True}
            }
        ]
    }
    mock_client.request.return_value = mock_response

    # Test info
    response = auth_resource.info()
    assert isinstance(response, AuthResponse)
    assert response.ok is True
    assert response.status == 200
    assert isinstance(response.data.user, User)
    assert isinstance(response.data.team, Team)
    assert response.data.collaboration_token == "collab_token"
    
    mock_client.request.assert_called_with(
        method="POST",
        endpoint="/auth.info",
        data=None,
        params=None,
        files=None
    )


def test_config(auth_resource, mock_client):
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "status": 200,
        "data": {
            "providers": ["google", "slack"],
            "emailSignin": True,
            "googleSignin": True,
            "slackSignin": True
        }
    }
    mock_client.request.return_value = mock_response

    # Test config
    response = auth_resource.config()
    assert response.ok is True
    assert response.status == 200
    assert "providers" in response.json()["data"]
    assert "emailSignin" in response.json()["data"]
    
    mock_client.request.assert_called_with(
        method="POST",
        endpoint="/auth.config",
        data=None,
        params=None,
        files=None
    )


def test_get_current_user(auth_resource, mock_client):
    # Setup mock response for info method
    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "status": 200,
        "data": {
            "user": {
                "id": str(uuid4()),
                "name": "Test User",
                "email": "test@example.com",
                "avatarUrl": "https://example.com/avatar.jpg",
                "isSuspended": False,
                "createdAt": "2023-01-01T00:00:00Z",
                "updatedAt": "2023-01-01T00:00:00Z"
            },
            "team": {
                "id": str(uuid4()),
                "name": "Test Team",
                "sharing": True,
                "memberCollectionCreate": True,
                "memberTeamCreate": False,
                "documentEmbeds": True,
                "guestSignin": False,
                "inviteRequired": True,
                "url": "https://app.getoutline.com"
            },
            "groups": [],
            "groupUsers": [],
            "collaborationToken": "collab_token",
            "availableTeams": []
        },
        "pagination": {
            "offset": 0,
            "limit": 100,
            "total": 1
        },
        "policies": [
            {
                "id": str(uuid4()),
                "abilities": {"read": True, "write": True}
            }
        ]
    }
    mock_client.request.return_value = mock_response

    # Test get_current_user
    user = auth_resource.get_current_user()
    assert isinstance(user, User)
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    
    # Verify that info was called
    mock_client.request.assert_called_with(
        method="POST",
        endpoint="/auth.info",
        data=None,
        params=None,
        files=None
    )


def test_get_current_team(auth_resource, mock_client):
    # Setup mock response for info method
    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "status": 200,
        "data": {
            "user": {
                "id": str(uuid4()),
                "name": "Test User",
                "email": "test@example.com",
                "avatarUrl": "https://example.com/avatar.jpg",
                "isSuspended": False,
                "createdAt": "2023-01-01T00:00:00Z",
                "updatedAt": "2023-01-01T00:00:00Z"
            },
            "team": {
                "id": str(uuid4()),
                "name": "Test Team",
                "sharing": True,
                "memberCollectionCreate": True,
                "memberTeamCreate": False,
                "documentEmbeds": True,
                "guestSignin": False,
                "inviteRequired": True,
                "url": "https://app.getoutline.com"
            },
            "groups": [],
            "groupUsers": [],
            "collaborationToken": "collab_token",
            "availableTeams": []
        },
        "pagination": {
            "offset": 0,
            "limit": 100,
            "total": 1
        },
        "policies": [
            {
                "id": str(uuid4()),
                "abilities": {"read": True, "write": True}
            }
        ]
    }
    mock_client.request.return_value = mock_response

    # Test get_current_team
    team = auth_resource.get_current_team()
    assert isinstance(team, Team)
    assert team.name == "Test Team"
    assert team.sharing is True
    
    # Verify that info was called
    mock_client.request.assert_called_with(
        method="POST",
        endpoint="/auth.info",
        data=None,
        params=None,
        files=None
    )
