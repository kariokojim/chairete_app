from sacco_app.utils.email_utils import send_email
def send_receipt_email(member, txn, pdf_buffer, receipt_no):
    body = f"""
        Dear {member.name},

        Thank you for your deposit with PCEA Chairete SACCO.

        Receipt No: {receipt_no}
        Amount: KES {txn.credit_amount:,.2f}
        Reference: {txn.reference}

        Please find your receipt attached.

        PCEA Chairete SACCO
        """

    send_email(
        to_email=member.email,
        subject=f"SACCO Receipt - {receipt_no}",
        body=body,
        attachments=[
            (f"{receipt_no}.pdf", pdf_buffer.getvalue(), "application/pdf")
        ]
    )
