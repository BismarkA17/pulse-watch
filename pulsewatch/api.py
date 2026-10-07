from fastapi import FastAPI , HTTPException
import psycopg 
from psycopg.rows import dict_row

app = FastAPI(title = "Pulsewatch")

conn = psycopg.connect(
    "postgresql://pulsewatch:pulsewatch@localhost:5432/pulsewatch",
    autocommit=True,
    row_factory=dict_row,
)

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/incidents")
def list_incidents():
    rows = conn.execute(
        "SELECT * FROM incidents ORDER BY id DESC"
    ).fetchall()
    return rows 

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    incident = conn.execute(
        "SELECT * FROM incidents WHERE id = %s",
        (incident_id,),
    ).fetchone()
    if incident is None:
        raise HTTPException(status_code=404, detail = "Incident not found")
    else:
        return incident 

@app.post("/incidents/{incident_id}/acknowledge")
def acknowledge_incident(incident_id: int):
    incident = conn.execute(
        "SELECT * FROM incidents WHERE id = %s",
        (incident_id,),
    ).fetchone()
    if incident is None:
        raise HTTPException(status_code=404, detail = "Incident not found")
    if incident["status"] != "open":
        raise HTTPException(status_code=409, detail ="Only open incidents can be acknowledged!")
    updated = conn.execute(
        "UPDATE incidents SET status = %s WHERE id = %s RETURNING *",
        ("acknowledged", incident_id),
    ).fetchone()
    return updated 

@app.post("/incidents/{incident_id}/resolve")
def resolve_incident(incident_id: int):
    incident = conn.execute(
        "SELECT * FROM incidents WHERE id = %s",
        (incident_id,),
    ).fetchone()
    if incident is None:
        raise HTTPException(status_code=404, detail = "Incident not found")
    if incident["status"] == "resolved":
        raise HTTPException(status_code=409, detail ="Incident is already resolved")
    updated = conn.execute(
        "UPDATE incidents SET status = %s WHERE id = %s RETURNING *",
        ("resolved", incident_id),
    ).fetchone()
    return updated 