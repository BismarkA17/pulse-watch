from pulsewatch.worker import parse_message, update_history


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