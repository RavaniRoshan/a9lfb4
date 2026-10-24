const BASE = import.meta.env.VITE_API_BASE || "";

export async function fetchSeries(params: Record<string, string | number>) {
  const qs = new URLSearchParams(params as any).toString();
  const r = await fetch(`${BASE}/api/series?${qs}`);
  if (!r.ok) throw new Error("series fetch failed");
  return r.json();
}

export async function fetchMetrics(params: Record<string, string | number>) {
  const qs = new URLSearchParams(params as any).toString();
  const r = await fetch(`${BASE}/api/metrics?${qs}`);
  if (!r.ok) throw new Error("metrics fetch failed");
  return r.json();
}

export async function fetchConfig() {
  const r = await fetch(`${BASE}/api/config`);
  return r.json();
}
