from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple


def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def decision_time_for_period(
    period_start: datetime,
    mode: str = "gate",
    gate_time: str = "09:10",
    lead_hours: float = 24.0,
) -> datetime:
    if mode == "lead":
        return period_start - timedelta(hours=lead_hours)
    # gate mode: previous day at gate_time UTC
    prev_date = period_start.date() - timedelta(days=1)
    hh, mm = gate_time.split(":")
    return datetime(
        prev_date.year, prev_date.month, prev_date.day,
        int(hh), int(mm), tzinfo=timezone.utc,
    )


def select_vintage(
    publish_times: List[datetime], decision_time: datetime
) -> Optional[datetime]:
    cands = [p for p in publish_times if p <= decision_time]
    if not cands:
        return None
    return max(cands)


def align_forecast(
    vintage_points: List[Dict[str, Any]],
    period_start: datetime,
    tolerance_min: int = 60,
) -> Optional[Tuple[float, datetime]]:
    cands = [p for p in vintage_points if parse_dt(p["startTime"]) <= period_start]
    if not cands:
        return None
    best = max(cands, key=lambda p: parse_dt(p["startTime"]))
    fs = parse_dt(best["startTime"])
    if (period_start - fs).total_seconds() <= tolerance_min * 60:
        return float(best["generation"]), fs
    return None


def group_vintages(forecast_rows: List[Dict[str, Any]]) -> Dict[datetime, List[Dict[str, Any]]]:
    out: Dict[datetime, List[Dict[str, Any]]] = {}
    for r in forecast_rows:
        pt = parse_dt(r["publishTime"])
        out.setdefault(pt, []).append(r)
    return out


def build_series(
    actual_rows: List[Dict[str, Any]],
    forecast_rows: List[Dict[str, Any]],
    mode: str = "gate",
    gate_time: str = "09:10",
    lead_hours: float = 24.0,
    tolerance_min: int = 60,
) -> List[Dict[str, Any]]:
    actuals = sorted(actual_rows, key=lambda r: r["startTime"])
    vintages = group_vintages(forecast_rows)
    publish_times = sorted(vintages.keys())
    results: List[Dict[str, Any]] = []
    for a in actuals:
        ps = parse_dt(a["startTime"])
        dt = decision_time_for_period(ps, mode, gate_time, lead_hours)
        pub = select_vintage(publish_times, dt)
        forecast = None
        fstart = None
        missing = True
        if pub is not None:
            aligned = align_forecast(vintages[pub], ps, tolerance_min)
            if aligned is not None:
                forecast, fstart = aligned
                missing = False
        lead = (ps - pub).total_seconds() / 3600.0 if pub is not None else None
        gen = float(a["generation"])
        error = (forecast - gen) if forecast is not None else None
        results.append({
            "startTime": a["startTime"],
            "actual": gen,
            "forecast": forecast,
            "forecastStartTime": fstart.isoformat().replace("+00:00", "Z") if fstart else None,
            "publishTime": pub.isoformat().replace("+00:00", "Z") if pub else None,
            "leadHours": lead,
            "error": error,
            "missing": missing,
            "decisionTime": dt.isoformat().replace("+00:00", "Z"),
        })
    return results
