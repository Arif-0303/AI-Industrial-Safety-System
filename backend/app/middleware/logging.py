import time
import logging

from fastapi import Request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("SafetySystem")


async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)

    logger.info(
        f"{request.method} {request.url.path} "
        f"Status={response.status_code} "
        f"Time={process_time}s"
    )

    return response