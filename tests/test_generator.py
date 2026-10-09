from pulsewatch.generator import make_metric


def test_make_metric_has_expected_fields():
    metric = make_metric("auth")

    assert metric["service"] == "auth"
    assert "latency_ms" in metric
    assert "error_rate" in metric
    assert metric["error_rate"] >= 0