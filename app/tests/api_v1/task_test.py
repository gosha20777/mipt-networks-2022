import hashlib
import json
import os
import uuid

from fastapi.testclient import TestClient

from core.config import get_config

prefix = get_config().api_prefix

bin_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../bin'
)


def test_get_wrong_task(client: TestClient):
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': '00000000-0000-0000-0000-00000000000a'
        }
    )
    assert response.status_code == 400


def test_register(client: TestClient):
    stolman_img = open(os.path.join(bin_directory, 'stolman.jpg'), 'rb').read()
    stolman_img_hash = hashlib.md5(stolman_img).hexdigest()
    expected = {
        "file_hash": stolman_img_hash,
        "exp": 60
    }

    multipart_form_data = {
        'data': ('stolman.jpg', stolman_img)
    }
    response = client.post(
        f'{prefix}/file', 
        files=multipart_form_data
    )
    assert response.status_code == 200
    assert response.json() == expected

    data = {
        'engine_id': '11111111-1111-1111-1111-111111111111',
        'file_hash': stolman_img_hash
    }

    response = client.post(
        f'{prefix}/task/register',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['task_id']))
    assert x == response.json()['task_id']

    task_id = response.json()['task_id']
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': task_id
        }
    )
    assert response.status_code == 200
    response = dict(response.json())
    assert response['status'] == 'finished'
    x = str(uuid.UUID(response['result']['face_id']))
    assert x == response['result']['face_id']


def test_quality(client: TestClient):
    stolman_img = open(
        os.path.join(bin_directory, 'stolman.jpg'), 'rb'
    ).read()
    stolman_img_hash = hashlib.md5(stolman_img).hexdigest()
    expected = {
        "file_hash": stolman_img_hash,
        "exp": 60
    }

    multipart_form_data = {
        'data': ('stolman.jpg', stolman_img)
    }
    response = client.post(
        f'{prefix}/file', 
        files=multipart_form_data
    )
    assert response.status_code == 200
    assert response.json() == expected

    data = {
        'engine_id': '11111111-1111-1111-1111-111111111111',
        'file_hash': stolman_img_hash
    }

    response = client.post(
        f'{prefix}/task/quality',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['task_id']))
    assert x == response.json()['task_id']

    task_id = response.json()['task_id']
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': task_id
        }
    )
    assert response.status_code == 200
    response = dict(response.json())
    assert response['status'] == 'finished'
    assert response['result']['score'] == 0.9


def test_anti_spoofing(client: TestClient):
    stolman_img = open(
        os.path.join(bin_directory, 'stolman.jpg'), 'rb'
    ).read()
    stolman_img_hash = hashlib.md5(stolman_img).hexdigest()
    expected = {
        "file_hash": stolman_img_hash,
        "exp": 60
    }

    multipart_form_data = {
        'data': ('stolman.jpg', stolman_img)
    }
    response = client.post(
        f'{prefix}/file', 
        files=multipart_form_data
    )
    assert response.status_code == 200
    assert response.json() == expected

    data = {
        'engine_id': '11111111-1111-1111-1111-111111111111',
        'file_hash': stolman_img_hash
    }

    response = client.post(
        f'{prefix}/task/anti_spoofing',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['task_id']))
    assert x == response.json()['task_id']

    task_id = response.json()['task_id']
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': task_id
        }
    )
    assert response.status_code == 200
    response = dict(response.json())
    assert response['status'] == 'finished'
    assert response['result']['score'] == 0.9


def test_best_match(client: TestClient):
    stolman_img = open(
        os.path.join(bin_directory, 'stolman.jpg'), 'rb'
    ).read()
    stolman_img_hash = hashlib.md5(stolman_img).hexdigest()
    expected = {
        "file_hash": stolman_img_hash,
        "exp": 60
    }

    multipart_form_data = {
        'data': ('stolman.jpg', stolman_img)
    }
    response = client.post(
        f'{prefix}/file', 
        files=multipart_form_data
    )
    assert response.status_code == 200
    assert response.json() == expected

    data = {
        'engine_id': '11111111-1111-1111-1111-111111111111',
        'file_hash': stolman_img_hash
    }

    response = client.post(
        f'{prefix}/task/best_match',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['task_id']))
    assert x == response.json()['task_id']

    task_id = response.json()['task_id']
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': task_id
        }
    )
    assert response.status_code == 200
    response = dict(response.json())
    assert response['status'] == 'finished'
    assert response['result']['score'] == 0.9
    x = str(uuid.UUID(response['result']['face_id']))
    assert x == response['result']['face_id']


def test_match(client: TestClient):
    stolman_img = open(os.path.join(bin_directory, 'stolman.jpg'), 'rb').read()
    stolman_img_hash = hashlib.md5(stolman_img).hexdigest()
    expected = {
        "file_hash": stolman_img_hash,
        "exp": 60
    }

    multipart_form_data = {
        'data': ('stolman.jpg', stolman_img)
    }
    response = client.post(
        f'{prefix}/file', 
        files=multipart_form_data
    )
    assert response.status_code == 200
    assert response.json() == expected

    data = {
        'engine_id': '11111111-1111-1111-1111-111111111111',
        'file_hash': stolman_img_hash
    }

    response = client.post(
        f'{prefix}/task/register',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['task_id']))
    assert x == response.json()['task_id']

    task_id = response.json()['task_id']
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': task_id
        }
    )
    assert response.status_code == 200
    response = dict(response.json())
    assert response['status'] == 'finished'
    x = str(uuid.UUID(response['result']['face_id']))
    assert x == response['result']['face_id']

    stolman_img = open(
        os.path.join(bin_directory, 'stolman.jpg'), 'rb'
    ).read()
    stolman_img_hash = hashlib.md5(stolman_img).hexdigest()
    expected = {
        "file_hash": stolman_img_hash,
        "exp": 60
    }

    multipart_form_data = {
        'data': ('stolman.jpg', stolman_img)
    }
    response = client.post(
        f'{prefix}/file', 
        files=multipart_form_data
    )
    assert response.status_code == 200
    assert response.json() == expected

    data = {
        'engine_id': '11111111-1111-1111-1111-111111111111',
        'file_hash': stolman_img_hash,
        'face_id': x
    }

    response = client.post(
        f'{prefix}/task/match',
        data=json.dumps(data)
    )

    assert response.status_code == 200
    x = str(uuid.UUID(response.json()['task_id']))
    assert x == response.json()['task_id']

    task_id = response.json()['task_id']
    response = client.get(
        f'{prefix}/task', 
        params={
            'uuid': task_id
        }
    )
    assert response.status_code == 200
    response = dict(response.json())
    assert response['status'] == 'finished'
    assert response['result']['score'] == 0.9
