from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.connection_manager import manager

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            # Receive message from client (heartbeat/ping)
            data = await websocket.receive_text()

            await manager.send_personal_message(
                {
                    "type": "heartbeat",
                    "message": "Connection Alive",
                    "received": data,
                    "active_connections": manager.total_connections(),
                },
                websocket,
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)

        await manager.broadcast(
            {
                "type": "system",
                "message": "A client disconnected",
                "active_connections": manager.total_connections(),
            }
        )