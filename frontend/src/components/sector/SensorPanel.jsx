import InfoCard from "../common/InfoCard";

function SensorPanel({ sector }) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-5">
        Sensor Monitoring
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">

        <InfoCard
          title="Temperature"
          value={sector.temperature}
          color="text-red-400"
        />

        <InfoCard
          title="Gas"
          value={sector.gas}
          color="text-orange-400"
        />

        <InfoCard
          title="Pressure"
          value={sector.pressure}
          color="text-blue-400"
        />

        <InfoCard
          title="Vibration"
          value="0.34 mm/s"
          color="text-green-400"
        />

      </div>
    </div>
  );
}

export default SensorPanel;