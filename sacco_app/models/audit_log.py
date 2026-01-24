from sacco_app.extensions import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)

    entity_type = db.Column(db.String(50))     # MEMBER, LOAN, NOK, BENEFICIARY
    entity_id = db.Column(db.String(50))       # member_no, loan_no
    event_type = db.Column(db.String(20))      # CREATE, UPDATE, DELETE

    before_data = db.Column(db.JSON)
    after_data = db.Column(db.JSON)

    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', lazy='joined')

    def __repr__(self):
        return f"<Audit {self.action} {self.entity_type}:{self.entity_id}>"


