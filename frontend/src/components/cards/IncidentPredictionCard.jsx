function IncidentPredictionCard({ sector }) {
  const probability = sector.accident_probability;

  let color = "bg-green-500";
  if (probability >= 60) color = "bg-red-500";
  else if (probability >= 30) color = "bg-yellow-500";

  return (
    <div className="mt-5 border-t border-slate-700 pt-4">

      <h3 className="font-semibold text-red-400 mb-3">
        🤖 AI Incident Prediction
      </h3>

      <div className="mb-3">
        <div className="flex justify-between text-sm mb-1">
          <span>Accident Probability</span>
          <span>{probability}%</span>
        </div>

        <div className="w-full bg-slate-700 rounded-full h-3">
          <div
            className={`${color} h-3 rounded-full transition-all duration-500`}
            style={{ width: `${probability}%` }}
          />
        </div>
      </div>

      <p className="text-sm">
        <strong>Severity:</strong>{" "}
        {sector.incident_severity}
      </p>

      <p className="text-sm mt-2">
        <strong>Cause:</strong>{" "}
        {sector.incident_cause}
      </p>

      <p className="text-sm mt-2 text-cyan-300">
        {sector.incident_recommendation}
      </p>

    </div>
  );
}

export default IncidentPredictionCard;