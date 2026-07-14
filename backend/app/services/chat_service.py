from sqlalchemy.orm import Session

from app.models.sector import Sector
from app.ai.gemini_service import ask_gemini
from app.ai.risk_engine import calculate_risk_score
from app.ai.recommendation_engine import recommendation
from app.ai.predictive_maintenance import predictive_maintenance
from app.ai.incident_prediction import predict_incident
from app.ai.alert_engine import generate_alerts


def generate_chat_response(message: str, db: Session):

    original_message = message
    message = message.lower()

    sectors = db.query(Sector).all()

    # ======================================
    # Plant Summary
    # ======================================

    if "summary" in message:

        total = len(sectors)

        avg_risk = 0

        for sector in sectors:
            avg_risk += calculate_risk_score(sector)

        avg_risk = round(avg_risk / total, 2) if total else 0

        return (
            f"Plant Summary\n\n"
            f"Total Sectors : {total}\n"
            f"Average Risk : {avg_risk}\n"
            f"Overall Plant Status : "
            f"{'Safe' if avg_risk < 50 else 'Attention Required'}"
        )

    # ======================================
    # Most Dangerous Sector
    # ======================================

    if "danger" in message or "dangerous" in message:

        dangerous = max(
            sectors,
            key=lambda s: calculate_risk_score(s),
        )

        risk = calculate_risk_score(dangerous)

        return (
            f"Most Dangerous Sector\n\n"
            f"{dangerous.name}\n"
            f"Risk Score : {risk}\n"
            f"Recommendation : {recommendation(risk)}"
        )

    # ======================================
    # Maintenance
    # ======================================

    if "maintenance" in message:

        answer = []

        for sector in sectors:
            answer.append(
                f"{sector.name} : "
                f"{predictive_maintenance(sector)}"
            )

        return "\n".join(answer)

    # ======================================
    # Incident Prediction
    # ======================================

    if "incident" in message or "accident" in message:

        answer = []

        for sector in sectors:
            answer.append(
                f"{sector.name} : "
                f"{predict_incident(sector)}"
            )

        return "\n".join(answer)

    # ======================================
    # Alerts
    # ======================================

    if "alert" in message:

        text = []

        for sector in sectors:

            alerts = generate_alerts(sector)

            for alert in alerts:
                text.append(
                    f"{sector.name} : {alert['message']}"
                )

        if not text:
            return "No active alerts."

        return "\n".join(text)

    # ======================================
    # Sector Search
    # ======================================

    for sector in sectors:

        if sector.name.lower() in message:

            risk = calculate_risk_score(sector)

            return (
                f"Sector : {sector.name}\n\n"
                f"Temperature : {sector.temperature}\n"
                f"Gas : {sector.gas}\n"
                f"Pressure : {sector.pressure}\n"
                f"Workers : {sector.workers_present}\n"
                f"Risk Score : {risk}\n"
                f"Recommendation : {recommendation(risk)}"
            )

    # ======================================
    # Gemini AI Fallback
    # ======================================

    context = []

    for sector in sectors:

        context.append(
            f"""
Sector: {sector.name}
Temperature: {sector.temperature}
Gas: {sector.gas}
Pressure: {sector.pressure}
Workers: {sector.workers_present}
Risk Score: {calculate_risk_score(sector)}
Maintenance: {predictive_maintenance(sector)}
Incident Prediction: {predict_incident(sector)}
"""
        )

    prompt = f"""
You are an AI Industrial Safety Assistant.

Below is the current plant status.

{''.join(context)}

User Question:
{original_message}

Answer professionally with practical industrial safety recommendations.
"""

    return ask_gemini(prompt)