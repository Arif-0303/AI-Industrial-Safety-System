export default function ActionLog({ logs }) {

    if (!logs || logs.length === 0)
        return null;

    return (

        <div
            style={{
                position: "fixed",
                left: 25,
                top: 25,
                width: 360,
                maxHeight: 350,
                overflowY: "auto",
                background: "#141414",
                color: "white",
                borderRadius: 12,
                padding: 18,
                border: "2px solid #ff4040",
                zIndex: 99999
            }}
        >

            <h2>📋 Emergency Action Log</h2>

            <hr />

            {logs.map((log, index) => (

                <div
                    key={index}
                    style={{
                        marginBottom: 12,
                        paddingBottom: 10,
                        borderBottom: "1px solid #333"
                    }}
                >

                    <div
                        style={{
                            color: "#00ff95",
                            fontWeight: "bold"
                        }}
                    >
                        {log.time}
                    </div>

                    <div>

                        {log.action}

                    </div>

                </div>

            ))}

        </div>

    );

}