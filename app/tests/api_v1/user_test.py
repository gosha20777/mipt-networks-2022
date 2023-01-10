import json
import uuid

from fastapi.testclient import TestClient

from core.config import get_config

prefix = get_config().api_prefix


def test_get_users(client: TestClient):
    expected = {
        'users': [
            '00000000-0000-0000-0000-000000000000'
        ],
        'max_page': 0
    }

    response = client.get(
        f'{prefix}/users', 
        params={
            'page': 0,
            'limit': 50
        }
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_users_with_zero_limit(client: TestClient):
    response = client.get(
        f'{prefix}/users', 
        params={
            'page': 0,
            'limit': 0
        }
    )
    assert response.status_code == 400


def test_get_user(client: TestClient):
    expected = {
        'user': 'user',
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ],
        'roles': [
            'user',
            'admin'
        ],
        'date': '2021-09-16T00:00:00'
    }
    
    response = client.get(
        f'{prefix}/user', 
        params={
            'uuid': '00000000-0000-0000-0000-000000000000'
        }
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_invalid_user(client: TestClient):
    response = client.get(
        f'{prefix}/user', 
        params={
            'uuid': '00000000-0000-0000-0000-00000000000a'
        }
    )

    assert response.status_code == 400


def test_create_user(client: TestClient):
    data = {
        'user': 'user1',
        'password': 'password1',
        'roles': [
            'user',
            'admin'
        ],
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ]
    }
    response = client.post(
        f'{prefix}/user',
        data=json.dumps(data)
    )
    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['user_id']))
    assert x == response.json()['user_id']

    user_id = response.json()['user_id']
    response = client.get(
        f'{prefix}/users', 
        params={
            'page': 0,
            'limit': 50
        }
    )
    assert response.status_code == 200
    assert user_id in response.json()['users']


def test_create_existing_user(client: TestClient):
    data = {
        'user': 'user',
        'password': 'password',
        'roles': [
            'user',
            'admin'
        ],
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ]
    }
    response = client.post(
        f'{prefix}/user',
        data=json.dumps(data)
    )
    assert response.status_code == 400
    

def test_update_user(client: TestClient):
    data = {
        'user': 'user2',
        'password': 'password',
        'roles': [
            'user',
            'admin'
        ],
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ]
    }
    response = client.put(
        f'{prefix}/user',
        data=json.dumps(data), 
        params={
            'uuid': '00000000-0000-0000-0000-000000000000',
        }
    )
    assert response.status_code == 200

    expected = {
        'user': 'user2',
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ],
        'roles': [
            'user',
            'admin'
        ],
        'date': '2021-09-16T00:00:00'
    }
    
    response = client.get(
        f'{prefix}/user', 
        params={
            'uuid': '00000000-0000-0000-0000-000000000000'
        }
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_invalid_user(client: TestClient):
    data = {
        'user': 'user2',
        'password': 'password',
        'roles': [
            'user',
            'admin'
        ],
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ]
    }
    response = client.put(
        f'{prefix}/user',
        data=json.dumps(data), 
        params={
            'uuid': '00000000-0000-0000-0000-00000000000a',
        }
    )
    assert response.status_code == 400


def test_delete_user(client: TestClient):
    response = client.delete(
        f'{prefix}/user',
        params={
            'uuid': '00000000-0000-0000-0000-000000000000',
        }
    )
    assert response.status_code == 200

    response = client.get(
        f'{prefix}/users', 
        params={
            'page': 0,
            'limit': 50
        }
    )
    assert response.status_code == 200
    assert '00000000-0000-0000-0000-000000000000' not in \
        response.json()['users']


def test_delete_invalid_user(client: TestClient):
    response = client.delete(
        f'{prefix}/user',
        params={
            'uuid': '00000000-0000-0000-0000-00000000000a',
        }
    )
    assert response.status_code == 400
