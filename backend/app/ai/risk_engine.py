def calculate_risk_score(sector):
    score = 0

    # ===========================
    # Temperature
    # ===========================
    if sector.temperature >= 1500:
        score += 45
    elif sector.temperature >= 1200:
        score += 35
    elif sector.temperature >= 900:
        score += 20
    elif sector.temperature >= 100:
        score += 10

    # ===========================
    # Gas
    # ===========================
    if sector.gas >= 35:
        score += 35
    elif sector.gas >= 20:
        score += 20
    elif sector.gas >= 10:
        score += 10

    # ===========================
    # Pressure
    # ===========================
    if sector.pressure >= 8:
        score += 20
    elif sector.pressure >= 5:
        score += 10

    # ===========================
    # Workers
    # ===========================
    if sector.workers_present >= 20:
        score += 5

    # ===========================
    # Maintenance
    # ===========================
    if sector.maintenance == "Inactive":
        score += 20
    elif sector.maintenance == "Average":
        score += 10

    return min(score, 100)