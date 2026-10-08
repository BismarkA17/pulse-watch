from fastapi.testclient import TestClient

from pulsewatch.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_incidents():
    response = client.get("/incidents")
    assert response.status_code == 200 
    assert isinstance(response.json(), list)

def test_incident_not_found():
    response = client.get("/incidents/999999")
    assert response.status_code == 404 
    assert response.json() == {"detail": "Incident not found"}

def test_incident_id_must_be_a_number():
    response = client.get("/incidents/abc")
    assert response.status_code == 422 

def test_metrics_limit():
    response = client.get("/metrics?limit=3")
    assert response.status_code == 200 
    assert len(response.json()) == 3 
