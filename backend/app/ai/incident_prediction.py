def predict_incident(sector):
    """
    Intelligent AI Incident Prediction Engine
    """

    probability = 0

    reasons = []

    # ==========================================================
    # Temperature
    # ==========================================================

    if sector.temperature >= 90:

        probability += 35

        reasons.append(
            f"Critical temperature ({sector.temperature}°C)"
        )

    elif sector.temperature >= 80:

        probability += 20

        reasons.append(
            f"High temperature ({sector.temperature}°C)"
        )

    # ==========================================================
    # Gas
    # ==========================================================

    if sector.gas >= 70:

        probability += 35

        reasons.append(
            f"Dangerous gas concentration ({sector.gas})"
        )

    elif sector.gas >= 55:

        probability += 20

        reasons.append(
            f"Gas concentration increasing ({sector.gas})"
        )

    # ==========================================================
    # Pressure
    # ==========================================================

    if sector.pressure >= 10:

        probability += 20

        reasons.append(
            f"High pressure ({sector.pressure})"
        )

    # ==========================================================
    # Maintenance
    # ==========================================================

    if sector.maintenance.lower() == "inactive":

        probability += 15

        reasons.append(
            "Maintenance overdue"
        )

    probability = min(probability, 100)

    # ==========================================================
    # Severity
    # ==========================================================

    if probability >= 90:

        severity = "CRITICAL"

        confidence = "VERY HIGH"

        estimated_time = "5 Minutes"

    elif probability >= 75:

        severity = "HIGH"

        confidence = "HIGH"

        estimated_time = "15 Minutes"

    elif probability >= 55:

        severity = "MEDIUM"

        confidence = "MEDIUM"

        estimated_time = "30 Minutes"

    else:

        severity = "LOW"

        confidence = "LOW"

        estimated_time = "No Immediate Risk"

    # ==========================================================
    # Incident Type
    # ==========================================================

    if sector.temperature >= 90 and sector.gas >= 70:

        incident = "Explosion"

    elif sector.temperature >= 90:

        incident = "Industrial Fire"

    elif sector.gas >= 70:

        incident = "Toxic Gas Leak"

    elif sector.pressure >= 10:

        incident = "Pressure Vessel Failure"

    else:

        incident = "No Major Incident Expected"

    # ==========================================================
    # Recommendation
    # ==========================================================

    if severity == "CRITICAL":

        recommendation = (
            "Immediately evacuate workers, isolate the affected equipment, "
            "stop production and dispatch the emergency response team."
        )

    elif severity == "HIGH":

        recommendation = (
            "Reduce plant load, inspect the sector immediately and prepare emergency response."
        )

    elif severity == "MEDIUM":

        recommendation = (
            "Increase monitoring frequency and schedule maintenance."
        )

    else:

        recommendation = (
            "Continue normal plant operation."
        )

    return {

        "incident": incident,

        "probability": probability,

        "severity": severity,

        "confidence": confidence,

        "estimated_time": estimated_time,

        "reason": (
            " | ".join(reasons)
            if reasons
            else "No abnormal condition detected."
        ),

        "recommendation": recommendation,

    }