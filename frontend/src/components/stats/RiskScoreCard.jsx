function RiskScoreCard({ sectors }) {

  if (sectors.length === 0) {
    return (
      <div className="bg-slate-800 rounded-xl p-5 shadow-lg">
        Loading...
      </div>
    );
  }

  const avg =
    sectors.reduce(
      (sum, sector) => sum + sector.risk_score,
      0
    ) / sectors.length;

  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-lg">

      <h3 className="text-gray-400 text-sm">
        Average AI Risk
      </h3>

      <p className="text-3xl font-bold text-yellow-400 mt-2">
        {avg.toFixed(0)}
      </p>

      <p className="text-sm text-gray-500 mt-2">
        Risk Score
      </p>

    </div>
  );
}

export default RiskScoreCard;