from pydantic import BaseModel

class ClimateResponse(BaseModel):
    country: str
    horizon: int
    temperature: float
    rainfall: int

class HealthResponse(BaseModel):
    country: str
    horizon: int
    malaria_risk: int
    heat_stress: int

class MigrationResponse(BaseModel):
    country: str
    horizon: int
    stress_score: int
    category: str

class RecommendResponse(BaseModel):
    country: str
    horizon: int
    recommendations: list[str]
