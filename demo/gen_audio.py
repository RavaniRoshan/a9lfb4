from gtts import gTTS
import subprocess, os

narr = [
 ("Title", "UK Wind Forecast Accuracy. A day-ahead decision tool for January twenty twenty six."),
 ("Problem", "Energy buyers must procure thermal power beyond expected wind. Wind output is weather dependent and the purchase decision is made about one day before delivery."),
 ("Data", "We use Elexon data only. FUELHH gives thirty minute actual wind generation. WINDFOR gives hourly wind forecasts."),
 ("Decision time", "A forecast is only usable if it existed at decision time. We use the latest WINDFOR vintage with publish time less than or equal to the day ahead gate, default previous day zero nine ten UTC. Comparing against the newest forecast on record is a hindsight backtest and is wrong."),
 ("Demo timeline", "The timeline view shows actual versus the decision eligible forecast. Each period shows which vintage publish time was used and the resulting lead time in hours."),
 ("Demo accuracy", "The accuracy dashboard shows MAE two thousand one hundred forty five megawatts, RMSE two thousand six hundred sixteen, bias plus one thousand eight hundred fifty two, MAPE twenty two point four percent across one thousand four hundred eighty eight periods. Worst day is twenty eighth January at roughly five thousand three hundred seventy five megawatts."),
 ("Config", "Decision time is configurable: day ahead gate or fixed lead hours. Alignment tolerance defaults to sixty minutes to bridge hourly forecasts and thirty minute actuals."),
 ("Value", "This lets the team price the quantified forecast error into procurement decisions."),
 ("Guardrails", "No latest as of now comparison. Live fetch with disk cache and offline mode. Configuration via environment variables."),
 ("Part 1 close", "That concludes the client pitch. Part two covers the technical implementation."),
 ("Architecture", "Backend is FastAPI in Python. Frontend is React with Vite. Docker compose runs the full stack. Deployed to Vercel. No database."),
 ("Pipeline", "The pipeline fetches and caches raw Elexon JSON, parses actuals and forecasts, computes decision time, selects the vintage, aligns hourly to thirty minutes, and computes metrics."),
 ("Vintage", "For each period we select the maximum publish time less than or equal to decision time. This is implemented in pipeline dot py."),
 ("Alignment", "Forecasts are hourly, actuals are thirty minutes. We carry forward the latest forecast start less than or equal to the period start within tolerance. Missing forecasts are counted."),
 ("Metrics", "We compute MAE, RMSE, bias, and MAPE with a guard for zero actuals. Breakdowns by day, hour of day, and horizon bucket zero to twelve, twelve to twenty four, twenty four to thirty six, and thirty six plus hours."),
 ("Codebase", "Backend app contains pipeline, metrics, elexon fetch, and main routes. Frontend views are ForecastTimeline and AccuracyDashboard. Tests cover pipeline, metrics, and API."),
 ("Tests and CI", "Twenty one backend tests and one frontend smoke test. Ruff and TypeScript checks. GitHub Actions runs tests and docker compose verification."),
 ("Deployment", "Frontend and backend deployed on Vercel. Frontend uses VITE_API_BASE. Backend cache directory is slash tmp slash cache."),
 ("Edge cases", "Missing forecasts, zero actual generation, coverage gaps, and duplicate revisions are handled. Actuals are deduplicated by latest publish time."),
 ("Close", "Repository at github dot com slash RavaniRoshan slash girds wind forecast. Live app at frontend mu beige thirty nine dot vercel dot app."),
]

os.makedirs("audio", exist_ok=True)
total=0
for i,(title,text) in enumerate(narr):
    tts=gTTS(text=text, lang="en", slow=False)
    fn=f"audio/slide_{i:02d}.mp3"
    tts.save(fn)
    # duration
    out=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",fn]).decode().strip()
    dur=float(out)
    total+=dur
    print(i, round(dur,2), title)
print("total audio", round(total,2))
