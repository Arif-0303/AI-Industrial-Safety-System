import React, { useState, useEffect } from "react";

export default function CommandCenter({
    emergency,
    onLog,
}) {
    const [status, setStatus] = useState({});

    useEffect(() => {
        setStatus({});
    }, [emergency]);

    if (!emergency) return null;

    function action(name) {
        const time = new Date().toLocaleTimeString();

        setStatus((prev) => ({
            ...prev,
            [name]: "Completed",
        }));

        if (onLog) {
            onLog({
                time,
                action: `${name} executed for ${emergency.sector_name}`,
            });
        }
    }

    return (
        <div
            style={{
                position: "fixed",
                left: 25,
                bottom: 25,
                width: 330,
                background: "#161616",
                color: "white",
                padding: 20,
                borderRadius: 15,
                border: "3px solid red",
                boxShadow: "0 0 25px red",
                zIndex: 99999,
            }}
        >
            <h2>
                🚨 COMMAND CENTER
            </h2>

            <hr />

            <h3>
                {emergency.sector_name}
            </h3>

            <button
                onClick={() => action("Emergency Shutdown")}
                style={buttonStyle("#d32f2f")}
            >
                🛑 Emergency Shutdown
                {status["Emergency Shutdown"] && " ✅"}
            </button>

            <button
                onClick={() => action("Fire Team")}
                style={buttonStyle("#ef6c00")}
            >
                🚒 Dispatch Fire Team
                {status["Fire Team"] && " ✅"}
            </button>

            <button
                onClick={() => action("Medical Team")}
                style={buttonStyle("#1565c0")}
            >
                🚑 Dispatch Medical Team
                {status["Medical Team"] && " ✅"}
            </button>

            <button
                onClick={() => action("Maintenance")}
                style={buttonStyle("#2e7d32")}
            >
                👷 Send Maintenance Team
                {status["Maintenance"] && " ✅"}
            </button>

            <button
                onClick={() => action("Evacuation")}
                style={buttonStyle("#8e24aa")}
            >
                📢 Evacuate Workers
                {status["Evacuation"] && " ✅"}
            </button>
        </div>
    );
}

function buttonStyle(color) {
    return {
        width: "100%",
        padding: 14,
        marginTop: 10,
        border: "none",
        borderRadius: 8,
        color: "white",
        background: color,
        fontWeight: "bold",
        cursor: "pointer",
        fontSize: 16,
    };
}