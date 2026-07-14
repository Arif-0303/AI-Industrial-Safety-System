import StatusCard from "../cards/StatusCard";

function PlantOverview({ sectors }) {
  const activeSectors = sectors.length;

  const workersPresent = sectors.reduce(
    (sum, sector) => sum + sector.workers_present,
    0
  );

  const criticalAlerts = sectors.reduce(
    (sum, sector) =>
      sum +
      sector.alerts.filter((alert) => alert.type === "Danger").length,
    0
  );

  const maintenance = sectors.filter(
    (sector) => sector.maintenance === "Inactive"
  ).length;

  return (
    <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-5">

      <StatusCard
        title="Active Sectors"
        value={activeSectors}
        color="text-blue-400"
      />

      <StatusCard
        title="Workers Present"
        value={workersPresent}
        color="text-green-400"
      />

      <StatusCard
        title="Critical Alerts"
        value={criticalAlerts}
        color="text-red-500"
      />

      <StatusCard
        title="Maintenance Due"
        value={maintenance}
        color="text-yellow-400"
      />

    </div>
  );
}

export default PlantOverview;