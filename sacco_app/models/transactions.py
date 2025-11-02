from ..extensions import db
from datetime import datetime
from sqlalchemy import Enum
from decimal import Decimal


# GL Account model (control accounts)
class GLAccount(db.Model):
    __tablename__ = "gl_accounts"
    id = db.Column(db.Integer, primary_key=True)
    gl_code = db.Column(db.String(20), unique=True, nullable=False)   # e.g. GL1001
    gl_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(20))    # Asset, Liability, Income, Expense
    balance = db.Column(db.Numeric(15,2), default=0)

    def __repr__(self):
        return f"<GLAccount {self.gl_code} {self.balance}>"
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    txn_no = db.Column(db.String(30), unique=True, nullable=False)  # Unique system TXN number (e.g., TXN0001)
    member_no = db.Column(db.String(20), db.ForeignKey('members.member_no'), nullable=True)
    account_no = db.Column(db.String(20), db.ForeignKey('sacco_accounts.account_number'), nullable=True)

    # this allows GL-side posting even if no member is tied directly
    gl_account = db.Column(db.String(20), nullable=True)  # e.g., 'GL1001' for Savings Control

    debit_amount = db.Column(db.Numeric(15, 2), nullable=False)
    credit_amount = db.Column(db.Numeric(15, 2), nullable=False)

    running_balance = db.Column(db.Numeric(15, 2), nullable=True)

    reference = db.Column(db.String(50), nullable=True)
    narration = db.Column(db.String(100), nullable=True)
    bank_txn_date = db.Column(db.Date, nullable=False)

    tran_type = db.Column(db.String(10), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_by = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f"<SavingsTransaction {self.txn_no} {self.tran_type.upper()} {self.amount}>"
class GLPosting(db.Model):
    __tablename__ = 'gl_postings'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    account_code = db.Column(db.String(50), nullable=False)
    debit = db.Column(db.Numeric(18,2), nullable=False, default=0.00)
    credit = db.Column(db.Numeric(18,2), nullable=False, default=0.00)
    narration = db.Column(db.String(255))
    
class GLTransaction(db.Model):
    __tablename__ = "gl_transactions"

    id = db.Column(db.Integer, primary_key=True)
    txn_no = db.Column(db.String(30), nullable=False)     # same as transaction txn_no
    gl_code = db.Column(db.String(20), db.ForeignKey("gl_accounts.gl_code"), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    tran_type = db.Column(db.String(10), nullable=False)  # 'debit' or 'credit'
    narration = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now())
    posted_by = db.Column(db.String(50), nullable=False)

    # Optional relationship to GLAccount
    gl_account = db.relationship("GLAccount", backref="gl_transactions")

