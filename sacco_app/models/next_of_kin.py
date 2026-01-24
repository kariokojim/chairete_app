from sacco_app.extensions import db

class NextOfKin(db.Model):
    __tablename__ = 'next_of_kin'

    id = db.Column(db.Integer, primary_key=True)

    member_no = db.Column(
        db.String(20),
        db.ForeignKey('members.member_no', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    full_name = db.Column(db.String(150), nullable=False)
    relationship = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    id_number = db.Column(db.String(30))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Optional relationship back to Member
    member = db.relationship(
        'Member',
        backref=db.backref('next_of_kin', uselist=False, cascade='all, delete-orphan')
    )

    def __repr__(self):
        return f"<NextOfKin {self.full_name} ({self.member_no})>"
