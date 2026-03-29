from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def export_report_to_pdf(report_data: dict, filename: str):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "Classroom Usage Report")
    y = 700
    for key, value in report_data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20
    c.save()
