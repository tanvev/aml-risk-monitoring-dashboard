from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_str_pdf(customer, alert, behavior, out_path):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-40, "Suspicious Transaction Report (Simulated)")

    c.setFont("Helvetica", 10)
    c.drawString(50, height-65, f"Generated on: {datetime.now()}")

    y = height - 100
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Customer Details")
    y -= 16

    c.setFont("Helvetica", 10)
    for k in ["customer_id", "branch", "income", "kyc_risk_score"]:
        c.drawString(60, y, f"{k}: {customer[k]}")
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Reason for Suspicion")
    y -= 16

    c.setFont("Helvetica", 10)
    c.drawString(60, y, alert["alert_reason"])
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Behavioral Change Summary")
    y -= 16

    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"Past txn count: {behavior[0]['txn_count']}")
    y -= 14
    c.drawString(60, y, f"Recent txn count: {behavior[1]['txn_count']}")

    c.showPage()
    c.save()
