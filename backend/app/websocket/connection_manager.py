from typing import List
from fastapi import WebSocket
import json


class ConnectionManager:
    """
    Production-ready WebSocket Connection Manager.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accept and register a new websocket connection.
        """
        await websocket.accept()

        if websocket not in self.active_connections:
            self.active_connections.append(websocket)

        print(f"✅ Client Connected | Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """
        Remove disconnected websocket.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        print(f"❌ Client Disconnected | Total: {len(self.active_connections)}")

    async def send_personal_message(
        self,
        message: dict,
        websocket: WebSocket,
    ):
        """
        Send message to a single client.
        """
        await websocket.send_text(json.dumps(message))

    async def broadcast(
        self,
        message: dict,
    ):
        """
        Broadcast message to every connected client.
        """

        print("=" * 50)
        print("🔥 BROADCAST CALLED")
        print("Connected Clients:", len(self.active_connections))
        print("Message Type:", message.get("type"))
        print("=" * 50)

        disconnected_clients = []

        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
                print("✅ Sent to one client")
            except Exception as e:
                print("❌ Send Failed:", e)
                disconnected_clients.append(connection)

        for connection in disconnected_clients:
            self.disconnect(connection)

    async def send_sensor_update(
        self,
        sector_name: str,
        temperature: float,
        pressure: float,
        humidity: float,
        gas_level: float,
        risk_score: float,
        risk_label: str,
    ):
        """
        Broadcast live sensor data.
        """

        await self.broadcast(
            {
                "type": "sensor_update",
                "data": {
                    "sector": sector_name,
                    "temperature": temperature,
                    "pressure": pressure,
                    "humidity": humidity,
                    "gas_level": gas_level,
                    "risk_score": risk_score,
                    "risk_label": risk_label,
                },
            }
        )

    async def send_alert(
        self,
        title: str,
        message: str,
        severity: str,
    ):
        """
        Broadcast safety alerts.
        """

        await self.broadcast(
            {
                "type": "alert",
                "data": {
                    "title": title,
                    "message": message,
                    "severity": severity,
                },
            }
        )

    async def send_notification(
        self,
        title: str,
        message: str,
    ):
        """
        Broadcast general notifications.
        """

        await self.broadcast(
            {
                "type": "notification",
                "data": {
                    "title": title,
                    "message": message,
                },
            }
        )

    def total_connections(self):
        """
        Return active websocket count.
        """
        return len(self.active_connections)


manager = ConnectionManager()