def predictive_maintenance(sector):
    """
    Simple AI logic for predictive maintenance.
    Later we will replace this with a Machine Learning model.
    """

    health = 100

    # Temperature effect
    if sector.temperature > 70:
        health -= 20
    elif sector.temperature > 60:
        health -= 10

    # Gas effect
    if sector.gas > 70:
        health -= 20
    elif sector.gas > 50:
        health -= 10

    # Pressure effect
    if sector.pressure > 10:
        health -= 15
    elif sector.pressure > 8:
        health -= 8

    # Maintenance effect
    if sector.maintenance == "Inactive":
        health -= 20

    # Prevent negative values
    health = max(0, health)

    # Remaining life estimation
    remaining_life = int(health * 3)

    # Maintenance status
    if health >= 80:
        status = "Healthy"
    elif health >= 50:
        status = "Maintenance Soon"
    else:
        status = "Immediate Maintenance"

    return {
        "machine_health": health,
        "remaining_life": remaining_life,
        "maintenance_status": status
    }