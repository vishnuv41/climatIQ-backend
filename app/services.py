import numpy as np

def hybrid_score(base, noise=3):
    return int(min(max(base + np.random.randint(-noise, noise), 0), 100))

def climate_model(country: str, horizon: int):
    temp = 25 + np.random.randn() * 2
    rain = abs(int(200 * np.sin(horizon/30 + np.random.randn())))
    return {
        "country": country,
        "horizon": horizon,
        "temperature": round(temp, 1),
        "rainfall": rain
    }

def health_model(country: str, horizon: int):
    malaria = hybrid_score(60 if country in ["IND","KEN","NGA","BGD","BRA"] else 20)
    heat = hybrid_score(70 if country in ["IND","EGY","USA","AUS"] else 30)
    return {
        "country": country,
        "horizon": horizon,
        "malaria_risk": malaria,
        "heat_stress": heat
    }

def migration_model(country: str, horizon: int):
    stress = hybrid_score(60)
    category = "High" if stress > 60 else "Moderate" if stress > 30 else "Low"
    return {
        "country": country,
        "horizon": horizon,
        "stress_score": stress,
        "category": category
    }

def recommend_model(country: str, horizon: int):
    recs = [
        "Scale heat early-warning systems and climate advisories.",
        "Strengthen mosquito vector control.",
        "Improve migration planning and housing resilience."
    ]
    return {
        "country": country,
        "horizon": horizon,
        "recommendations": recs
    }
