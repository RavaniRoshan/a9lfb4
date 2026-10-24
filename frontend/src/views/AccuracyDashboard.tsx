import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Metrics } from "../types";

function fmt(v: number | null) {
  return v == null ? "—" : v.toFixed(1);
}

export default function AccuracyDashboard({ metrics }: { metrics: Metrics | null }) {
  if (!metrics) return <div>Loading metrics…</div>;
  const o = metrics.overall;
  return (
    <div>
      <h2>Forecast accuracy (decision-eligible vintages)</h2>
      <div className="kpi-row">
        <div className="kpi"><span>MAE (MW)</span><strong>{fmt(o.mae)}</strong></div>
        <div className="kpi"><span>RMSE (MW)</span><strong>{fmt(o.rmse)}</strong></div>
        <div className="kpi"><span>Bias (MW)</span><strong>{fmt(o.bias)}</strong></div>
        <div className="kpi"><span>MAPE</span><strong>{o.mape == null ? "—" : (o.mape * 100).toFixed(2) + "%"}</strong></div>
        <div className="kpi"><span>Periods (n)</span><strong>{o.n}</strong></div>
        <div className="kpi"><span>Missing</span><strong>{o.missing}</strong></div>
        <div className="kpi"><span>MAPE skipped (zero actual)</span><strong>{o.mapeSkipped}</strong></div>
        <div className="kpi"><span>Gaps (30-min)</span><strong>{o.gaps}</strong></div>
      </div>

      <h3>MAE by day</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={metrics.byDay}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" minTickGap={30} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="mae" fill="#1f77b4" />
        </BarChart>
      </ResponsiveContainer>

      <h3>MAE by hour of day</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={metrics.byHour}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="hour" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="mae" fill="#ff7f0e" />
        </BarChart>
      </ResponsiveContainer>

      <h3>MAE by forecast horizon</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={metrics.byHorizon}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="bucket" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="mae" fill="#2ca02c" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
