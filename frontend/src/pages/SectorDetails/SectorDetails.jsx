import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getSectors } from "../../services/sectorService";

function SectorDetails() {
  const { id } = useParams();
  const [sector, setSector] = useState(null);

  const loadSector = async () => {
    const data = await getSectors();

    const selected = data.find(
      (item) => item.id === Number(id)
    );

    setSector(selected);
  };

  useEffect(() => {
    loadSector();

    const interval = setInterval(loadSector, 5000);

    return () => clearInterval(interval);
  }, []);

  if (!sector) {
    return (
      <div className="text-center text-white mt-20">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white p-10">

      <h1 className="text-4xl font-bold mb-8">
        {sector.name}
      </h1>

      <div className="grid md:grid-cols-2 gap-6">

        <div className="bg-slate-800 p-6 rounded-xl">
          <h2 className="text-xl mb-4">Sensor Data</h2>

          <p>🌡 Temperature : {sector.temperature} °C</p>
          <p>☁ Gas : {sector.gas} ppm</p>
          <p>⚙ Pressure : {sector.pressure} bar</p>
          <p>👷 Workers : {sector.workers_present}</p>
          <p>🔧 Maintenance : {sector.maintenance}</p>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl">

          <h2 className="text-xl mb-4">
            AI Analysis
          </h2>

          <p>Risk Score : {sector.risk_score}</p>

          <p>Risk Level : {sector.risk_level}</p>

          <p className="mt-4">
            Recommendation
          </p>

          <p className="text-green-400">
            {sector.recommendation}
          </p>

        </div>

      </div>

      <div className="bg-slate-800 mt-8 p-6 rounded-xl">

        <h2 className="text-xl mb-4">
          Alerts
        </h2>

        {sector.alerts.map((alert, index) => (
          <div
            key={index}
            className="border-b border-slate-700 py-2"
          >
            <strong>{alert.type}</strong> : {alert.message}
          </div>
        ))}

      </div>

    </div>
  );
}

export default SectorDetails;