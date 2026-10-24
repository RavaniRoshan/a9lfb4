import math

from app.metrics import compute_metrics


def _series():
    # 4 periods, forecasts
    return [
        {"startTime": "2026-01-01T00:00:00Z", "actual": 100.0, "forecast": 90.0, "error": -10.0, "leadHours": 5.0, "missing": False},
        {"startTime": "2026-01-01T01:00:00Z", "actual": 200.0, "forecast": 210.0, "error": 10.0, "leadHours": 15.0, "missing": False},
        {"startTime": "2026-01-02T00:00:00Z", "actual": 0.0, "forecast": 5.0, "error": 5.0, "leadHours": 30.0, "missing": False},
        {"startTime": "2026-01-02T01:00:00Z", "actual": 50.0, "forecast": None, "error": None, "leadHours": None, "missing": True},
    ]


def test_overall_metrics():
    m = compute_metrics(_series())
    o = m["overall"]
    # valid periods: first 3 (4th missing)
    assert o["n"] == 3
    # errors -10,10,5
    assert abs(o["mae"] - (10+10+5)/3) < 1e-9
    assert abs(o["rmse"] - math.sqrt((100+100+25)/3)) < 1e-9
    assert abs(o["bias"] - (5)/3) < 1e-9
    # mape: skip zero actual (3rd actual 0); uses periods 1,2: (10/100 + 10/200)/2 = (0.1+0.05)/2=0.075
    assert abs(o["mape"] - 0.075) < 1e-9
    assert o["missing"] == 1


def test_by_day():
    m = compute_metrics(_series())
    days = [d["day"] for d in m["byDay"]]
    assert "2026-01-01" in days
    assert "2026-01-02" in days


def test_by_hour_has_24():
    m = compute_metrics(_series())
    assert len(m["byHour"]) == 24


def test_by_horizon_buckets():
    m = compute_metrics(_series())
    buckets = [h["bucket"] for h in m["byHorizon"]]
    assert buckets == ["0-12h", "12-24h", "24-36h", "36h+"]


def test_empty_series():
    m = compute_metrics([])
    assert m["overall"]["n"] == 0
    assert m["overall"]["mae"] is None
    assert m["overall"]["missing"] == 0
