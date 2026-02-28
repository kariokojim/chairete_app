from sacco_app.extensions import db
from datetime import date,datetime
from sqlalchemy import event


class MemberMonthlyBalance(db.Model):
    __tablename__ = "member_monthly_balances"

    id = db.Column(db.Integer, primary_key=True)

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)

    opening_balance = db.Column(db.Numeric(14, 2), default=0)
    deposits = db.Column(db.Numeric(14, 2), default=0)
    withdrawals = db.Column(db.Numeric(14, 2), default=0)
    closing_balance = db.Column(db.Numeric(14, 2), default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    member = db.relationship("Member", backref="monthly_balances")

    __table_args__ = (
        db.UniqueConstraint("member_id", "year", "month"),
    )

