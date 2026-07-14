def calculate_risk_score(sector):
    score = 0

    # Temperature
    if sector.temperature > 80:
        score += 30
    elif sector.temperature > 70:
        score += 20
    elif sector.temperature > 60:
        score += 10

    # Gas
    if sector.gas > 70:
        score += 30
    elif sector.gas > 50:
        score += 20
    elif sector.gas > 30:
        score += 10

    # Pressure
    if sector.pressure > 10:
        score += 20
    elif sector.pressure > 8:
        score += 10

    # Workers
    if sector.workers_present > 8:
        score += 10

    # Maintenance
    if sector.maintenance == "Inactive":
        score += 10

    return min(score, 100)