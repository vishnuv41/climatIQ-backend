def heat_index(temp, rh):
    return temp + (0.33 * rh) - 4

def heat_risk(hi):
    if hi < 32:
        return "Low"
    if hi < 40:
        return "Moderate"
    if hi < 54:
        return "High"
    return "Extreme"