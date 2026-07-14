import { Link } from "react-router-dom";
import RiskBadge from "../common/RiskBadge";
import PredictiveMaintenanceCard from "./PredictiveMaintenanceCard";
import IncidentPredictionCard from "./IncidentPredictionCard";
function SectorCard({ sector }) {
  return (
  <Link
    to={`/sector/${sector.id}`}
    className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-red-500 transition block"
  >
    <div className="flex justify-between items-center mb-4">
      <h2 className="text-xl font-bold">{sector.name}</h2>

      <RiskBadge risk={sector.risk} />
    </div>

    <div className="space-y-2 text-sm">

      <p>
        🌡 Temperature :
        <span className="float-right">{sector.temperature} °C</span>
      </p>

      <p>
        ☁ Gas :
        <span className="float-right">{sector.gas} ppm</span>
      </p>

      <p>
        ⚙ Pressure :
        <span className="float-right">{sector.pressure} bar</span>
      </p>

      <p>
        👷 Workers :
        <span className="float-right">{sector.workers_present}</span>
      </p>

      <p>
        🔧 Maintenance :
        <span className="float-right">{sector.maintenance}</span>
      </p>

    </div>

    <PredictiveMaintenanceCard sector={sector} />
    
    <IncidentPredictionCard sector={sector} />

  </Link>
);
}

export default SectorCard;