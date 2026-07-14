import os
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from app.ai.risk_engine import calculate_risk_score
from app.ai.recommendation_engine import recommendation
from app.ai.alert_engine import generate_alerts


REPORT_FOLDER = "reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_pdf_report(sectors):
    filename = os.path.join(
        REPORT_FOLDER,
        f"Safety_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    )

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>AI Industrial Safety Monitoring Report</b>", styles["Title"])
    )

    story.append(Spacer(1, 20))

    for sector in sectors:
        score = calculate_risk_score(sector)

        story.append(
            Paragraph(f"<b>Sector:</b> {sector.name}", styles["Heading2"])
        )

        story.append(
            Paragraph(f"Temperature: {sector.temperature} °C", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Gas: {sector.gas}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Pressure: {sector.pressure}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Workers: {sector.workers_present}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"Maintenance: {sector.maintenance}", styles["BodyText"])
        )

        story.append(
            Paragraph(f"<b>Risk Score:</b> {score}", styles["BodyText"])
        )

        story.append(
            Paragraph(
                f"<b>Recommendation:</b> {recommendation(score)}",
                styles["BodyText"],
            )
        )

        alerts = generate_alerts(sector)

        story.append(
            Paragraph("<b>Alerts:</b>", styles["Heading3"])
        )

        for alert in alerts:
            story.append(
                Paragraph(
                    f"- {alert['type']}: {alert['message']}",
                    styles["BodyText"],
                )
            )

        story.append(Spacer(1, 20))

    doc.build(story)

    return filename