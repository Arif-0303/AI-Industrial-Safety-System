def predict_incident(sector):
    """
    AI Incident Prediction Engine
    Returns:
    - accident_probability (%)
    - severity
    - cause
    - recommendation
    """

    probability = 0
    causes = []

    # Temperature
    if sector.temperature > 75:
        probability += 30
        causes.append("High Temperature")

    # Gas
    if sector.gas > 60:
        probability += 30
        causes.append("Gas Leakage Risk")

    # Pressure
    if sector.pressure > 9:
        probability += 20
        causes.append("High Pressure")

    # Maintenance
    if sector.maintenance.lower() == "inactive":
        probability += 20
        causes.append("Maintenance Overdue")

    probability = min(probability, 100)

    # Severity
    if probability >= 80:
        severity = "Critical"
    elif probability >= 60:
        severity = "High"
    elif probability >= 30:
        severity = "Medium"
    else:
        severity = "Low"

    # AI Recommendation
    if severity == "Critical":
        recommendation = "Immediate shutdown and inspection required."
    elif severity == "High":
        recommendation = "Send maintenance team immediately."
    elif severity == "Medium":
        recommendation = "Increase monitoring frequency."
    else:
        recommendation = "System operating normally."

    return {
        "accident_probability": probability,
        "severity": severity,
        "cause": ", ".join(causes) if causes else "No abnormal condition detected",
        "recommendation": recommendation,
    }