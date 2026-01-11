# ClimatIQ Backend (FastAPI)

This is the backend API for ClimatIQ, a climate intelligence dashboard.
It provides hybrid climate, health, and migration analytics with simple forecasting.

## Endpoints

GET /api/climate?country=IND&horizon=30  
GET /api/health?country=IND&horizon=30  
GET /api/migration?country=IND&horizon=30  
GET /api/recommend?country=IND&horizon=30  

## Deploy (Render.com)

1. Push this folder to GitHub
2. Go to https://render.com
3. New Web Service
4. Connect repo
5. Build command:
