def calculate_machine_health(
    temperature: float,
    gas: float,
    pressure: float,
    maintenance: str,
):
    """
    Calculate machine health and maintenance status.
    """

    health = 100

    # Temperature impact
    if temperature > 80:
        health -= 20
    elif temperature > 70:
        health -= 10

    # Gas impact
    if gas > 70:
        health -= 20
    elif gas > 50:
        health -= 10

    # Pressure impact
    if pressure > 10:
        health -= 20
    elif pressure > 8:
        health -= 10

    # Maintenance impact
    if maintenance.lower() == "inactive":
        health -= 20

    # Clamp between 0 and 100
    health = max(0, min(health, 100))

    # Remaining life estimation
    remaining_life = int((health / 100) * 30)

    # Maintenance status
    if health >= 80:
        status = "Healthy"
    elif health >= 60:
        status = "Maintenance Due Soon"
    elif health >= 40:
        status = "Urgent Maintenance"
    else:
        status = "Critical"

    return {
        "machine_health": health,
        "remaining_life": remaining_life,
        "maintenance_status": status,
    }