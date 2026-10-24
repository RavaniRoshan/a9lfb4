# CLAUDE.md

## Project
UK day-ahead wind forecast accuracy tool. React (Vite) front-end, FastAPI back-end, Docker.

## Commands
- Backend dev: `cd backend && uvicorn app.main:app --reload --port 8000`
- Backend tests: `cd backend && pytest -q`
- Frontend dev: `cd frontend && npm run dev`
- Frontend build: `cd frontend && npm run build`
- Frontend tests: `cd frontend && npm test`
- Full stack: `docker compose up --build`
- Lint: `cd backend && ruff check .` ; `cd frontend && npm run lint`

## Architecture (3 sentences)
FastAPI fetches FUELHH actuals and WINDFOR forecasts from Elexon at runtime, caches raw JSON to disk, and serves aggregated decision-eligible forecast series and accuracy metrics. React renders two views: a decision-time forecast timeline and an accuracy dashboard. No database; all data is loaded into memory per request from cache or live fetch.

## Domain gotcha (read this)
A forecast is only usable if it existed at decision time. For each delivery period, use the WINDFOR vintage with the greatest publishTime <= decision_time(period), never the newest on record. Comparing actuals against "latest as of now" is a hindsight backtest and is wrong. decision_time(period) defaults to previous day 09:10 UTC (GB day-ahead gate); alternative fixed lead hours. Align hourly WINDFOR startTime to 30-min FUELHH periods by carry-forward within tolerance (default 60 min).

## Scope
National UK wind only, Elexon data alone. January 2026 delivery window. No DB, no auth, no secrets.
