from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from data.postgresql import create_tables
from routers import login

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    create_tables()
    print("Tables created successfully (if they didn't exist).")

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
