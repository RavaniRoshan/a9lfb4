import math
from datetime import datetime
from typing import Any, Dict, List, Optional


def _agg(errors: List[float], actuals: List[float]) -> Dict[str, Any]:
    n = len(errors)
    if n == 0:
        return {"n": 0, "mae": None, "rmse": None, "bias": None, "mape": None, "mapeSkipped": 0}
    mae = sum(abs(e) for e in errors) / n
    rmse = math.sqrt(sum(e * e for e in errors) / n)
    bias = sum(errors) / n
    mape_vals = [abs(e) / a for e, a in zip(errors, actuals) if a != 0]
    mape = (sum(mape_vals) / len(mape_vals)) if mape_vals else None
    zero_actuals = sum(1 for a in actuals if a == 0)
    return {"n": n, "mae": mae, "rmse": rmse, "bias": bias, "mape": mape, "mapeSkipped": zero_actuals}


def _horizon_bucket(lead: Optional[float]) -> str:
    if lead is None:
        return "unknown"
    if lead < 12:
        return "0-12h"
    if lead < 24:
        return "12-24h"
    if lead < 36:
        return "24-36h"
    return "36h+"


def _count_gaps(series: List[Dict[str, Any]]) -> int:
    starts = sorted(r["startTime"] for r in series)
    gaps = 0
    for i in range(1, len(starts)):
        t0 = datetime.fromisoformat(starts[i-1].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(starts[i].replace("Z", "+00:00"))
        if (t1 - t0).total_seconds() != 1800:
            gaps += 1
    return gaps


def compute_metrics(series: List[Dict[str, Any]]) -> Dict[str, Any]:
    valid = [r for r in series if r.get("forecast") is not None and r.get("error") is not None]
    errors = [r["error"] for r in valid]
    actuals = [r["actual"] for r in valid]
    overall = _agg(errors, actuals)
    overall["missing"] = len(series) - len(valid)
    overall["gaps"] = _count_gaps(series)

    by_day_map: dict = {}
    for r in valid:
        day = r["startTime"][:10]
        by_day_map.setdefault(day, ([], []))
        by_day_map[day][0].append(r["error"])
        by_day_map[day][1].append(r["actual"])
    by_day = []
    for day in sorted(by_day_map):
        e, a = by_day_map[day]
        by_day.append({"day": day, **_agg(e, a)})

    by_hour_map: dict = {}
    for r in valid:
        hour = int(r["startTime"][11:13])
        by_hour_map.setdefault(hour, ([], []))
        by_hour_map[hour][0].append(r["error"])
        by_hour_map[hour][1].append(r["actual"])
    by_hour = []
    for hour in range(24):
        if hour in by_hour_map:
            e, a = by_hour_map[hour]
            by_hour.append({"hour": hour, **_agg(e, a)})
        else:
            by_hour.append({"hour": hour, "n": 0, "mae": None, "rmse": None, "bias": None, "mape": None, "mapeSkipped": 0})

    buckets = ["0-12h", "12-24h", "24-36h", "36h+"]
    by_horizon_map: dict = {b: ([], []) for b in buckets}
    for r in valid:
        b = _horizon_bucket(r.get("leadHours"))
        if b in by_horizon_map:
            by_horizon_map[b][0].append(r["error"])
            by_horizon_map[b][1].append(r["actual"])
    by_horizon = []
    for b in buckets:
        e, a = by_horizon_map[b]
        by_horizon.append({"bucket": b, **_agg(e, a)})

    return {"overall": overall, "byDay": by_day, "byHour": by_hour, "byHorizon": by_horizon}
