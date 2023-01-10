import json
import uuid

from fastapi.testclient import TestClient

from core.config import get_config

prefix = get_config().api_prefix


def test_get_token(client: TestClient):
    expected = {
        "exp": 1735689600,
        "user_id": "00000000-0000-0000-0000-000000000000",
        "access_token": {
            "aud": "greenatom.ru",
            "iss": "greenatom.ru",
            "sub": "00000000-0000-0000-0000-000000000000",
            "jti": "59206680-7755-401d-9eb8-2d79b7418353",
            "roles": [
                "user",
                "admin"
            ],
            "exp": 1735689600
        }
    }
    data = {
        'user': 'user',
        'password': 'password'
    }

    response = client.post(
        f'{prefix}/token',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    response = dict(response.json())
    assert response['exp'] == expected['exp']
    assert response['user_id'] == expected['user_id']
    assert response['access_token']['aud'] == expected['access_token']['aud']
    assert response['access_token']['iss'] == expected['access_token']['iss']
    assert response['access_token']['sub'] == expected['access_token']['sub']
    x = str(uuid.UUID(response['access_token']['jti']))
    assert x == response['access_token']['jti']
    x = response['access_token']['roles']
    assert x == expected['access_token']['roles']
    assert response['access_token']['exp'] == expected['access_token']['exp']
    

def test_get_invalid_user_token(client: TestClient):
    data = {
        'user': 'user1',
        'password': 'password'
    }

    response = client.post(
        f'{prefix}/token',
        data=json.dumps(data)
    )

    assert response.status_code == 400


def test_get_invalid_password_token(client: TestClient):
    data = {
        'user': 'user',
        'password': 'password1'
    }

    response = client.post(
        f'{prefix}/token',
        data=json.dumps(data)
    )

    assert response.status_code == 400
