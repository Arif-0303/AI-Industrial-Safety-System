import React from "react";

function LiveAlerts({ sectors = [] }) {
  const alerts = [];

  sectors.forEach((sector) => {
    if (!sector.alerts) return;

    // AI Alert
    if (sector.alerts.ai_alert) {
      alerts.push({
        sector: sector.name,
        type: sector.alerts.ai_alert.status,
        message: sector.alerts.ai_alert.cause,
      });
    }

    // CCTV Alert
    if (sector.alerts.cctv) {
      alerts.push({
        sector: sector.name,
        type: sector.alerts.cctv.status,
        message: sector.alerts.cctv.message,
      });
    }
  });

  return (
    <div className="mt-8 rounded-xl bg-gray-900 shadow-lg p-6">
      <h2 className="text-2xl font-bold text-white mb-6">
        🚨 Live AI Alerts
      </h2>

      {alerts.length === 0 ? (
        <div className="rounded-lg bg-green-900/30 border border-green-600 p-4 text-green-300 font-semibold">
          ✅ No Active Alerts
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert, index) => (
            <div
              key={index}
              className={`rounded-xl border-l-4 p-4 shadow ${
                alert.type === "CRITICAL"
                  ? "border-red-600 bg-red-100"
                  : alert.type === "WARNING"
                  ? "border-yellow-500 bg-yellow-100"
                  : alert.type === "SAFE" ||
                    alert.type === "NORMAL"
                  ? "border-green-500 bg-green-100"
                  : "border-blue-500 bg-blue-100"
              }`}
            >
              <h3 className="text-lg font-bold text-gray-900">
                {alert.type}
              </h3>

              <p className="mt-1 text-gray-800">
                {alert.message}
              </p>

              <p className="mt-2 text-sm text-gray-700">
                <span className="font-semibold">
                  Sector:
                </span>{" "}
                {alert.sector}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default LiveAlerts;