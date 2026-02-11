# app/aqi.py

# Basic EPA PM2.5 → AQI conversion
def epa_corr(pm25: float):
    if pm25 is None:
        return None
    if pm25 <= 12.0: return int(pm25 * 4.17)
    if pm25 <= 35.4: return int(50 + (pm25 - 12) * 2.04)
    if pm25 <= 55.4: return int(100 + (pm25 - 35.4) * 1.12)
    if pm25 <= 150.4: return int(150 + (pm25 - 55.4) * 0.5)
    return int(200 + (pm25 - 150.4) * 0.5)

def category(aqi):
    if aqi is None: return "Unknown"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy for Sensitive"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very Unhealthy"
    return "Hazardous"