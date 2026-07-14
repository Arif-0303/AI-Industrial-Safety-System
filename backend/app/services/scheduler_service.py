from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx

scheduler = AsyncIOScheduler()


async def broadcast_sensor_data():
    """
    Automatically triggers sensor broadcast every few seconds.
    """
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://ai-industrial-safety-system.onrender.com/sensors/broadcast"
            )
    except Exception as e:
        print("Scheduler Error:", e)


def start_scheduler():

    scheduler.add_job(
        broadcast_sensor_data,
        "interval",
        seconds=5,
    )

    scheduler.start()