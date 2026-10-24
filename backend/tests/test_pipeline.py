import json
from datetime import datetime, timezone

from app.pipeline import (
    parse_dt,
    decision_time_for_period,
    select_vintage,
    align_forecast,
    group_vintages,
    build_series,
)


def test_parse_dt():
    assert parse_dt("2026-01-01T00:00:00Z") == datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_decision_time_gate_previous_day():
    ps = parse_dt("2026-01-15T12:00:00Z")
    dt = decision_time_for_period(ps, mode="gate", gate_time="09:10")
    assert dt == datetime(2026, 1, 14, 9, 10, tzinfo=timezone.utc)


def test_decision_time_lead_hours():
    ps = parse_dt("2026-01-15T12:00:00Z")
    dt = decision_time_for_period(ps, mode="lead", lead_hours=24)
    assert dt == datetime(2026, 1, 14, 12, 0, tzinfo=timezone.utc)


def test_select_vintage_picks_latest_at_or_before():
    pts = [parse_dt("2026-01-01T00:00:00Z"), parse_dt("2026-01-01T06:00:00Z"), parse_dt("2026-01-01T12:00:00Z")]
    dt = parse_dt("2026-01-01T07:30:00Z")
    assert select_vintage(pts, dt) == parse_dt("2026-01-01T06:00:00Z")


def test_select_vintage_none_if_all_after():
    pts = [parse_dt("2026-01-01T12:00:00Z")]
    dt = parse_dt("2026-01-01T07:30:00Z")
    assert select_vintage(pts, dt) is None


def test_align_carry_forward_within_tolerance():
    vintage = [
        {"startTime": "2026-01-01T10:00:00Z", "generation": 100},
    ]
    ps = parse_dt("2026-01-01T10:30:00Z")
    res = align_forecast(vintage, ps, tolerance_min=60)
    assert res == (100.0, parse_dt("2026-01-01T10:00:00Z"))


def test_align_missing_if_beyond_tolerance():
    vintage = [
        {"startTime": "2026-01-01T09:00:00Z", "generation": 100},
    ]
    ps = parse_dt("2026-01-01T10:30:00Z")
    res = align_forecast(vintage, ps, tolerance_min=60)
    assert res is None


def test_align_exact_hourly():
    vintage = [
        {"startTime": "2026-01-01T10:00:00Z", "generation": 200},
    ]
    ps = parse_dt("2026-01-01T10:00:00Z")
    res = align_forecast(vintage, ps, tolerance_min=60)
    assert res == (200.0, parse_dt("2026-01-01T10:00:00Z"))


def test_build_series_basic():
    actuals = [
        {"startTime": "2026-01-02T00:00:00Z", "generation": 1000},
        {"startTime": "2026-01-02T00:30:00Z", "generation": 1100},
    ]
    forecasts = [
        {"publishTime": "2026-01-01T07:30:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 950},
    ]
    series = build_series(actuals, forecasts, mode="gate", gate_time="09:10", tolerance_min=60)
    assert len(series) == 2
    # decision time for Jan 2 periods = Jan 1 09:10; vintage 07:30 eligible
    assert series[0]["publishTime"] == "2026-01-01T07:30:00Z"
    assert series[0]["forecast"] == 950.0
    assert series[0]["error"] == -50.0
    # 00:30 period: carry-forward from 00:00 (30 min) within tolerance
    assert series[1]["forecast"] == 950.0
    assert series[1]["missing"] is False


def test_build_series_missing_forecast_when_no_vintage():
    actuals = [{"startTime": "2026-01-02T00:00:00Z", "generation": 1000}]
    forecasts = [{"publishTime": "2026-01-02T12:00:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 950}]
    series = build_series(actuals, forecasts, mode="gate", gate_time="09:10", tolerance_min=60)
    assert series[0]["missing"] is True
    assert series[0]["forecast"] is None
    assert series[0]["publishTime"] is None


def test_build_series_missing_when_beyond_tolerance():
    actuals = [{"startTime": "2026-01-02T02:00:00Z", "generation": 1000}]
    forecasts = [
        {"publishTime": "2026-01-01T07:30:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 950},
    ]
    series = build_series(actuals, forecasts, mode="gate", gate_time="09:10", tolerance_min=60)
    # 02:00 - 00:00 = 120 min > 60 -> missing
    assert series[0]["missing"] is True


def test_build_series_lead_mode():
    actuals = [{"startTime": "2026-01-02T00:00:00Z", "generation": 1000}]
    forecasts = [
        {"publishTime": "2025-12-31T23:00:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 900},
        {"publishTime": "2026-01-01T23:00:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 950},
    ]
    # lead 24h => decision = Dec 31? period Jan2 00 -24h = Jan1 00; latest vintage <= that = Dec31 23
    series = build_series(actuals, forecasts, mode="lead", lead_hours=24, tolerance_min=60)
    assert series[0]["publishTime"] == "2025-12-31T23:00:00Z"


def test_group_vintages():
    rows = [
        {"publishTime": "2026-01-01T07:30:00Z", "startTime": "2026-01-02T00:00:00Z", "generation": 1},
        {"publishTime": "2026-01-01T07:30:00Z", "startTime": "2026-01-02T01:00:00Z", "generation": 2},
    ]
    g = group_vintages(rows)
    assert len(g) == 1
    assert len(list(g.values())[0]) == 2
