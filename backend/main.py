import app.database.init_db
#uvicorn main:app --reload --ws wsproto
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat import router as chat_router
# ============================
# API Routes
# ============================
from app.api.routes.auth import router as auth_router
from app.api.routes.sectors import router as sector_router
from app.api.routes.sensors import router as sensor_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.ai_summary import router as ai_summary_router
from app.api.routes.admin import router as admin_router
from app.api.routes.health import router as health_router
from app.api.routes.notifications import router as notification_router
# WebSocket Routes
from app.websocket.websocket_routes import router as websocket_router

# Middleware
from app.middleware.logging import log_requests
from app.middleware.rate_limit import rate_limit_middleware
from app.middleware.error_handler import global_exception_handler

# Background Scheduler
from app.services.scheduler_service import start_scheduler
from app.api.routes.incidents import router as incident_router

app = FastAPI(
    title="AI Industrial Safety Monitoring System",
    version="1.0.0",
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "https://ai-industrial-safety-system.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Middlewares
# =====================================================

app.middleware("http")(log_requests)
app.middleware("http")(rate_limit_middleware)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# =====================================================
# Register API Routers
# =====================================================

app.include_router(auth_router)
app.include_router(sector_router)
app.include_router(sensor_router)          # Live Sensors
app.include_router(dashboard_router)
app.include_router(ai_summary_router)
app.include_router(admin_router)
app.include_router(health_router)
app.include_router(websocket_router)
print("WebSocket router loaded")
app.include_router(notification_router)
app.include_router(chat_router)
app.include_router(incident_router)
# =====================================================
# Startup Event
# =====================================================

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    print("Scheduler Started")


# =====================================================
# Home
# =====================================================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "AI Industrial Safety Monitoring System Running",
        "docs": "/docs",
        "health": "/health",
        "websocket": "/ws/dashboard",
    }
    #https://ai-industrial-safety-system.onrender.com