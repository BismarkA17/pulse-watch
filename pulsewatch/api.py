from fastapi import FastAPI
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