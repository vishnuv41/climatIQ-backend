import requests

SAFAR_API = "https://safar.tropmet.res.in/apis/getData.php?city=chennai&param=PM25"

def safar_pm25(city="chennai"):
    try:
        r = requests.get(SAFAR_API.replace("chennai", city.lower()), timeout=5)
        js = r.json()
        
        if js and "data" in js and len(js["data"]) > 0:
            return float(js["data"][-1]["value"])
        return None
        
    except:
        return None