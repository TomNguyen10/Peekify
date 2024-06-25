from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import spotify_tokens, user
from data.postgresql import Base, engine, SessionLocal
from utils.scheduler import scheduler
from dotenv import load_dotenv


load_dotenv()

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(spotify_tokens.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup():
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
