export type Period = {
  startTime: string;
  actual: number;
  forecast: number | null;
  forecastStartTime: string | null;
  publishTime: string | null;
  leadHours: number | null;
  error: number | null;
  missing: boolean;
  decisionTime: string;
};

export type Metrics = {
  overall: { n: number; mae: number | null; rmse: number | null; bias: number | null; mape: number | null; missing: number };
  byDay: { day: string; n: number; mae: number | null; rmse: number | null; bias: number | null; mape: number | null }[];
  byHour: { hour: number; n: number; mae: number | null; rmse: number | null; bias: number | null; mape: number | null }[];
  byHorizon: { bucket: string; n: number; mae: number | null; rmse: number | null; bias: number | null; mape: number | null }[];
};
