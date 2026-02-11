def get_aqi(pm25: float, pm10: float, country: str):
    if country == "IN":
        return convert_cpcb(pm25)
    return convert_epa(pm25)

def convert_epa(pm25):
    if pm25 <= 12:
        return 50, "Good"
    if pm25 <= 35:
        return 100, "Moderate"
    if pm25 <= 55:
        return 150, "Unhealthy for Sensitive"
    if pm25 <= 150:
        return 200, "Unhealthy"
    if pm25 <= 250:
        return 300, "Very Unhealthy"
    return 500, "Hazardous"

def convert_cpcb(pm25):
    if pm25 <= 30:
        return 50, "Good"
    if pm25 <= 60:
        return 100, "Satisfactory"
    if pm25 <= 90:
        return 200, "Moderate"
    if pm25 <= 120:
        return 300, "Poor"
    return 500, "Severe"