export default function IncidentTimeline({ emergency }) {

    if (!emergency) return null;

    const steps = [

        "Normal Operation",

        "Abnormal Sensor Values",

        "AI Risk Increased",

        emergency.incident_prediction?.incident || "Incident Predicted",

        "Emergency Broadcast",

        "Evacuation Started"

    ];

    return (

        <div
            style={{
                background: "#181818",
                color: "white",
                padding: 20,
                borderRadius: 15,
                marginTop: 20,
            }}
        >

            <h2>
                📈 INCIDENT TIMELINE
            </h2>

            <hr />

            {steps.map((step, index) => (

                <div
                    key={index}
                    style={{
                        display: "flex",
                        alignItems: "center",
                        marginBottom: 15,
                    }}
                >

                    <div
                        style={{
                            width: 18,
                            height: 18,
                            borderRadius: "50%",
                            background: index <= 3 ? "#ff3b30" : "#777",
                            marginRight: 15,
                        }}
                    />

                    <div>

                        {step}

                    </div>

                </div>

            ))}

        </div>

    );

}