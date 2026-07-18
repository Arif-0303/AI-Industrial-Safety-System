from app.ai.risk_engine import calculate_risk_score


def generate_alerts(sector):

    risk = calculate_risk_score(sector)

    # ==========================================================
    # AI ALERT
    # ==========================================================

    ai_status = "SAFE"

    cause = "All industrial parameters are operating normally."

    risk_description = "No immediate industrial safety risk detected."

    action = "Continue normal operation."

    findings = []

    # ----------------------------------------------------------

    if sector.temperature >= 90:

        findings.append(
            f"Temperature reached {sector.temperature}°C."
        )

    if sector.gas >= 70:

        findings.append(
            f"Gas concentration reached {sector.gas} ppm."
        )

    if sector.pressure >= 10:

        findings.append(
            f"Pressure reached {sector.pressure} bar."
        )

    if sector.maintenance == "Inactive":

        findings.append(
            "Maintenance overdue."
        )

    if sector.workers_present >= 8:

        findings.append(
            f"{sector.workers_present} workers currently inside the sector."
        )

    # ----------------------------------------------------------

    if risk >= 80:

        ai_status = "CRITICAL"

        cause = " | ".join(findings)

        risk_description = (
            "Multiple hazardous industrial conditions detected. "
            "Immediate accident or explosion risk exists."
        )

        action = (
            f"Evacuate all {sector.workers_present} workers immediately. "
            "Isolate equipment. Dispatch emergency response team."
        )

    elif risk >= 60:

        ai_status = "HIGH"

        cause = " | ".join(findings)

        risk_description = (
            "Sector is approaching critical operating conditions."
        )

        action = (
            "Inspect equipment and reduce operational load."
        )

    # ==========================================================
    # CCTV INSIGHT (ONLY CRITICAL)
    # ==========================================================

    cctv_status = "NORMAL"

    vision_findings = []

    # Temporary simulation
    # Replace later with YOLO/OpenCV output

    if risk >= 80:

        if sector.temperature >= 95:

            cctv_status = "CRITICAL"

            vision_findings.append(
                "• Dense Smoke Detected"
            )

        if getattr(sector, "helmet_violation", False):

            cctv_status = "CRITICAL"

            vision_findings.append(
                "• Worker Without Helmet"
            )

        if getattr(sector, "vest_violation", False):

            cctv_status = "CRITICAL"

            vision_findings.append(
                "• Worker Without Safety Vest"
            )

        if getattr(sector, "restricted_area", False):

            cctv_status = "CRITICAL"

            vision_findings.append(
                "• Restricted Area Intrusion"
            )

    if len(vision_findings) == 0:

        vision_findings.append(
            "No critical visual hazard detected."
        )

    return {

        "risk_score": risk,

        "ai_alert": {

            "status": ai_status,

            "cause": cause,

            "risk": risk_description,

            "action": action,

        },

        "cctv": {

            "status": cctv_status,

            "message": "\n".join(vision_findings)

        }

    }