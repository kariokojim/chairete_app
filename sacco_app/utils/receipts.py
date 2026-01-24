from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
from flask import current_app
import os

def generate_receipt_pdf(member, txn, receipt_no):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    blue = colors.HexColor("#003399")

    header_style = ParagraphStyle(
        "header",
        fontSize=14,
        textColor=blue,
        spaceAfter=6
    )

    contact_style = ParagraphStyle(
        "contact",
        fontSize=10,
        textColor=blue,
        spaceAfter=10
    )

    footer_style = ParagraphStyle(
        "footer",
        fontSize=10,
        textColor=blue,
        spaceBefore=15
    )

    story = []

    # --- Logo ---
    logo_path = os.path.join(current_app.root_path, "static/img", "logo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=80, height=60))
        story.append(Spacer(1, 6))
    # --- Blue divider ---
    story.append(Table([[""]], colWidths=[450], style=[
        ("LINEABOVE", (0,0), (-1,-1), 2, blue)
    ]))
    # --- SACCO Name ---
    story.append(Paragraph("PCEA CHAIRETE SACCO", header_style))
    story.append(Paragraph("MEMBER TRANSACTION RECIEPT", header_style))

    # --- Contact ---
    story.append(Paragraph("mobile: 0726 361261 | Email: info@chairetesacco.co.ke", contact_style))

    # --- Blue divider ---
    story.append(Table([[""]], colWidths=[450], style=[
        ("LINEABOVE", (0,0), (-1,-1), 2, blue)
    ]))
    story.append(Spacer(1, 12))

    # --- Receipt Meta ---
    meta = [
        ["Receipt No", receipt_no],
        ["Date", txn.bank_txn_date.strftime('%d %b %Y')],
        ["Served By", txn.posted_by]
    ]
    story.append(Table(meta, colWidths=[150, 300]))
    story.append(Spacer(1, 15))

    # --- Transaction Details ---
    data = [
        ["Member No", member.member_no],
        ["Member Name", f"{member.name}"],
        ["Amount", f"KES {txn.credit_amount:,.2f}"],
        ["Your Balance After", f"KES {txn.running_balance:,.2f}"],
        ["Reference", txn.reference],
        ["Narration", txn.narration],
    ]

    story.append(Table(data, colWidths=[150, 300]))
    story.append(Spacer(1, 15))

    # --- Blue divider before footer ---
    story.append(Table([[""]], colWidths=[450], style=[
        ("LINEABOVE", (0,0), (-1,-1), 2, blue)
    ]))

    # --- Footer message ---
    story.append(Paragraph(
        "Thank you for banking with PCEA Chairete SACCO. This is an electronically generated receipt.",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
