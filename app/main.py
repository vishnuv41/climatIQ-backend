from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import numpy as np

app = FastAPI(title="ClimatIQ Backend", version="1.0")

# CORS (public for hackathon)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# curated list + global fallback
CURATED = ["IND", "KEN", "BRA", "USA", "CHN", "NGA", "BGD", "GBR", "AUS", "EGY"]


def hybrid_score(base, noise=3):
    """Simple hybrid score 0-100"""
    return int(min(max(base + np.random.randint(-noise, noise), 0), 100))


@app.get("/api/climate")
def climate(country: str, horizon: int = 30) -> Dict:
    # simple latitude heuristic for temp
    temp = 25 + np.random.randn() * 2
    rain = abs(int(200 * np.sin(horizon/30 + np.random.randn())))
    return {
        "country": country.upper(),
        "horizon": horizon,
        "temperature": round(temp, 1),
        "rainfall": rain,
    }


@app.get("/api/health")
def health(country: str, horizon: int = 30) -> Dict:
    malaria = hybrid_score(60 if country in ["KEN","NGA","BGD","IND","BRA"] else 20)
    heat = hybrid_score(70 if country in ["IND","EGY","USA","AUS"] else 30)
    return {
        "country": country.upper(),
        "horizon": horizon,
        "malaria_risk": malaria,
        "heat_stress": heat,
    }


@app.get("/api/migration")
def migration(country: str, horizon: int = 30) -> Dict:
    stress = hybrid_score(60)
    category = "High" if stress > 60 else "Moderate" if stress > 30 else "Low"
    return {
        "country": country.upper(),
        "horizon": horizon,
        "stress_score": stress,
        "category": category,
    }


@app.get("/api/recommend")
def recommend(country: str, horizon: int = 30) -> Dict:
    recs = []
    recs.append("Strengthen early-warning systems for heat and extreme weather.")
    recs.append("Enhance vector control measures to reduce malaria impact.")
    recs.append("Support climate-driven migration planning and housing resilience.")
    return {
        "country": country.upper(),
        "horizon": horizon,
        "recommendations": recs,
    }


@app.get("/")
def root():
    return {"status": "ClimatIQ Backend Live"}
