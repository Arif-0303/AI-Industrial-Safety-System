import DigitalTwinCard from "./DigitalTwinCard";

export default function DigitalTwin({ sectors = [] }) {
    const critical = sectors
        .filter((s) => s.risk_score >= 80)
        .sort((a, b) => b.risk_score - a.risk_score);

    const warning = sectors
        .filter((s) => s.risk_score >= 40 && s.risk_score < 80)
        .sort((a, b) => b.risk_score - a.risk_score);

    const safe = sectors
        .filter((s) => s.risk_score < 40)
        .sort((a, b) => b.risk_score - a.risk_score);

    return (
        <div className="mt-10">

            <h2 className="text-3xl font-bold text-white mb-6">
                🏭 AI DIGITAL TWIN
            </h2>

            {/* Overview */}

            <div className="grid grid-cols-4 gap-5 mb-10">

                <OverviewCard
                    title="Plants"
                    value={sectors.length}
                    color="bg-slate-700"
                />

                <OverviewCard
                    title="Safe"
                    value={safe.length}
                    color="bg-green-600"
                />

                <OverviewCard
                    title="Warning"
                    value={warning.length}
                    color="bg-yellow-500"
                />

                <OverviewCard
                    title="Critical"
                    value={critical.length}
                    color="bg-red-600"
                />

            </div>

            <Section
                title="🔴 CRITICAL"
                sectors={critical}
                color="border-red-500"
            />

            <Section
                title="🟡 WARNING"
                sectors={warning}
                color="border-yellow-500"
            />

            <Section
                title="🟢 SAFE"
                sectors={safe}
                color="border-green-500"
            />

        </div>
    );
}

function OverviewCard({ title, value, color }) {
    return (
        <div className={`${color} rounded-xl p-5 text-center shadow-lg`}>
            <h3 className="text-white text-lg">
                {title}
            </h3>

            <p className="text-4xl font-bold text-white mt-2">
                {value}
            </p>
        </div>
    );
}

function Section({
    title,
    sectors,
    color,
}) {
    return (
        <div className="mb-10">

            <h2 className="text-2xl text-white font-bold mb-5">
                {title}
            </h2>

            <div className="grid lg:grid-cols-3 md:grid-cols-2 gap-6">

                {sectors.map((sector) => (
                    <DigitalTwinCard
                        key={sector.id}
                        sector={sector}
                        border={color}
                    />
                ))}

            </div>

        </div>
    );
}