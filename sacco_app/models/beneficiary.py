from sacco_app.extensions import db

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'

    id = db.Column(db.Integer, primary_key=True)

    member_no = db.Column(
        db.String(20),
        db.ForeignKey('members.member_no', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    full_name = db.Column(db.String(150), nullable=False)
    relationship = db.Column(db.String(50))
    contact = db.Column(db.String(20))

    percentage = db.Column(
        db.Numeric(5, 2),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    member = db.relationship(
        'Member',
        backref=db.backref('beneficiaries', lazy='dynamic', cascade='all, delete-orphan')
    )

    def __repr__(self):
        return f"<Beneficiary {self.full_name} {self.percentage}% ({self.member_no})>"
