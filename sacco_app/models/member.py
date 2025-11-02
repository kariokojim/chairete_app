from sacco_app.extensions import db
from datetime import date,datetime
from sqlalchemy import event

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    member_no = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    dob = db.Column(db.Date)
    id_no = db.Column(db.String(20))
    congregation = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    joined_date = db.Column(db.Date, default=date.today)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    savings = db.relationship('SavingsAccount', uselist=False, back_populates='member')
    loans = db.relationship('Loan', back_populates='member',lazy=True)
    loan_schedules = db.relationship('LoanSchedule', back_populates='member', cascade="all, delete-orphan")

class SavingsAccount(db.Model):
    __tablename__ = 'savings_accounts'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    balance = db.Column(db.Numeric(18,2), nullable=False, default=0.00)
    member = db.relationship('Member', back_populates='savings')
    
class SaccoAccount(db.Model):
    __tablename__ = 'sacco_accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    member_no = db.Column(db.String(10), db.ForeignKey('members.member_no'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Numeric(15, 2), default=0.00)
    limit = db.Column(db.Numeric(15, 2), default=1000000.00,nullable=True)
    status = db.Column(db.String(15), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(50), nullable=False)

    # Relationship: link back to Member by member_no
    member = db.relationship('Member', backref=db.backref('accounts', lazy=True), foreign_keys=[member_no])

    def __repr__(self):
        return f"<SaccoAccount {self.account_number} ({self.account_type})>"
        
def generate_account_number(member_no, account_type):
    # Map account type to suffix
    suffix_map = {
        "Savings": "SV",
        "Interest": "INT",
        "Share Capital": "SCS",
        "Loan Liability": "LNL"
    }

    suffix = suffix_map.get(account_type, "UNK")

    from sacco_app.models.member import SaccoAccount  # avoid circular import
    count = SaccoAccount.query.filter_by(member_no=member_no, account_type=account_type).count() + 1

    return f"{member_no}_{suffix}{count}"


@event.listens_for(Member, 'after_insert')
def create_default_accounts(mapper, connection, target):
    connection.execute(SaccoAccount.__table__.insert(), [
        {
            'member_no': target.member_no,
            'account_number': f"{target.member_no}_SAVINGS",
            'account_type': 'SAVINGS',
            'balance': 0.0,
            'interest_rate': 0.0,
            'limit': 100000000.00,
            'status': 'active',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'created_by': target.created_by
        },
        {
            'member_no': target.member_no,
            'account_number': f"{target.member_no}_SHARE_CAP",
            'account_type': 'EQUITY',
            'balance': 0.0,
            'interest_rate': 0.0,
            'limit': 100000000.00,
            'status': 'active',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'created_by': target.created_by
        }
    ])
