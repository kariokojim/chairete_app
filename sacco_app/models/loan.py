from sacco_app.extensions import db
from datetime import datetime
import uuid


# =========================
# 🔹 LOAN APPLICATION
# =========================
class LoanApplication(db.Model):
    __tablename__ = 'loan_applications'

    id = db.Column(db.Integer, primary_key=True)

    member_no = db.Column(db.String(20), db.ForeignKey('members.member_no'), nullable=False)

    amount = db.Column(db.Numeric(12, 2), nullable=False)
    period = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(30), default='PENDING_GUARANTORS')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ LINK USING application_id
    guarantors = db.relationship(
        'LoanGuarantor',
        primaryjoin="LoanApplication.id==foreign(LoanGuarantor.application_id)",
        lazy=True
    )

    committee_approvals = db.relationship(
        'CreditCommitteeApproval',
        primaryjoin="LoanApplication.id==foreign(CreditCommitteeApproval.application_id)",
        lazy=True
    )


# =========================
# 🔹 DISBURSED LOAN
# =========================
class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    loan_no = db.Column(db.String(20), unique=True, nullable=False)

    member_no = db.Column(db.String(20), db.ForeignKey('members.member_no'))

    loan_account = db.Column(db.String(20), nullable=False)
    interest_account = db.Column(db.String(20), nullable=False)

    loan_amount = db.Column(db.Numeric(12, 2))
    balance = db.Column(db.Numeric(12, 2))
    interest_balance = db.Column(db.Numeric(12, 2), default=0)

    loan_period = db.Column(db.Integer)
    interest_rate = db.Column(db.Numeric(5, 2), default=12.0)

    disbursed_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    disbursed_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    loan_type = db.Column(db.String(20), default='normal', nullable=True)

    # ✅ GUARANTORS NOW LINKED TO LOAN PROPERLY
    guarantees = db.relationship('LoanGuarantor', backref='loan', lazy=True)

    schedules = db.relationship('LoanSchedule', back_populates='loan', cascade='all, delete-orphan')
    interests = db.relationship('LoanInterest', backref='loan', lazy=True)
    member = db.relationship('Member', back_populates='loans', lazy=True)


# =========================
# 🔹 GUARANTORS (FIXED)
# =========================
class LoanGuarantor(db.Model):
    __tablename__ = 'loan_guarantors'

    id = db.Column(db.Integer, primary_key=True)

    guarantor_no = db.Column(db.String(50), nullable=False)
    member_no = db.Column(db.String(50), nullable=False)

    # ✅ APPLICATION STAGE
    application_id = db.Column(db.Integer)

    # ✅ DISBURSED STAGE
    loan_no = db.Column(db.String(20), db.ForeignKey('loans.loan_no'))

    amount_guaranteed = db.Column(db.Numeric(12, 2))

    approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime)

    rejected = db.Column(db.Boolean, default=False)

    token = db.Column(db.String(100), unique=True, default=lambda: str(uuid.uuid4()))


# =========================
# 🔹 CREDIT COMMITTEE
# =========================
class CreditCommitteeApproval(db.Model):
    __tablename__ = "credit_committee_approvals"

    id = db.Column(db.Integer, primary_key=True)

    application_id = db.Column(db.Integer, nullable=False)

    approver_member_no = db.Column(db.String(20))
    approver_email = db.Column(db.String(120))
    approver_name = db.Column(db.String(50))
    approver_role = db.Column(db.String(20))

    approved = db.Column(db.Boolean, default=False)
    approved_at = db.Column(db.DateTime)

    token = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# =========================
# 🔹 LOAN SCHEDULE
# =========================
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


# =========================
# 🔹 LOAN INTEREST
# =========================
class LoanInterest(db.Model):
    __tablename__ = 'loan_interest'

    id = db.Column(db.Integer, primary_key=True)

    loan_no = db.Column(db.String(20), db.ForeignKey('loans.loan_no'))
    interest_account = db.Column(db.String(20), nullable=False)

    month = db.Column(db.String(7))

    interest_due = db.Column(db.Numeric(12, 2))
    interest_paid = db.Column(db.Numeric(12, 2), default=0)

    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class CreditCommitteeMember(db.Model):
    __tablename__ = "credit_committee_members"

    id = db.Column(db.Integer, primary_key=True)

    member_no = db.Column(
        db.String(20),
        db.ForeignKey("members.member_no"),
        unique=True,
        nullable=False
    )

    name = db.Column(db.String(120), nullable=False)

    role = db.Column(
        db.String(30),
        nullable=False
    )  # Chairperson, Secretary, Member

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )  # ACTIVE / INACTIVE

    join_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    left_date = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    member = db.relationship("Member")