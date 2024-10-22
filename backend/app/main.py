from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from data.postgresql import create_tables, SessionLocal
from routers import login, top_items
from utils.cron_jobs import setup_scheduler
import logging
from models import User
from utils.user_listening_activity import get_last_week_listening_activities
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from config import OPENAI_API_KEY


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
    db = SessionLocal()
    users = db.query(User).all()
    for i in range(len(users) - 1):
        user = users[i]
        df = get_last_week_listening_activities(db, user.id)
        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=1, model="gpt-3.5-turbo",
                       api_key=OPENAI_API_KEY),
            df,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True,
            verbose=True,
        )
        agent.invoke(
            "What time of day do I listen to music the most?")


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
app.include_router(top_items.router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
