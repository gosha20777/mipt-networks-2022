import hashlib
import os
import time

from fastapi.testclient import TestClient

from core.config import get_config

prefix = get_config().api_prefix

bin_directory = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../bin'
)


def test_get_wrong_file(client: TestClient):
    expected = {
        "status": "not_found"
    }

    response = client.get(
        f'{prefix}/file', 
        params={
            'file_hash': '8743b52063cd84097a65d1633f5c74f5'
        }
    )
    assert response.status_code == 200
    assert response.json() == expected


def test_upload_file(client: TestClient):
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

    time.sleep(5)
    expected = {
        "status": "available"
    }

    response = client.get(
        f'{prefix}/file', 
        params={
            'file_hash': stolman_img_hash
        }
    )
    assert response.status_code == 200
    assert response.json() == expected

    time.sleep(60)

    expected = {
        "status": "not_found"
    }
    response = client.get(
        f'{prefix}/file', 
        params={
            'file_hash': stolman_img_hash
        }
    )
    assert response.status_code == 200
    assert response.json() == expected
