import { useNavigate } from "react-router-dom";

export default function DigitalTwinCard({
    sector,
    border,
}) {
    const navigate = useNavigate();

    let glow = "";

    if (sector.risk_score >= 80) {
        glow =
            "animate-pulse shadow-[0_0_25px_red]";
    } else if (sector.risk_score >= 40) {
        glow =
            "shadow-[0_0_15px_yellow]";
    } else {
        glow =
            "shadow-[0_0_12px_lime]";
    }

    return (
        <div
            className={`
                bg-[#161616]
                rounded-xl
                p-5
                border-2
                ${border}
                ${glow}
                transition-all
                hover:scale-105
                duration-300
                cursor-pointer
            `}
            onClick={() =>
                navigate(`/sector/${sector.id}`)
            }
        >
            <div className="flex justify-between items-center">

                <h2 className="text-xl font-bold text-white">

                    🏭 {sector.name}

                </h2>

                <span
                    className={`px-3 py-1 rounded-full text-sm font-bold
                    ${
                        sector.risk_score >= 80
                            ? "bg-red-600"
                            : sector.risk_score >= 40
                            ? "bg-yellow-500 text-black"
                            : "bg-green-600"
                    }`}
                >
                    {sector.risk_score >= 80
                        ? "CRITICAL"
                        : sector.risk_score >= 40
                        ? "WARNING"
                        : "SAFE"}
                </span>

            </div>

            <div className="mt-6 space-y-3 text-gray-200">

                <p>
                    🌡 Temperature :
                    <span className="font-bold ml-2">
                        {sector.temperature}°C
                    </span>
                </p>

                <p>
                    ☣ Gas :
                    <span className="font-bold ml-2">
                        {sector.gas}
                    </span>
                </p>

                <p>
                    ⚡ Pressure :
                    <span className="font-bold ml-2">
                        {sector.pressure}
                    </span>
                </p>

                <p>
                    👷 Workers :
                    <span className="font-bold ml-2">
                        {sector.workers_present}
                    </span>
                </p>

            </div>

            <div className="mt-6">

                <div className="w-full bg-gray-700 rounded-full h-4">

                    <div
                        className={`h-4 rounded-full
                        ${
                            sector.risk_score >= 80
                                ? "bg-red-500"
                                : sector.risk_score >= 40
                                ? "bg-yellow-400"
                                : "bg-green-500"
                        }`}
                        style={{
                            width: `${sector.risk_score}%`,
                        }}
                    />

                </div>

                <div className="text-center mt-2 text-white font-bold">

                    AI Risk Score :
                    {" "}
                    {sector.risk_score}%

                </div>

            </div>

            <button
                className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-bold"
            >
                View Sections →
            </button>

        </div>
    );
}