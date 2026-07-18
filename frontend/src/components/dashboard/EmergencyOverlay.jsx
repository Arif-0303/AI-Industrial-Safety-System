import { useEffect, useState } from "react";

export default function EmergencyOverlay({
    open,
    emergency,
}) {
    const [flash, setFlash] = useState(false);

    useEffect(() => {
        if (!open) return;

        const interval = setInterval(() => {
            setFlash((prev) => !prev);
        }, 600);

        return () => clearInterval(interval);
    }, [open]);

    if (!open || !emergency) return null;

    return (
        <div
            style={{
                position: "fixed",
                inset: 0,
                zIndex: 9999999,
                background: flash
                    ? "rgba(180,0,0,0.93)"
                    : "rgba(80,0,0,0.93)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                transition: "0.4s",
            }}
        >
            <div
                style={{
                    width: "75%",
                    background: "#111",
                    border: "6px solid red",
                    borderRadius: 15,
                    padding: 40,
                    color: "white",
                    textAlign: "center",
                    boxShadow: "0 0 50px red",
                }}
            >
                <h1
                    style={{
                        color: "#ff4040",
                        fontSize: 50,
                    }}
                >
                    🚨 AUTONOMOUS EVACUATION
                </h1>

                <h2>{emergency.sector_name}</h2>

                <br />

                <h3 style={{ color: "#ff8080" }}>
                    🤖 AI INSIGHT
                </h3>

                <p>
                    {emergency?.alerts?.ai_alert?.message ||
                        emergency?.incident_prediction?.recommendation ||
                        "AI analysis unavailable"}
                </p>

                <br />

                <h3 style={{ color: "#4dd9ff" }}>
                    🎥 CCTV INSIGHT
                </h3>

                <p>
                    {emergency?.alerts?.cctv?.message ||
                        "No CCTV abnormalities detected"}
                </p>

                <br />

                <h2>
                    👷 Workers Inside : {emergency.workers_present}
                </h2>

                <br />

                <h2
                    style={{
                        color: "#00ff95",
                    }}
                >
                    AI HAS INITIATED EVACUATION
                </h2>
            </div>
        </div>
    );
}