import { useState } from "react";

export default function StartMonitoring({ onStart }) {
    const [loading, setLoading] = useState(false);

    const startSystem = async () => {
        setLoading(true);

        // Unlock audio
        const audio = new Audio("/sounds/siren.mp3");

        try {
            await audio.play();
            audio.pause();
            audio.currentTime = 0;
        } catch (err) {
            console.log(err);
        }

        // Unlock speech synthesis
        const speech = new SpeechSynthesisUtterance("");

        window.speechSynthesis.speak(speech);

        setTimeout(() => {
            onStart();
        }, 500);
    };

    return (
        <div
            style={{
                position: "fixed",
                inset: 0,
                background: "#050505",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: 99999999,
            }}
        >
            <div
                style={{
                    width: 650,
                    background: "#111",
                    border: "4px solid #00ff99",
                    borderRadius: 15,
                    padding: 40,
                    color: "white",
                    textAlign: "center",
                    boxShadow: "0 0 40px #00ff99",
                }}
            >
                <h1
                    style={{
                        color: "#00ff99",
                        marginBottom: 20,
                    }}
                >
                    AI INDUSTRIAL SAFETY SYSTEM
                </h1>

                <h2>
                    Adobe Hackathon 2026
                </h2>

                <br />

                <h3
                    style={{
                        color: "#ffaa00",
                    }}
                >
                    STATUS : OFFLINE
                </h3>

                <br />

                <button
                    onClick={startSystem}
                    disabled={loading}
                    style={{
                        padding: "18px 50px",
                        fontSize: 22,
                        background: "#00ff99",
                        color: "black",
                        border: "none",
                        borderRadius: 10,
                        cursor: "pointer",
                        fontWeight: "bold",
                    }}
                >
                    {loading
                        ? "INITIALIZING..."
                        : "START MONITORING"}
                </button>
            </div>
        </div>
    );
}