from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import traffic

load_dotenv()

app = FastAPI(title="Traffic Projection Tool", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic.router)


@app.get("/")
async def root():
    return {"status": "ok", "service": "Traffic Projection Tool"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
