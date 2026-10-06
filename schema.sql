CREATE TABLE metrics(
    id SERIAL PRIMARY KEY,
    service  TEXT NOT NULL,
    latency_ms DOUBLE PRECISION NOT NULL,
    error_rate DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL 

);