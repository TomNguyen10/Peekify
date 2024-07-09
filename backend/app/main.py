from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from data.postgresql import create_tables
from routers import login
from utils.cron_jobs import setup_scheduler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Set up the scheduler
scheduler = setup_scheduler()


@app.on_event("startup")
async def startup_event():
    create_tables()
    logger.info("Tables created successfully (if they didn't exist).")
    scheduler.start()
    logger.info("Scheduler started.")


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    logger.info("Scheduler shut down.")


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
