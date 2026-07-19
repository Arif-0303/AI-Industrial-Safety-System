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
          AI Alerts
        </h2>

        {sector.alerts ? (
          <div className="space-y-4">

            <div className="bg-slate-700 p-4 rounded-lg">
              <h3 className="font-bold text-red-400">
                AI Alert
              </h3>

              <p>
                <strong>Status:</strong>{" "}
                {sector.alerts.ai_alert?.status}
              </p>

              <p>
                <strong>Cause:</strong>{" "}
                {sector.alerts.ai_alert?.cause}
              </p>

              <p>
                <strong>Risk:</strong>{" "}
                {sector.alerts.ai_alert?.risk}
              </p>

              <p>
                <strong>Action:</strong>{" "}
                {sector.alerts.ai_alert?.action}
              </p>
            </div>

            <div className="bg-slate-700 p-4 rounded-lg">
              <h3 className="font-bold text-yellow-400">
                CCTV Analysis
              </h3>

              <p>
                <strong>Status:</strong>{" "}
                {sector.alerts.cctv?.status}
              </p>

              <p>
                <strong>Message:</strong>{" "}
                {sector.alerts.cctv?.message}
              </p>
            </div>

          </div>
        ) : (
          <p>No alerts available.</p>
        )}

      </div>

    </div>
  );
}

export default SectorDetails;