# Deployment

## Vercel (frontend)
1. `cd frontend && npm ci && npm run build`
2. `npx vercel --prod --yes --env VITE_API_BASE=https://<backend-url>`
3. Note the production URL.

## Vercel (backend)
1. `cd backend`
2. `npx vercel --prod --yes --env CACHE_DIR=/tmp/cache --env OFFLINE=0`
3. Backend URL is the production alias.

## Docker (local)
`docker compose up --build` then open http://localhost:8080.

## Heroku (backend alternative)
`cd backend && heroku create && git push heroku main` (Procfile provided). Set `CACHE_DIR=/app/data/cache`.

## Incognito verification
Open the frontend production URL in an incognito window; confirm the timeline and accuracy views load with January 2026 data and no console errors.
