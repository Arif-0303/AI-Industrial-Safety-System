import { useEffect, useRef, useState } from "react";

export default function EmergencyPopup({
    emergency,
    onBroadcast,
    onClose,
}) {
    // Persistent siren instance
    const siren = useRef(new Audio("/sounds/siren.mp3"));
    siren.current.loop = true;

    const [seconds, setSeconds] = useState(45);

    const activeSector = useRef(null);

    // ---------------------------------------
    // Only reset timer when sector changes
    // Start siren immediately on new emergency
    // ---------------------------------------
    useEffect(() => {
        if (!emergency) {
            activeSector.current = null;

            siren.current.pause();
            siren.current.currentTime = 0;

            window.speechSynthesis.cancel();

            setSeconds(45);

            return;
        }

        if (activeSector.current !== emergency.sector_id) {
            activeSector.current = emergency.sector_id;

            setSeconds(45);

            // Start siren immediately
            siren.current
                .play()
                .then(() => {
                    console.log("✅ Siren started successfully");
                })
                .catch((err) => {
                    console.error("❌ Siren failed:", err);
                });
        }
    }, [emergency]);

    // ---------------------------------------
    // Countdown
    // ---------------------------------------
    useEffect(() => {
        if (!emergency) return;

        if (seconds <= 0) return;

        // 30 seconds announcement
        if (seconds === 30) {
            const speech = new SpeechSynthesisUtterance(
                "Emergency acknowledged. Waiting for operator response."
            );

            speech.rate = 1;
            speech.pitch = 1;

            window.speechSynthesis.speak(speech);
        }

        const timer = setTimeout(() => {
            setSeconds((prev) => prev - 1);
        }, 1000);

        return () => clearTimeout(timer);
    }, [seconds, emergency]);

    // ---------------------------------------
    // Auto Broadcast every 10 seconds
    // after timer finishes
    // ---------------------------------------
    useEffect(() => {
        if (!emergency) return;
        if (seconds > 0) return;

        speakEmergency();

        const interval = setInterval(() => {
            speakEmergency();
        }, 10000);

        return () => clearInterval(interval);
    }, [seconds, emergency]);

    function speakEmergency() {
        const speech = new SpeechSynthesisUtterance(
            `Emergency.
            ${emergency.sector_name}.
            Critical industrial risk detected.
            Please evacuate immediately.
            Safety team report to ${emergency.sector_name}.`
        );

        speech.rate = 1;
        speech.pitch = 1;

        speech.onend = () => {
            siren.current.pause();
            siren.current.currentTime = 0;
        };

        window.speechSynthesis.speak(speech);

        if (onBroadcast) {
            onBroadcast();
        }
    }

    if (!emergency) return null;

    return (
        <div
            style={{
                position: "fixed",
                right: 25,
                bottom: 25,
                width: 430,
                background: "#111",
                color: "white",
                border: "4px solid #ff2020",
                borderRadius: 15,
                padding: 22,
                zIndex: 999999,
                boxShadow: "0 0 30px red",
                animation: "pulse 1s infinite",
            }}
        >
            <h2 style={{ color: "#ff4040" }}>
                🚨 EMERGENCY RESPONSE
            </h2>

            <hr />

            <h3>{emergency.sector_name}</h3>

            <p>
                <b>Risk Score :</b> {emergency.risk_score}
            </p>

            <p>
                <b>Workers :</b> {emergency.workers_present}
            </p>

            <hr />

            <h3 style={{ color: "#ff7070" }}>
                🤖 AI ANALYSIS
            </h3>

            <div
                style={{
                    background: "#1b1b1b",
                    padding: 12,
                    borderRadius: 8,
                    border: "1px solid #333",
                    marginBottom: 10,
                }}
            >
                <p style={{ color: "#ff6666", fontWeight: "bold" }}>
                    INCIDENT CAUSE
                </p>

                <p>
                    {emergency.incident_prediction?.cause ||
                        "No incident cause detected"}
                </p>

                <hr />

                <p style={{ color: "#ffcc00", fontWeight: "bold" }}>
                    AI MESSAGE
                </p>

                <p>
                    {emergency.alerts?.ai_alert?.message ||
                        "AI analysis unavailable"}
                </p>

                <hr />

                <p style={{ color: "#00ff99", fontWeight: "bold" }}>
                    ACTION
                </p>

                <p>
                    {emergency.alerts?.ai_alert?.action ||
                        "Follow standard emergency evacuation procedures."}
                </p>
            </div>

            <hr />

            <h3 style={{ color: "#4fd1ff" }}>
                🎥 CCTV ANALYSIS
            </h3>

            <div
                style={{
                    background: "#1b1b1b",
                    padding: 12,
                    borderRadius: 8,
                    border: "1px solid #333",
                }}
            >
                <p>
                    {emergency.alerts?.cctv?.message ||
                        "No CCTV abnormality detected"}
                </p>
            </div>

            <hr />

            <div
                style={{
                    textAlign: "center",
                    fontSize: 48,
                    color: seconds <= 10 ? "#ff2020" : "#00ff99",
                    fontWeight: "bold",
                    marginTop: 15,
                    marginBottom: 15,
                }}
            >
                {seconds}s
            </div>

            <button
                onClick={speakEmergency}
                style={{
                    width: "100%",
                    padding: 16,
                    fontSize: 18,
                    background: "#ff2020",
                    color: "white",
                    border: "none",
                    cursor: "pointer",
                    borderRadius: 8,
                    fontWeight: "bold",
                }}
            >
                🔊 BROADCAST TO SPEAKERS NOW
            </button>

            <button
                onClick={() => {
                    siren.current.pause();
                    siren.current.currentTime = 0;
                    window.speechSynthesis.cancel();

                    onClose();
                }}
                style={{
                    width: "100%",
                    padding: 12,
                    marginTop: 10,
                    borderRadius: 8,
                    border: "none",
                    cursor: "pointer",
                    background: "#444",
                    color: "white",
                }}
            >
                Dismiss
            </button>
        </div>
    );
}