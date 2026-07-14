import RiskBadge from "../common/RiskBadge";

function AIPredictionPanel({ sector }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 mt-8">

      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">
          AI Prediction
        </h2>

        <RiskBadge risk={sector.risk} />
      </div>

      <div className="mt-6 space-y-5">

        <div>
          <p className="text-slate-400">
            Predicted Hazard
          </p>

          <h3 className="text-xl font-bold text-red-400">
            Gas Leakage
          </h3>
        </div>

        <div>
          <p className="text-slate-400">
            Prediction Probability
          </p>

          <h3 className="text-xl font-bold text-orange-400">
            91%
          </h3>
        </div>

        <div>
          <p className="text-slate-400">
            Suggested Action
          </p>

          <p className="mt-2">
            Evacuate workers immediately and stop maintenance activity.
          </p>
        </div>

      </div>

    </div>
  );
}

export default AIPredictionPanel;