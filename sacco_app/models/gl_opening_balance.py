from sacco_app.extensions import db

class GLOpeningBalance(db.Model):
    __tablename__ = 'gl_opening_balances'

    id = db.Column(db.Integer, primary_key=True)
    gl_account = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    opening_balance = db.Column(db.Numeric(14, 2), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('gl_account', 'year', name='uq_gl_year'),
    )
