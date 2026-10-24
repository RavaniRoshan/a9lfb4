import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Period } from "../types";

export default function ForecastTimeline({ series }: { series: Period[] }) {
  const data = series.map((p) => ({
    time: p.startTime.slice(5, 16).replace("T", " "),
    actual: p.actual,
    forecast: p.forecast,
    publishTime: p.publishTime,
    leadHours: p.leadHours,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload || !payload.length) return null;
    const p = payload[0].payload;
    return (
      <div style={{ background: "#fff", border: "1px solid #ccc", padding: 8, fontSize: 12 }}>
        <div><strong>{p.time}</strong></div>
        <div>Actual: {p.actual?.toLocaleString()} MW</div>
        <div>Forecast: {p.forecast == null ? "—" : p.forecast.toLocaleString()} MW</div>
        <div>Vintage: {p.publishTime ?? "—"}</div>
        <div>Lead: {p.leadHours == null ? "—" : p.leadHours.toFixed(1)} h</div>
      </div>
    );
  };

  return (
    <div>
      <h2>Decision-time wind forecast vs actual</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" minTickGap={40} />
          <YAxis label={{ value: "MW", angle: -90, position: "insideLeft" }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line type="monotone" dataKey="actual" stroke="#1f77b4" dot={false} name="Actual" />
          <Line type="monotone" dataKey="forecast" stroke="#ff7f0e" dot={false} name="Decision-eligible forecast" />
        </LineChart>
      </ResponsiveContainer>
      <div className="table-wrap">
        <table>
          <thead>
            <tr><th>Period (UTC)</th><th>Actual MW</th><th>Forecast MW</th><th>Error MW</th><th>Vintage (publishTime)</th><th>Lead h</th></tr>
          </thead>
          <tbody>
            {series.map((p) => (
              <tr key={p.startTime}>
                <td>{p.startTime}</td>
                <td>{p.actual.toLocaleString()}</td>
                <td>{p.forecast == null ? "—" : p.forecast.toLocaleString()}</td>
                <td>{p.error == null ? "—" : p.error.toLocaleString()}</td>
                <td>{p.publishTime ?? "—"}</td>
                <td>{p.leadHours == null ? "—" : p.leadHours.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
