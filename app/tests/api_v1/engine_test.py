import json
import uuid

from fastapi.testclient import TestClient

from core.config import get_config

prefix = get_config().api_prefix


def test_get_engines(client: TestClient):
    expected = {
        'engines': [
            '11111111-1111-1111-1111-111111111111'
        ],
        'max_page': 0
    }

    response = client.get(
        f'{prefix}/engines', 
        params={
            'page': 0,
            'limit': 50
        }
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_get_engines_with_zero_limit(client: TestClient):
    response = client.get(
        f'{prefix}/engines', 
        params={
            'page': 0,
            'limit': 0
        }
    )
    assert response.status_code == 400


def test_get_engine(client: TestClient):
    expected = {
        "engine_type": "tevian",
        "users": [
            "00000000-0000-0000-0000-000000000000"
        ],
        "description": "Room 228",
        "version": {
            "major": 1,
            "minor": 0,
            "path": 0
        },
        "date": "2021-09-16T00:00:00",
        "meta_data": {
            "quality_threshold": 0.6,
            "anti_spoofing_threshold": 0.6,
            "build": "build-0.1.74",
            "extra": {
                'orchestrator_type': 'thread',
                'queue': 'tevian-1-0-0.11111111-1111-1111-1111-111111111111'
            }
        }
    }
    
    response = client.get(
        f'{prefix}/engine', 
        params={
            'uuid': '11111111-1111-1111-1111-111111111111'
        }
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_get_invalid_engine(client: TestClient):
    response = client.get(
        f'{prefix}/engine', 
        params={
            'uuid': '11111111-1111-1111-1111-11111111111a'
        }
    )

    assert response.status_code == 400


def test_create_engine(client: TestClient):
    data = {
        "engine_type": "tevian",
        "description": "Room 229",
        "version": {
            "major": 1,
            "minor": 0,
            "path": 0
        }
    }
    response = client.post(
        f'{prefix}/engine',
        data=json.dumps(data)
    )
    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['engine_id']))
    assert x == response.json()['engine_id']

    engine_id = response.json()['engine_id']
    response = client.get(
        f'{prefix}/engines', 
        params={
            'page': 0,
            'limit': 50
        }
    )
    assert response.status_code == 200
    assert engine_id in response.json()['engines']
    

def test_update_engine(client: TestClient):
    data = {
        "engine_type": "tevian",
        "description": "Room 111",
        "version": {
            "major": 1,
            "minor": 0,
            "path": 0
        }
    }
    response = client.put(
        f'{prefix}/engine',
        data=json.dumps(data), 
        params={
            'uuid': '11111111-1111-1111-1111-111111111111',
        }
    )
    assert response.status_code == 200
    
    response = client.get(
        f'{prefix}/engine', 
        params={
            'uuid': '11111111-1111-1111-1111-111111111111'
        }
    )

    assert response.status_code == 200
    assert response.json()['description'] == 'Room 111'


def test_update_invalid_engine(client: TestClient):
    data = {
        "engine_type": "tevian",
        "description": "Room 111",
        "version": {
            "major": 1,
            "minor": 0,
            "path": 0
        }
    }
    response = client.put(
        f'{prefix}/engine',
        data=json.dumps(data), 
        params={
            'uuid': '11111111-1111-1111-1111-11111111111a',
        }
    )
    assert response.status_code == 400


def test_delete_engine(client: TestClient):
    response = client.delete(
        f'{prefix}/engine',
        params={
            'uuid': '11111111-1111-1111-1111-111111111111',
        }
    )
    assert response.status_code == 200

    response = client.get(
        f'{prefix}/engines', 
        params={
            'page': 0,
            'limit': 50
        }
    )
    assert response.status_code == 200
    assert '11111111-1111-1111-1111-111111111111' not in \
        response.json()['engines']


def test_delete_invalid_engine(client: TestClient):
    response = client.delete(
        f'{prefix}/engine',
        params={
            'uuid': '11111111-1111-1111-1111-11111111111a',
        }
    )
    assert response.status_code == 400
