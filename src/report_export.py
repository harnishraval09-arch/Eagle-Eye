"""Court-style PDF export for the reviewable mock case."""

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


def build_report(case):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=.65*inch, leftMargin=.65*inch, topMargin=.55*inch, bottomMargin=.55*inch)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11, textColor=colors.HexColor("#526375")))
    styles.add(ParagraphStyle(name="Heading", parent=styles["Heading2"], fontSize=13, leading=16, textColor=colors.HexColor("#142338"), spaceBefore=10, spaceAfter=6))
    story = [Paragraph("EAGLE EYE · FORENSIC DOCUMENT EXAMINATION", styles["Title"]), Paragraph("Expert decision-support report · examiner review required", styles["Small"]), Spacer(1, 14)]
    obs = case["observations"]
    story.append(Paragraph("Case identification", styles["Heading"]))
    story.append(Table([["Case number", obs["case_number"]], ["Document type", obs["document_type"]], ["Issuing body", obs["issuing_body"]], ["Examiner", obs["examiner"]]], colWidths=[1.35*inch, 5.6*inch], style=TableStyle([("GRID", (0,0), (-1,-1), .35, colors.HexColor("#dbe3ea")), ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f4f7f9")), ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 9), ("VALIGN", (0,0), (-1,-1), "TOP"), ("PADDING", (0,0), (-1,-1), 7)])))
    story.append(Paragraph("Automated findings", styles["Heading"]))
    rows = [["Check", "Signal", "Observation"]] + [[f["name"], f["status"], f["detail"]] for f in case["engine"]["flags"]]
    story.append(Table(rows, colWidths=[1.5*inch, .8*inch, 4.65*inch], style=TableStyle([("GRID", (0,0), (-1,-1), .35, colors.HexColor("#dbe3ea")), ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0b1828")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTSIZE", (0,0), (-1,-1), 8.5), ("VALIGN", (0,0), (-1,-1), "TOP"), ("PADDING", (0,0), (-1,-1), 6)])))
    story.append(Paragraph("Bob / MCP orchestration", styles["Heading"]))
    for step in case["steps"]:
        story.append(Paragraph(f"<b>{step['label']}</b> — {step['detail']}", styles["Small"]))
    story.append(Paragraph("Interpretive statement", styles["Heading"]))
    story.append(Paragraph("The automated analysis produced convergent indicators consistent with a Typography Forgery / Cut-and-paste anomaly. This report is a decision-support artifact. It is not a verdict, and the examiner must review, amend where appropriate, and sign before use.", styles["BodyText"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Examiner signature: ____________________________________    Date: __________________", styles["BodyText"]))
    doc.build(story)
    return buf.getvalue()
