function AIRiskPanel({ sectors }) {
  if (!sectors || sectors.length === 0) return null;

  const highRisk = sectors.filter(
    (sector) => sector.risk === "High"
  );

  return (
    <div className="bg-slate-800 rounded-xl p-6 mt-8">

      <h2 className="text-2xl font-bold mb-5">
        AI Risk Analysis
      </h2>

      {highRisk.length === 0 ? (
        <div className="text-green-400 text-lg">
          ✅ No High Risk Sector Detected
        </div>
      ) : (
        highRisk.map((sector) => (
          <div
            key={sector.id}
            className="bg-slate-700 rounded-lg p-4 mb-4"
          >
            <h3 className="text-xl font-bold text-red-400">
              {sector.name}
            </h3>

            <p className="mt-2">
              Risk Score :
              <span className="text-yellow-400 ml-2">
                {sector.risk_score}
              </span>
            </p>

            <p className="mt-2">
              Recommendation :
              <span className="text-green-400 ml-2">
                {sector.recommendation}
              </span>
            </p>

            <div className="mt-3">
              {sector.alerts.map((alert, index) => (
                <div key={index}>
                  • {alert.message}
                </div>
              ))}
            </div>

          </div>
        ))
      )}

    </div>
  );
}

export default AIRiskPanel;