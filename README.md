# UK Wind Forecast Accuracy (Day-Ahead)

National-level UK wind generation: decision-time forecasts vs actuals for January 2026.

## File/directory map
```
backend/
  app/
    main.py        FastAPI routes
    config.py      env-based settings
    elexon.py      Elexon fetch + disk cache + offline mode
    pipeline.py    decision_time, vintage selection, hourly->30-min alignment, series
    metrics.py     MAE/RMSE/bias/MAPE + breakdowns
  tests/           pytest suite
  Dockerfile
  Procfile         Heroku/Render
frontend/
  src/
    App.tsx        controls + tabs
    views/         ForecastTimeline, AccuracyDashboard
  Dockerfile
  nginx.conf
  vercel.json
docker-compose.yml
```

## Run locally (Docker)
```
docker compose up --build
```
Frontend: http://localhost:8080  Backend: http://localhost:8000

## Run locally (dev)
Backend:
```
cd backend
pip install -r requirements.txt
OFFLINE=1 CACHE_DIR=../data/cache uvicorn app.main:app --reload --port 8000
```
Frontend:
```
cd frontend
npm install
npm run dev
```

## Tests
```
cd backend && pytest -q
cd frontend && npm test && npm run lint
```

## Deployment
- Frontend (Vercel): import `frontend/` as a Vite project. Set env `VITE_API_BASE` to the backend URL.
- Backend (Heroku/Render): deploy `backend/` (Dockerfile or Procfile). Set env vars as needed; cache dir is `/data/cache` (ephemeral on Heroku — first request fetches live).

- Frontend (Vercel): https://frontend-mu-beige-39.vercel.app
- Backend (Vercel): https://backend-ten-chi-59.vercel.app

Deployment URL placeholder: `https://frontend-mu-beige-39.vercel.app`

## AI tools disclosure
Built with assistance from an AI coding agent (Kilo/Beam). All generated code was reviewed and tested by the author.

## Domain note
Forecasts are decision-eligible: for each delivery period the latest WINDFOR vintage with publishTime <= decision_time (default previous day 09:10 UTC) is used, never the latest-as-of-now vintage.
