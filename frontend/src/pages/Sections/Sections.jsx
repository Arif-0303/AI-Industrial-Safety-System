import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getSectors } from "../../services/sectorService";
import DigitalTwin from "../../components/dashboard/DigitalTwin";

function Sections() {
    const [sectors, setSectors] = useState([]);
    const navigate = useNavigate();

    const loadSectors = async () => {
        try {
            const data = await getSectors();
            setSectors(data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        loadSectors();

        const interval = setInterval(loadSectors, 5000);

        return () => clearInterval(interval);
    }, []);

    const critical = sectors.filter((s) => s.risk_score >= 80);
    const warning = sectors.filter(
        (s) => s.risk_score >= 50 && s.risk_score < 80
    );
    const safe = sectors.filter((s) => s.risk_score < 50);

    const renderGroup = (title, color, list) => (
        <div className="mb-10">
            <h2
                className="text-3xl font-bold mb-5"
                style={{ color }}
            >
                {title}
            </h2>

            <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
                {list.map((sector) => (
                    <div
                        key={sector.id}
                        onClick={() =>
                            navigate(`/sector/${sector.id}`)
                        }
                        className="cursor-pointer rounded-xl bg-slate-800 hover:bg-slate-700 transition-all p-5 border border-slate-700 hover:scale-105"
                    >
                        <h3 className="text-xl font-bold mb-3">
                            {sector.name}
                        </h3>

                        <p>🌡 Temperature : {sector.temperature} °C</p>

                        <p>☣ Gas : {sector.gas}</p>

                        <p>⚙ Pressure : {sector.pressure}</p>

                        <p>👷 Workers : {sector.workers_present}</p>

                        <p className="mt-3 text-red-400 font-bold">
                            AI Risk : {sector.risk_score}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );

    return (
        <div className="min-h-screen bg-slate-950 text-white p-8">

            <h1 className="text-4xl font-bold mb-8">
                🏭 Industrial Sections
            </h1>

            <DigitalTwin sectors={sectors} />

            <div className="mt-10">
                {renderGroup(
                    "🔴 CRITICAL",
                    "#ff4040",
                    critical
                )}

                {renderGroup(
                    "🟡 WARNING",
                    "#ffcc00",
                    warning
                )}

                {renderGroup(
                    "🟢 SAFE",
                    "#00ff88",
                    safe
                )}
            </div>

        </div>
    );
}

export default Sections;