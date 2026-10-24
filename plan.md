# Plan

## Goal
Web app for UK day-ahead wind forecast accuracy (Jan 2026), satisfying brief goals (1) and (2).

## Repo layout
```
girds/
  CLAUDE.md
  plan.md
  README.md
  docker-compose.yml
  backend/
    app/
      __init__.py
      main.py          # FastAPI app, routes, CORS
      config.py        # env-based settings
      models.py        # pydantic models
      elexon.py        # live fetch + disk cache + offline mode
      pipeline.py      # pure logic: decision_time, vintage selection, alignment, series
      metrics.py       # MAE/RMSE/bias/MAPE + breakdowns
    tests/
      test_pipeline.py
      test_metrics.py
      test_api.py
    requirements.txt
    Dockerfile
  frontend/
    package.json
    vite.config.ts
    tsconfig.json
    index.html
    src/
      main.tsx
      App.tsx
      api.ts
      types.ts
      views/ForecastTimeline.tsx
      views/AccuracyDashboard.tsx
      components/KpiCard.tsx
      styles.css
    Dockerfile
    nginx.conf
```

## Data pipeline steps
1. Fetch FUELHH (fuelType=WIND, settlementDate 2026-01-01..2026-01-31) live; cache raw JSON to `CACHE_DIR/fuelhh.json`. [brief: fetch + cache]
2. Fetch WINDFOR (publishDateTime 2025-12-28..2026-02-01) live; cache raw JSON to `CACHE_DIR/windfor.json`.
3. Offline mode (`OFFLINE=1` or fetch failure with cache present): load from cache; never hardcode.
4. Parse actuals → list of {start, generation}.
5. Group forecasts by publishTime → vintages (dict publish_time -> list {start, generation}).
6. For each actual period compute decision_time (gate: previous day 09:10 UTC; or period - lead_hours).
7. Select vintage = max publishTime <= decision_time.
8. Align: within selected vintage, carry-forward latest forecast start <= period.start within tolerance (default 60 min); else missing.
9. error = forecast - actual; lead_hours = (period.start - publish_time).
10. Aggregate metrics overall + by day + hour-of-day + horizon bucket (0-12/12-24/24-36/36+ h).

## API endpoints
- `GET /api/health`
- `GET /api/series` → PeriodResult[] (actual, forecast, publishTime, leadHours, error, missing)
- `GET /api/metrics` → {overall, byDay[], byHour[], byHorizon[]}
- `GET /api/config` → current settings
- `POST /api/refresh` → re-fetch live (optional)

Query params: decision_mode, gate_time, lead_hours, tolerance_min.

## Front-end views
1. Forecast Timeline: line chart actual vs decision-eligible forecast (MW) over Jan; tooltip shows publishTime + lead time; controls for decision params; table of periods.
2. Accuracy Dashboard: KPI cards (MAE, RMSE, bias, MAPE) + bar charts by day, hour, horizon; missing-forecast count.

## Test list
- test_pipeline: vintage selection (max <= decision), tie/none; alignment carry-forward within tolerance and missing; decision_time gate & lead-hours modes.
- test_metrics: MAE/RMSE/bias/MAPE correctness on hand-computed arrays; zero-actual guard; missing excluded.
- test_api: /health, /series shape, /metrics shape against cached sample.

## Risks
- Network availability in container → offline cache fallback.
- Irregular publish cadence → computed selection, not assumed.
- Hourly→30-min alignment → carry-forward tolerance; missing counted.
- MAPE divide-by-zero → skip zero actuals, report count.
- Large WINDFOR payload (~2.7MB) → cache + in-memory; fine.

## Rejected alternatives
- Pandas/numpy: heavier deps; pure Python sufficient for ~1500 rows.
- "Latest as of now" forecast: hindsight backtest, analytically wrong (brief forbids).
- Database: brief says no DB; in-memory + disk cache.
- Per-period live fetch: too many requests; one bulk fetch + cache.
- Fixed 30-min forecast interpolation: fabricates data; carry-forward is honest.
