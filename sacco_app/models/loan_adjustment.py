from sacco_app.extensions import db
from datetime import datetime, timedelta
from decimal import Decimal



class LoanAdjustment(db.Model):
    __tablename__ = "loan_adjustments"

    id = db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String, db.ForeignKey('loans.id'), nullable=False)
    member_no = db.Column(db.String, db.ForeignKey('members.id'), nullable=False)

    amount = db.Column(db.Numeric(12,2), nullable=False)
    adjustment_type = db.Column(db.String(10), nullable=False)  # increase / decrease
    narration = db.Column(db.String(255))

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)