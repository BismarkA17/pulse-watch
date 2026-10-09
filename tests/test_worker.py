from pulsewatch.worker import parse_message, update_history, process_message
from pulsewatch.api import conn


def test_parse_message_converts_strings_to_numbers():
    fields = {
        "service": "auth",
        "latency_ms": "120.5",
        "error_rate": "0.01",
        "timestamp": "1700000000.0",
    }

    service, latency, error_rate, timestamp = parse_message(fields)

    assert service == "auth"
    assert latency == 120.5
    assert error_rate == 0.01
    assert timestamp == 1700000000.0

def test_update_history_keeps_only_last_30():
    history = list(range(30)) 
    update_history(history, 99)
    assert len(history) == 30
    assert history[0] == 1
    assert history[-1] == 99 

def test_normal_message_saves_metric_but_no_incident():
    fields = {
        "service": "auth",
        "latency_ms": "120.0",
        "error_rate": "0.01",
        "timestamp": "1700000000.0",
    }
    histories = {}

    process_message(conn, histories, fields)

    metrics = conn.execute("SELECT COUNT(*) AS n FROM metrics").fetchone()["n"]
    incidents = conn.execute("SELECT COUNT(*) AS n FROM incidents").fetchone()["n"]
    assert metrics == 1
    assert incidents == 0
    assert histories["auth"] == [120.0]

def test_spike_after_warmup_creates_incident():
    histories = {"auth": [105, 135] * 10 }
    fields = {
            "service": "auth",
            "latency_ms": "600",
            "error_rate": "0.01",
            "timestamp": "1700000000.0",
        }
    process_message(conn, histories, fields)
    incidents = conn.execute("SELECT COUNT(*) AS n FROM incidents").fetchone()["n"]
    assert incidents == 1
    incident = conn.execute("SELECT * FROM incidents").fetchone()
    assert incident["service"] == "auth"
    assert incident["status"] == "open"