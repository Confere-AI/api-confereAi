from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_predict_endpoint():
    resp = client.post("/predict", json={"data": {"x": 1}})
    assert resp.status_code == 200
    body = resp.json()
    assert "result" in body
