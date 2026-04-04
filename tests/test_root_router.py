from fastapi.testclient import TestClient

from app.bootstrap.factory import create_application


def test_root_info_endpoint():
    client = TestClient(create_application())

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "flex-ai-gateway",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
