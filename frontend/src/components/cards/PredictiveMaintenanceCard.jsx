function PredictiveMaintenanceCard({ sector }) {
  const health = sector.machine_health;

  let barColor = "bg-green-500";
  let statusColor = "text-green-400";

  if (health < 80) {
    barColor = "bg-yellow-500";
    statusColor = "text-yellow-400";
  }

  if (health < 50) {
    barColor = "bg-red-500";
    statusColor = "text-red-500";
  }

  return (
    <div className="bg-slate-800 rounded-xl p-5 border border-slate-700 mt-4">

      <h3 className="text-lg font-bold mb-4">
        🔧 Predictive Maintenance
      </h3>

      <div className="mb-4">
        <div className="flex justify-between mb-2">
          <span>Machine Health</span>
          <span>{sector.machine_health}%</span>
        </div>

        <div className="w-full bg-slate-700 rounded-full h-3">
          <div
            className={`${barColor} h-3 rounded-full transition-all duration-500`}
            style={{ width: `${sector.machine_health}%` }}
          ></div>
        </div>
      </div>

      <div className="space-y-2">

        <p>
          ⏳ Remaining Life
          <span className="float-right">
            {sector.remaining_life} hrs
          </span>
        </p>

        <p>
          🔧 Status
          <span className={`float-right font-semibold ${statusColor}`}>
            {sector.maintenance_status}
          </span>
        </p>

      </div>

    </div>
  );
}

export default PredictiveMaintenanceCard;