from fastapi import FastAPI, Query
from starlette.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware

from app.config import (
    DEFAULT_DECISION_MODE,
    DEFAULT_GATE_TIME,
    DEFAULT_LEAD_HOURS,
    DEFAULT_TOLERANCE_MIN,
)
from app.elexon import fetch_fuelhh, fetch_windfor
from app.metrics import compute_metrics
from app.pipeline import build_series

app = FastAPI(title="UK Wind Forecast Accuracy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _params(decision_mode, gate_time, lead_hours, tolerance_min):
    return {
        "mode": decision_mode or DEFAULT_DECISION_MODE,
        "gate_time": gate_time or DEFAULT_GATE_TIME,
        "lead_hours": lead_hours if lead_hours is not None else DEFAULT_LEAD_HOURS,
        "tolerance_min": tolerance_min if tolerance_min is not None else DEFAULT_TOLERANCE_MIN,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/config")
def config():
    return {
        "decision_mode": DEFAULT_DECISION_MODE,
        "gate_time": DEFAULT_GATE_TIME,
        "lead_hours": DEFAULT_LEAD_HOURS,
        "tolerance_min": DEFAULT_TOLERANCE_MIN,
    }


@app.get("/api/series")
async def series(
    decision_mode: str = Query(DEFAULT_DECISION_MODE, pattern="^(gate|lead)$"),
    gate_time: str = Query(DEFAULT_GATE_TIME, pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$"),
    lead_hours: float = Query(DEFAULT_LEAD_HOURS, ge=0, le=72),
    tolerance_min: int = Query(DEFAULT_TOLERANCE_MIN, ge=0, le=240),
):
    p = _params(decision_mode, gate_time, lead_hours, tolerance_min)
    actuals = await run_in_threadpool(fetch_fuelhh)
    forecasts = await run_in_threadpool(fetch_windfor)
    data = build_series(
        actuals, forecasts,
        mode=p["mode"], gate_time=p["gate_time"],
        lead_hours=p["lead_hours"], tolerance_min=p["tolerance_min"],
    )
    return data


@app.get("/api/metrics")
async def metrics(
    decision_mode: str = Query(DEFAULT_DECISION_MODE, pattern="^(gate|lead)$"),
    gate_time: str = Query(DEFAULT_GATE_TIME, pattern="^([01][0-9]|2[0-3]):[0-5][0-9]$"),
    lead_hours: float = Query(DEFAULT_LEAD_HOURS, ge=0, le=72),
    tolerance_min: int = Query(DEFAULT_TOLERANCE_MIN, ge=0, le=240),
):
    p = _params(decision_mode, gate_time, lead_hours, tolerance_min)
    actuals = await run_in_threadpool(fetch_fuelhh)
    forecasts = await run_in_threadpool(fetch_windfor)
    data = build_series(
        actuals, forecasts,
        mode=p["mode"], gate_time=p["gate_time"],
        lead_hours=p["lead_hours"], tolerance_min=p["tolerance_min"],
    )
    return compute_metrics(data)


@app.post("/api/refresh")
async def refresh():
    await run_in_threadpool(fetch_fuelhh, True)
    await run_in_threadpool(fetch_windfor, True)
    return {"status": "refreshed"}
