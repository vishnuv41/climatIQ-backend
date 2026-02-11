import requests
from math import sin, pi, log
from app.aqi import epa_corr, category
from datetime import datetime

# ----------- SAFAR + MAPS -----------

SAFAR_CITIES = {
    "Chennai": "Chennai",
    "Delhi": "Delhi",
    "Mumbai": "Mumbai",
    "Pune": "Pune",
    "Ahmedabad": "Ahmedabad",
    "Kolkata": "Kolkata",
    "Bengaluru": "Bengaluru",
    "Hyderabad": "Hyderabad",
    "Lucknow": "Lucknow"
}

STATE_MAP = {
    "Tamil Nadu": "TN",
    "Kerala": "KL",
    "Karnataka": "KA",
    "Andhra Pradesh": "AP",
    "Telangana": "TS",
    "Maharashtra": "MH",
    "Gujarat": "GJ",
    "West Bengal": "WB",
    "Uttar Pradesh": "UP",
    "Delhi": "DL",
    "Haryana": "HR",
    "Rajasthan": "RJ",
    "Punjab": "PB"
}

REGIONAL_NEAREST = {
    "TN": "Chennai",
    "KL": "Bengaluru",
    "KA": "Bengaluru",
    "AP": "Hyderabad",
    "TS": "Hyderabad",
    "MH": "Mumbai",
    "GJ": "Ahmedabad",
    "WB": "Kolkata",
    "UP": "Lucknow",
    "DL": "Delhi",
    "HR": "Delhi",
    "RJ": "Delhi",
    "PB": "Delhi"
}

# ----------- GEO LOOKUP -----------

def geo_lookup(lat, lon):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/reverse?latitude={lat}&longitude={lon}&language=en"
        r = requests.get(url, timeout=5).json()
        if r.get("results"):
            d = r["results"][0]
            city = d.get("name")
            if city:
                city = city.replace(" Corporation", "").replace(" City", "").strip()
            return {
                "city": city,
                "state": d.get("admin1"),
                "country": d.get("country_code")
            }
    except:
        pass

    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        r = requests.get(url, headers={"User-Agent": "climatiq"}, timeout=5).json()
        addr = r.get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village")
        if city:
            city = city.replace(" City", "").replace(" Corporation", "")
        return {
            "city": city,
            "state": addr.get("state"),
            "country": addr.get("country_code", "").upper()
        }
    except:
        pass

    return {"city": None, "state": None, "country": None}

# ----------- WEATHER -----------

def fetch_forecast(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&hourly=temperature_2m,relativehumidity_2m,uv_index,pm2_5,precipitation"
        "&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,sunrise,sunset"
        "&timezone=auto"
    )
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

# ----------- EXTERNAL AQI -----------

def safar(city):
    try:
        r = requests.get(
            f"https://safar.tropmet.res.in/v2/city/{city}",
            timeout=5,
            verify=False
        ).json()
        if r.get("cities"):
            row = r["cities"][0]
            return {
                "pm25": row["PM25"],
                "aqi": row["AQI"],
                "aqi_cat": row["AQI_Bucket"],
                "src": "SAFAR"
            }
    except:
        return None

def waqi(lat, lon):
    try:
        r = requests.get(
            f"https://api.waqi.info/feed/geo:{lat};{lon}/?token=d23b5f10141e06b6ff217bf6b5ccd93f202f3aa7",
            timeout=5
        ).json()
        if r.get("status") == "ok":
            return r["data"]["iaqi"]["pm25"]["v"]
    except:
        return None

def openaq(lat, lon):
    try:
        r = requests.get(
            f"https://api.openaq.org/v2/latest?limit=1&coordinates={lat},{lon}&parameter=pm25",
            timeout=5
        ).json()
        if r.get("results"):
            return r["results"][0]["measurements"][0]["value"]
    except:
        return None

# ----------- DEW + FEELS ----------

def dew_point(T, H):
    a, b = 17.27, 237.7
    alpha = (a * T) / (b + T) + log(H / 100)
    return round((b * alpha) / (a - alpha), 1)

def feels(T, H):
    if T >= 27:
        return round(
            -8.784695
            + 1.61139411 * T
            + 2.338549 * H
            - 0.14611605 * T * H
            - 0.012308094 * T * T
            - 0.016424828 * H * H
            + 0.002211732 * T * T * H
            + 0.00072546 * T * H * H
            - 0.000003582 * T * T * H * H,
            1
        )
    if T >= 10:
        return round(T + 0.33 * (H / 100) * 10 - 0.7, 1)
    return T

# ----------- MAIN -----------

def get_climate(lat, lon):
    geo = geo_lookup(lat, lon)
    f = fetch_forecast(lat, lon)
    h = f["hourly"]

    temp = f["current_weather"]["temperature"]

    temps = h["temperature_2m"]
    idx = min(range(len(temps)), key=lambda i: abs(temps[i] - temp))

    hum = h["relativehumidity_2m"][idx]
    uv = h["uv_index"][idx]
    pp = h["precipitation"][idx]

    dew = dew_point(temp, hum)
    fl = feels(temp, hum)

    # ----- WIND (ADDED ONLY) -----
    wind_speed = f["current_weather"].get("windspeed")
    wind_dir = f["current_weather"].get("winddirection")
    wind_gust = f["current_weather"].get("windgusts")

    # ----- local time -----
    local_time = f["current_weather"]["time"]
    now = datetime.fromisoformat(local_time)

    # ----- daytime check -----
    sunrise = datetime.fromisoformat(f["daily"]["sunrise"][0])
    sunset = datetime.fromisoformat(f["daily"]["sunset"][0])

    is_night = now < sunrise or now > sunset
    uv_night = (uv == 0 and now < sunrise)

    # ----- AQI -----
    aqi = None

    if geo["country"] == "IN" and geo["state"]:
        metro = SAFAR_CITIES.get(geo["city"]) or REGIONAL_NEAREST.get(
            STATE_MAP.get(geo["state"])
        )
        if metro:
            aqi = safar(metro)

    if not aqi:
        pm = openaq(lat, lon)
        if pm:
            aqi = {
                "pm25": pm,
                "aqi": epa_corr(pm),
                "aqi_cat": category(epa_corr(pm)),
                "src": "OpenAQ"
            }

    if not aqi:
        pm = waqi(lat, lon)
        if pm:
            aqi = {
                "pm25": pm,
                "aqi": epa_corr(pm),
                "aqi_cat": category(epa_corr(pm)),
                "src": "WAQI"
            }

    if not aqi:
        pm = h["pm2_5"][idx]
        if pm:
            aqi = {
                "pm25": pm,
                "aqi": epa_corr(pm),
                "aqi_cat": category(epa_corr(pm)),
                "src": "EPA"
            }

    if not aqi:
        aqi = {
            "pm25": 50,
            "aqi": epa_corr(50),
            "aqi_cat": category(epa_corr(50)),
            "src": "Fallback"
        }

    # ----- TREND -----
    trend = []
    base = aqi["pm25"] or 60

    for i in range(24):
        pm = (
            h["pm2_5"][i]
            if h["pm2_5"][i] is not None
            else int(base + sin((i / 24) * 2 * pi) * 40)
        )

        trend.append({
            "t": h["time"][i],
            "time": h["time"][i].split("T")[1],
            "temp": h["temperature_2m"][i],
            "humidity": h["relativehumidity_2m"][i],
            "pm25": pm,
            "uv": h["uv_index"][i],
            "precip": h["precipitation"][i]
        })

    # ----- FORECAST -----
    daily = f["daily"]
    forecast = [{
        "day": daily["time"][i],
        "tmax": daily["temperature_2m_max"][i],
        "tmin": daily["temperature_2m_min"][i],
        "uv": daily["uv_index_max"][i],
        "precip": daily["precipitation_sum"][i]
    } for i in range(len(daily["time"]))]

    sun = {
        "sunrise": daily["sunrise"][0],
        "sunset": daily["sunset"][0]
    }

    return {
        "location": geo,
        "local_time": local_time,
        "is_night": is_night,
        "uv_night": uv_night,
        "current": {
            "temp": temp,
            "humidity": hum,
            "dew": dew,
            "feels": fl,
            "uv": uv,
            "precip": pp,
            "wind_speed": wind_speed,
            "wind_dir": wind_dir,
            "wind_gust": wind_gust
        },
        "air": aqi,
        "trend": trend,
        "forecast": forecast,
        "sun": sun
    }