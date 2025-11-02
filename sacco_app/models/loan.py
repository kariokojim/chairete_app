from sacco_app.extensions import db
from datetime import datetime, timedelta
from decimal import Decimal


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String(20), unique=True, nullable=False)
    member_no = db.Column(db.String(20), db.ForeignKey('members.member_no'))
    loan_account = db.Column(db.String(20), nullable=False)
    interest_account = db.Column(db.String(20), nullable=False)
    loan_amount = db.Column(db.Numeric(12, 2))
    balance = db.Column(db.Numeric(12, 2))
    interest_balance = db.Column(db.Numeric(12, 2), default=0)  # 👈 add this
    loan_period = db.Column(db.Integer)  # months
    interest_rate = db.Column(db.Numeric(5, 2), default=12.0)
    disbursed_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    disbursed_by= db.Column(db.Integer, db.ForeignKey('users.id'))
    guarantees = db.relationship('LoanGuarantor', backref='loan', lazy=True)
    schedules = db.relationship('LoanSchedule', backref='loan', lazy=True)
    interests = db.relationship('LoanInterest', backref='loan', lazy=True)
    member = db.relationship('Member', back_populates='loans', lazy=True)
    loan_type = db.Column(db.String(20), default='normal', nullable=True)

    schedules = db.relationship('LoanSchedule', back_populates='loan', cascade='all, delete-orphan')


class LoanGuarantor(db.Model):
    __tablename__ = 'loan_guarantors'
    id = db.Column(db.Integer, primary_key=True)
    member_no = db.Column(db.String(20), db.ForeignKey('members.member_no'))
    loan_no = db.Column(db.String(20), db.ForeignKey('loans.loan_no'))
    guarantor_no = db.Column(db.String(20))
    amount_guaranteed = db.Column(db.Numeric(12, 2))

class LoanSchedule(db.Model):
    __tablename__ = 'loan_schedules'
    id = db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String(20), db.ForeignKey('loans.loan_no'))
    due_date = db.Column(db.Date)
    member_no = db.Column(db.String(20), db.ForeignKey('members.member_no'))
    installment_no = db.Column(db.Integer)
    principal_due = db.Column(db.Numeric(12, 2))
    interest_due = db.Column(db.Numeric(12, 2))
    principal_paid = db.Column(db.Numeric(12, 2), default=0)
    interest_paid = db.Column(db.Numeric(12, 2), default=0)
    status = db.Column(db.String(20), default='Pending')
    principal_balance = db.Column(db.Numeric(12, 2))
    
    loan = db.relationship('Loan', back_populates='schedules')
    member = db.relationship('Member', back_populates='loan_schedules')

class LoanInterest(db.Model):
    __tablename__ = 'loan_interest'
    id = db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String(20), db.ForeignKey('loans.loan_no'))
    interest_account = db.Column(db.String(20), nullable=False)
    month = db.Column(db.String(7))  # e.g. "2025-10"
    interest_due = db.Column(db.Numeric(12, 2))
    interest_paid = db.Column(db.Numeric(12, 2), default=0)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
