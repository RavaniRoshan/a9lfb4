import { useEffect, useState } from "react";
import { fetchSeries, fetchMetrics, fetchConfig } from "./api";
import { Period, Metrics } from "./types";
import ForecastTimeline from "./views/ForecastTimeline";
import AccuracyDashboard from "./views/AccuracyDashboard";

export default function App() {
  const [mode, setMode] = useState("gate");
  const [gateTime, setGateTime] = useState("09:10");
  const [leadHours, setLeadHours] = useState(24);
  const [tolerance, setTolerance] = useState(60);
  const [series, setSeries] = useState<Period[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<"timeline" | "accuracy">("timeline");

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const params = { decision_mode: mode, gate_time: gateTime, lead_hours: leadHours, tolerance_min: tolerance };
      const [s, m] = await Promise.all([fetchSeries(params), fetchMetrics(params)]);
      setSeries(s);
      setMetrics(m);
    } catch (e: any) {
      setError(e.message || "load failed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchConfig().then((c) => {
      setMode(c.decision_mode);
      setGateTime(c.gate_time);
      setLeadHours(c.lead_hours);
      setTolerance(c.tolerance_min);
    }).catch(() => {});
  }, []);

  useEffect(() => { load(); }, [mode, gateTime, leadHours, tolerance]);

  return (
    <div className="container">
      <header>
        <h1>UK Wind Forecast Accuracy — January 2026</h1>
        <p className="subtitle">Decision-eligible (day-ahead gate) wind forecasts vs actuals</p>
      </header>
      <section className="controls">
        <label>Mode
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="gate">Day-ahead gate</option>
            <option value="lead">Fixed lead hours</option>
          </select>
        </label>
        {mode === "gate" ? (
          <label>Gate time (UTC)
            <input value={gateTime} onChange={(e) => setGateTime(e.target.value)} />
          </label>
        ) : (
          <label>Lead hours
            <input type="number" value={leadHours} onChange={(e) => setLeadHours(Number(e.target.value))} />
          </label>
        )}
        <label>Tolerance (min)
          <input type="number" value={tolerance} onChange={(e) => setTolerance(Number(e.target.value))} />
        </label>
        <button onClick={load} disabled={loading}>{loading ? "Loading…" : "Refresh"}</button>
      </section>
      {error && <div className="error">{error}</div>}
      <nav className="tabs">
        <button className={tab === "timeline" ? "active" : ""} onClick={() => setTab("timeline")}>Forecast Timeline</button>
        <button className={tab === "accuracy" ? "active" : ""} onClick={() => setTab("accuracy")}>Accuracy Dashboard</button>
      </nav>
      {tab === "timeline" ? (
        <ForecastTimeline series={series} />
      ) : (
        <AccuracyDashboard metrics={metrics} />
      )}
    </div>
  );
}
