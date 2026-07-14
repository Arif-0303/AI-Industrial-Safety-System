def generate_alerts(sector):

    alerts = []

    # Temperature
    if sector.temperature > 85:
        alerts.append({
            "type": "Danger",
            "message": "Critical temperature detected."
        })

    elif sector.temperature > 75:
        alerts.append({
            "type": "Warning",
            "message": "High temperature detected."
        })

    # Gas
    if sector.gas > 70:
        alerts.append({
            "type": "Danger",
            "message": "Gas leakage risk."
        })

    elif sector.gas > 50:
        alerts.append({
            "type": "Warning",
            "message": "Gas level increasing."
        })

    # Pressure
    if sector.pressure > 10:
        alerts.append({
            "type": "Warning",
            "message": "Pressure above normal."
        })

    # Workers
    if sector.workers_present > 8:
        alerts.append({
            "type": "Info",
            "message": "High worker density."
        })

    # Maintenance
    if sector.maintenance == "Inactive":
        alerts.append({
            "type": "Warning",
            "message": "Maintenance overdue."
        })

    if len(alerts) == 0:
        alerts.append({
            "type": "Safe",
            "message": "System operating normally."
        })

    return alerts