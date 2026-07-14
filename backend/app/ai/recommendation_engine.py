def recommendation(score):

    if score >= 85:
        return "Immediate shutdown and evacuation."

    if score >= 65:
        return "Reduce production and inspect equipment."

    if score >= 45:
        return "Increase monitoring frequency."

    return "Normal operation."