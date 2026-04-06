from datetime import datetime
from decimal import Decimal
from sacco_app.extensions import db
from datetime import datetime
from decimal import Decimal
from sacco_app.extensions import db


class MemberMonthlyBalance(db.Model):
    __tablename__ = "member_monthly_balances"

    id = db.Column(db.Integer, primary_key=True)

    member_no = db.Column(
        db.String(50),
        db.ForeignKey("members.member_no", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    year = db.Column(db.Integer, nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False, index=True)

    # 🔹 Savings movements
    opening_balance_savings = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    deposits = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    withdrawals = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    closing_balance_savings = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    # 🔹 Loan movements
    opening_balance_loan = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    loan_paid = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    interest_paid = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    closing_balance_loan = db.Column(
        db.Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # 🔗 Relationship
    member = db.relationship(
        "Member",
        primaryjoin="Member.member_no == MemberMonthlyBalance.member_no",
        backref=db.backref("monthly_balances", lazy=True, cascade="all, delete-orphan")
    )

    __table_args__ = (
        db.UniqueConstraint("member_no", "year", "month", name="uq_member_month_year"),
        db.CheckConstraint("month >= 1 AND month <= 12", name="check_valid_month"),
    )

    def __repr__(self):
        return (
            f"<MemberMonthlyBalance member_no={self.member_no} "
            f"{self.year}-{self.month:02d}>"
        )

    # 🔥 Business logic helpers

    def calculate_savings_closing(self):
        """
        closing_savings = opening + deposits - withdrawals
        """
        self.closing_balance_savings = (
            (self.opening_balance_savings or Decimal("0.00"))
            + (self.deposits or Decimal("0.00"))
            - (self.withdrawals or Decimal("0.00"))
        )

    def calculate_loan_closing(self):
        """
        closing_loan = opening - principal_paid
        (interest is tracked separately)
        """
        self.closing_balance_loan = (
            (self.opening_balance_loan or Decimal("0.00"))
            - (self.loan_paid or Decimal("0.00"))
        )

    def calculate_all(self):
        """
        Convenience method to compute everything
        """
        self.calculate_savings_closing()
        self.calculate_loan_closing()