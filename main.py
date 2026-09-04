import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio

app = FastAPI(title="Health App Monitor API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

START_TIME = time.time()

@app.get("/health")
async def get_system_health():
    db_status = "disconnected"
    latency_ms = None

    try:
        start = time.time()
        await client.admin.command('ping')
        latency_ms = round((time.time() - start) * 1000, 2)
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    uptime_seconds = int(time.time() - START_TIME)

    return {
        "status": "healthy",
        "uptime_seconds": uptime_seconds,
        "database": db_status,
        "latency_ms": latency_ms
    }