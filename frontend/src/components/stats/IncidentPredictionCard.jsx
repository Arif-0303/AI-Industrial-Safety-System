import React from "react";

export default function IncidentPredictionCard({ sectors }) {

    if (!sectors || sectors.length === 0) {
        return null;
    }


    // Find highest risk sector
    const highest = [...sectors]
        .sort(
            (a, b) =>
                (b.incident_prediction?.accident_probability || 0) -
                (a.incident_prediction?.accident_probability || 0)
        )[0];


    if (!highest || !highest.incident_prediction) {
        return null;
    }


    const prediction = highest.incident_prediction;


    let color = "#00ff95";


    if (prediction.severity === "Critical") {

        color = "#ff2020";

    } else if (prediction.severity === "High") {

        color = "#ff9900";

    } else if (prediction.severity === "Medium") {

        color = "#ffff00";

    }


    return (
        <div
            style={{
                background: "#161616",
                color: "white",
                borderRadius: 15,
                padding: 20,
                border: `3px solid ${color}`,
                boxShadow: `0 0 15px ${color}`,
                animation:
                    prediction.severity === "Critical"
                        ? "pulse 1s infinite"
                        : "none",
            }}
        >

            <h2>
                ⚠ AI INCIDENT PREDICTION
            </h2>


            <hr />


            <p>
                <b>Sector</b>
            </p>


            <h3>
                {highest.name}
            </h3>


            <hr />


            <p>
                <b>Likely Incident</b>
            </p>


            <h3>
                {prediction.cause}
            </h3>


            <hr />


            <p>
                <b>Probability</b>
            </p>


            <div
                style={{
                    width: "100%",
                    height: 15,
                    background: "#444",
                    borderRadius: 10,
                    overflow: "hidden",
                    marginBottom: 10,
                }}
            >

                <div
                    style={{
                        width: `${prediction.accident_probability}%`,
                        height: "100%",
                        background: color,
                        transition: "0.5s",
                    }}
                />

            </div>


            <h2
                style={{
                    color: color,
                    marginTop: 0,
                }}
            >
                {prediction.accident_probability}%
            </h2>


            <hr />


            <p>
                <b>Severity</b>
            </p>


            <h3
                style={{
                    color: color,
                }}
            >
                {prediction.severity}
            </h3>


            <hr />


            <p>
                <b>AI Recommendation</b>
            </p>


            <h3>
                {prediction.recommendation}
            </h3>


        </div>
    );
}