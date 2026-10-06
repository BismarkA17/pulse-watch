import pytest 
from pulsewatch.detection import z_score

def test_z_score_one_wobble_above():
    result = z_score(135, [105, 135])
    assert result == pytest.approx(1)

def test_z_score_two_wobble_below():
    result = z_score(90, [105, 135])
    assert result == pytest.approx(-2)

def test_z_score_thirty_two_wobble_above():
    result = z_score(600, [105, 135])
    assert result == pytest.approx(32)

def test_z_score_flat_history_returns_zero():
    result = z_score(130,[120,120,120])
    assert result == pytest.approx(0)