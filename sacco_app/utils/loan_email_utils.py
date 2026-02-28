from sacco_app.utils.email_utils import send_email

def send_loan_schedule_email(member, loan, pdf_buffer):
    body = f"""
Dear {member.name},

Congratulations!

Your loan has been successfully disbursed.

Loan Number: {loan.loan_no}
Loan Amount: KES {loan.loan_amount:,.2f}
Disbursement Date: {loan.disbursed_date}

Please find your repayment schedule attached.

Kindly ensure timely repayments.

PCEA Chairete SACCO
"""

    send_email(
        to_email=member.email,
        subject=f"Loan Disbursement - {loan.loan_no}",
        body=body,
        attachments=[
            (
                f"{loan.loan_no}_Schedule.pdf",
                pdf_buffer.getvalue(),
                "application/pdf"
            )
        ]
    )
