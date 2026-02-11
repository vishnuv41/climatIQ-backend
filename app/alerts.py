def generate_alerts(hi, aqi, uv):
    alerts = []
    if hi > 40:
        alerts.append("Heat stress risk today")
    if uv > 6:
        alerts.append("High UV exposure expected")
    if aqi > 100:
        alerts.append("Air quality unhealthy for sensitive groups")
    return alerts