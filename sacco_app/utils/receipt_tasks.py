from sacco_app import db
from sacco_app.utils.receipt_mailer import send_receipt_email
from sacco_app.utils.receipts import generate_receipt_pdf
from sqlalchemy import text

def send_receipt_background(app, member, txn, receipt_no):
    with app.app_context():
        pdf = generate_receipt_pdf(member, txn, receipt_no)

        send_receipt_email(member, txn, pdf, receipt_no)

        db.session.execute(text("""
            INSERT INTO receipt_logs (transaction_id, member_no, email, receipt_no)
            VALUES (:t, :m, :e, :r)
        """), {
            "t": txn.id,
            "m": member.member_no,
            "e": member.email,
            "r": receipt_no
        })
        db.session.commit()
