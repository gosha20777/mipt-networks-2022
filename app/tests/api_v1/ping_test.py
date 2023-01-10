from fastapi.testclient import TestClient

from core.config import get_config

prefix = get_config().api_prefix


def test_ping(client: TestClient):
    response = client.get(f"{prefix}/ping")
    assert response.status_code == 200
