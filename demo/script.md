# Demo narration script (record your own voice)

## Part 1 — Client pitch (<=5 min)

1. Title (0:00–0:20): UK Wind Forecast Accuracy — day-ahead decisions.
2. Problem (0:20–0:50): Buyers must procure thermal power; wind output uncertain; decision one day ahead.
3. Data (0:50–1:20): Elexon FUELHH actuals and WINDFOR forecasts; national UK wind only; January 2026.
4. Decision time (1:20–1:50): only forecasts that existed at the gate (prev day 09:10 UTC) count; no hindsight.
5. Demo timeline (1:50–2:30): actual vs decision-eligible forecast; vintage publishTime and lead time per period.
6. Demo accuracy (2:30–3:10): MAE, RMSE, bias, MAPE; by day, hour, horizon.
7. Config (3:10–3:40): gate vs fixed lead hours; carry-forward tolerance.
8. Value (3:40–4:10): price the quantified error; transparent metrics.
9. Guardrails (4:10–4:40): no latest-as-of-now backtest; offline cache; env config.
10. Close Part 1 (4:40–5:00): repo + live URL.

## Part 2 — Technical walkthrough (<=5 min)

11. Architecture (5:00–5:30): FastAPI + React (Vite), Docker, Vercel; no DB.
12. Pipeline (5:30–6:10): fetch → cache → parse → decision_time → vintage → align → metrics.
13. Vintage selection (6:10–6:40): max publishTime <= decision_time; code in pipeline.py.
14. Alignment (6:40–7:10): hourly forecast to 30-min actuals via carry-forward ≤60 min; missing handled.
15. Metrics (7:10–7:40): MAE/RMSE/bias/MAPE; zero-actual guard; by day/hour/horizon.
16. Codebase (7:40–8:10): backend/app, frontend/src/views, tests.
17. Tests/CI (8:10–8:40): pytest 21, tsc, GitHub Actions docker compose verification.
18. Deploy (8:40–9:10): Vercel frontend/backend; env VITE_API_BASE; cache /tmp.
19. Edge cases (9:10–9:40): missing forecasts, zero actuals, gaps, dedup revisions.
20. Close (9:40–10:00): links and next steps.
