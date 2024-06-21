from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    return {"message": f"Hello {name}"}


def get_db() -> Session:
    """
    Returns a database session.

    Returns:
        Session: The database session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
