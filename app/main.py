# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services import get_climate

app = FastAPI(title="ClimatIQ Backend")

# CORS so frontend (React / Flutter / Web) can fetch
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "ClimatIQ backend running"}

@app.get("/climate")
def climate(lat: float, lon: float):
    return get_climate(lat, lon)