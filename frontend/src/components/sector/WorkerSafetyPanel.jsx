import InfoCard from "../common/InfoCard";

function WorkerSafetyPanel({ sector }) {
  return (
    <div className="mt-8">

      <h2 className="text-2xl font-bold mb-5">
        Worker Safety
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">

        <InfoCard
          title="Workers Present"
          value={sector.workers}
          color="text-green-400"
        />

        <InfoCard
          title="Maintenance"
          value={sector.maintenance}
          color="text-yellow-400"
        />

        <InfoCard
          title="Helmet Detection"
          value="Detected"
          color="text-green-400"
        />

        <InfoCard
          title="Smoke Detection"
          value="Not Detected"
          color="text-green-400"
        />

      </div>

    </div>
  );
}

export default WorkerSafetyPanel;