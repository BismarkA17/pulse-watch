from fastapi.testclient import TestClient

from pulsewatch.api import app, conn

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
    for i in range(5):
        conn.execute(
            "INSERT INTO metrics (service, latency_ms, error_rate, recorded_at) "
            "VALUES (%s, %s, %s, now())",
            ("test", 100.0, 0.01),
        )
    response = client.get("/metrics?limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_incident_lifecycle():
    incident_id = conn.execute(
        "INSERT INTO incidents (service, latency_ms)"
        "VALUES(%s, %s) "
        "RETURNING id",
        ("test", 999.0)      
    ).fetchone()["id"]

    response = client.get(f"/incidents/{incident_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "open"

    response_1 = client.post(f"/incidents/{incident_id}/acknowledge")
    assert response_1.status_code == 200
    assert response_1.json()["status"] == "acknowledged"

    response_2 = client.post(f"/incidents/{incident_id}/acknowledge")
    assert response_2.status_code == 409 

    response_3 = client.post(f"/incidents/{incident_id}/resolve")
    assert response_3.status_code == 200 
    assert response_3.json()["status"] == "resolved"

    response_4 = client.post(f"/incidents/{incident_id}/resolve")
    assert response_4.status_code == 409

    delete_incident_id = conn.execute(
        "DELETE FROM incidents WHERE id = %s",
        (incident_id,)
    )

def test_acknowledge_missing_incident():
    response = client.post("/incidents/999999/acknowledge")
    assert response.status_code == 404

def test_resolve_missing_incident():
    response = client.post("/incidents/999999/resolve")
    assert response.status_code == 404


