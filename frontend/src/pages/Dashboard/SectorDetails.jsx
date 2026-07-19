import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getSectors } from "../../services/sectorService";

function SectorDetails() {
  const { id } = useParams();

  const [sector, setSector] = useState(null);

  useEffect(() => {
    async function loadSector() {
      const data = await getSectors();

      const selected = data.find(
        (item) => item.id === Number(id)
      );

      setSector(selected);
    }

    loadSector();
  }, [id]);

  if (!sector) {
    return (
      <div className="text-white p-10">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-10">

      <h1 className="text-4xl font-bold mb-8">
        {sector.name}
      </h1>

      <div className="grid md:grid-cols-2 gap-6">

        <div className="bg-slate-800 rounded-xl p-6">

          <p>🌡 Temperature: {sector.temperature} °C</p>

          <p className="mt-3">
            ☁ Gas: {sector.gas} ppm
          </p>

          <p className="mt-3">
            ⚙ Pressure: {sector.pressure} bar
          </p>

          <p className="mt-3">
            👷 Workers: {sector.workers_present}
          </p>

          <p className="mt-3">
            🔧 Maintenance: {sector.maintenance}
          </p>

        </div>

        <div className="bg-slate-800 rounded-xl p-6">

          <h2 className="text-2xl font-bold mb-4">
            AI Analysis
          </h2>

          <p>
            Risk Score: {sector.risk_score}
          </p>

          <p className="mt-3">
            Risk Level: {sector.risk_level}
          </p>

          <p className="mt-3">
            Recommendation:
          </p>

          <p className="text-red-400">
            {sector.recommendation}
          </p>

        </div>

      </div>

      {/* AI Alerts */}

      <div className="bg-slate-800 rounded-xl p-6 mt-8">

        <h2 className="text-2xl font-bold mb-4">
          AI Alerts
        </h2>

        <div className="space-y-4">

          <div className="border-b border-slate-700 pb-3">
            <strong>Status</strong>
            <p>{sector.alerts?.ai_alert?.status}</p>
          </div>

          <div className="border-b border-slate-700 pb-3">
            <strong>Cause</strong>
            <p>{sector.alerts?.ai_alert?.cause}</p>
          </div>

          <div className="border-b border-slate-700 pb-3">
            <strong>Risk</strong>
            <p>{sector.alerts?.ai_alert?.risk}</p>
          </div>

          <div className="border-b border-slate-700 pb-3">
            <strong>Recommended Action</strong>
            <p>{sector.alerts?.ai_alert?.action}</p>
          </div>

          <div className="border-b border-slate-700 pb-3">
            <strong>CCTV Status</strong>
            <p>{sector.alerts?.cctv?.status}</p>
          </div>

          <div>
            <strong>CCTV Message</strong>
            <p>{sector.alerts?.cctv?.message}</p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default SectorDetails;