from app.health import router


def test_health_endpoint_exists():
    routes = [r.path for r in router.routes]
    assert "/health" in routes


def test_health_response(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
