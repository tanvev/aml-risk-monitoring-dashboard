# src/str_pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_str(customer, scores, recent_tx, graph_img, out_path):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-40, "Suspicious Transaction Report (Simulated)")

    c.setFont("Helvetica", 10)
    c.drawString(50, height-65, f"Generated on: {datetime.utcnow()} UTC")

    y = height-100
    for k,v in customer.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Risk Summary")
    y -= 16

    c.setFont("Helvetica", 10)
    for k,v in scores.items():
        c.drawString(60, y, f"{k}: {v:.2f}")
        y -= 14

    c.drawImage(graph_img, 50, y-250, width=500, height=250)

    c.showPage()
    c.save()
