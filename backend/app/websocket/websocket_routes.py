from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from app.websocket.connection_manager import manager
from app.database.session import SessionLocal
from app.models.sector import Sector

from app.api.routes.sensors import (
    simulate_sensor_values,
    build_ai_response,
)

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)


@router.websocket("/dashboard")
async def dashboard_websocket(websocket: WebSocket):

    await manager.connect(websocket)

    db = SessionLocal()

    try:

        while True:

            payload = []

            sectors = db.query(Sector).all()

            for sector in sectors:

                simulate_sensor_values(sector)

                db.commit()
                db.refresh(sector)

                payload.append(
                    build_ai_response(sector)
                )

            await manager.send_personal_message(
                {
                    "type": "sensor_update",
                    "data": payload,
                },
                websocket,
            )

            await asyncio.sleep(5)

    except WebSocketDisconnect:

        manager.disconnect(websocket)

    finally:

        db.close()