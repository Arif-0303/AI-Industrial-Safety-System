import RiskBadge from "../common/RiskBadge";

function PlantStatus() {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 flex justify-between items-center">
      <div>
        <h2 className="text-3xl font-bold">
          Steel Plant
        </h2>

        <p className="text-slate-400 mt-2">
          AI Powered Industrial Monitoring
        </p>
      </div>

      <div className="text-right">
        <p className="text-slate-400 mb-2">
          Overall Risk
        </p>

        <RiskBadge risk="Critical" />
      </div>
    </div>
  );
}

export default PlantStatus;