import { describe, it } from "vitest";
import React from "react";
import ReactDOMServer from "react-dom/server";
import AccuracyDashboard from "./views/AccuracyDashboard";
import { Metrics } from "./types";

describe("AccuracyDashboard", () => {
  it("renders MAPE as 22.44%", () => {
    const metrics: Metrics = {
      overall: { n: 1488, mae: 2145.2, rmse: 2615.8, bias: 1851.9, mape: 0.2244, missing: 0, mapeSkipped: 1, gaps: 0 },
      byDay: [],
      byHour: [],
      byHorizon: [],
    };
    const html = ReactDOMServer.renderToString(React.createElement(AccuracyDashboard, { metrics }));
    if (!html.includes("22.44%")) throw new Error("MAPE not rendered");
  });
});
