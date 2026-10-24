import os
from fastapi.testclient import TestClient

from app.main import app

SAMPLE_ACTUALS = [
    {"startTime": "2026-01-02T00:00:00Z", "generation": 1000, "publishTime": "2026-01-02T00:30:00Z", "settlementDate": "2026-01-02", "settlementPeriod": 1, "fuelType": "WIND", "dataset": "FUELHH"},
]
SAMPLE_FORECASTS = [
    {"publishTime": "2026-01-01T07:30:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 950, "dataset": "WINDFOR"},
]


def test_health():
    c = TestClient(app)
    r = c.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_series_shape(monkeypatch):
    import app.main as m
    monkeypatch.setattr(m, "fetch_fuelhh", lambda force=False: SAMPLE_ACTUALS)
    monkeypatch.setattr(m, "fetch_windfor", lambda force=False: SAMPLE_FORECASTS)
    c = TestClient(app)
    r = c.get("/api/series")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 1
    assert set(data[0].keys()) >= {"startTime", "actual", "forecast", "publishTime", "leadHours", "error", "missing"}


def test_metrics_shape(monkeypatch):
    import app.main as m
    monkeypatch.setattr(m, "fetch_fuelhh", lambda force=False: SAMPLE_ACTUALS)
    monkeypatch.setattr(m, "fetch_windfor", lambda force=False: SAMPLE_FORECASTS)
    c = TestClient(app)
    r = c.get("/api/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "overall" in data and "byDay" in data and "byHour" in data and "byHorizon" in data
    assert len(data["byHour"]) == 24
