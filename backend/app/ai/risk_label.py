def risk_label(score):

    if score >= 85:
        return "Critical"

    if score >= 65:
        return "High"

    if score >= 45:
        return "Medium"

    return "Safe"