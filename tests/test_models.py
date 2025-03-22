
from unittest.mock import patch
from outline_wiki_api.client import OutlineWiki


app = OutlineWiki()


@patch('outline_wiki_api.models.auth.Auth.info')
def test_auth_methods(mock_post):
    mock_info_value = {
        "data": {
            "user": {
              "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "name": "Jane Doe",
              "avatarUrl": "string",
              "email": "user@example.com",
              "role": "admin",
              "isSuspended": True,
              "lastActiveAt": "2025-03-22T05:02:49.549Z",
              "createdAt": "2025-03-22T05:02:49.549Z"
            },
            "team": {
              "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "name": "string",
              "avatarUrl": "string",
              "sharing": True,
              "defaultCollectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "defaultUserRole": "admin",
              "memberCollectionCreate": True,
              "documentEmbeds": True,
              "collaborativeEditing": True,
              "inviteRequired": True,
              "allowedDomains": [
                "string"
              ],
              "guestSignin": True,
              "subdomain": "string",
              "url": "string"
            }
        }
    }
    mock_post.return_value.json.return_value = mock_info_value
    info = app.auth.info()
    print(info.json())
    assert info.json() == mock_info_value


if __name__ == "__main__":
    test_auth_methods()
