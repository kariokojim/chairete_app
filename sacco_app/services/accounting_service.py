from sqlalchemy import func
from datetime import date
from sacco_app.extensions import db
from sacco_app.models.transactions import Transaction
from sacco_app.models.gl_opening_balance import GLOpeningBalance


def generate_opening_balances(year: int):
    """
    Create opening balances for `year` using closing balances from year-1.
    Will NOT overwrite existing opening balances.
    """
    prev_year = year - 1

    start = date(prev_year, 1, 1)
    end = date(prev_year, 12, 31)

    balances = (
        db.session.query(
            Transaction.gl_account,
            (func.coalesce(func.sum(Transaction.debit_amount), 0) -
             func.coalesce(func.sum(Transaction.credit_amount), 0)).label("closing_balance")
        )
        .filter(Transaction.created_at.between(start, end))
        .group_by(Transaction.gl_account)
        .all()
    )

    created = 0

    for gl_account, closing in balances:
        exists = GLOpeningBalance.query.filter_by(
            gl_account=gl_account,
            year=year
        ).first()

        if exists:
            continue  # 🔒 never overwrite

        db.session.add(
            GLOpeningBalance(
                gl_account=gl_account,
                year=year,
                opening_balance=closing or 0
            )
        )
        created += 1

    db.session.commit()
    return created
