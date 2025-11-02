import uuid
from datetime import date
from decimal import Decimal
from sacco_app.extensions import db
from sacco_app.models.transactions import Transaction, GLAccount
from sacco_app.models.member import Member  # adjust import to your structure
from sqlalchemy import func, select, text

# Map account_type -> GL control codes (customize to your chart of accounts)
GL_MAP = {
    "savings": { "control": "GL1001", "counterparty": "GL5001" },       # counterparty often Cash/Bank
    "share_capital": { "control": "GL2001", "counterparty": "GL5001" },
    "loan": { "control": "GL3001", "counterparty": "GL5001" },
    "interest": { "control": "GL4001", "counterparty": "GL5001" }
}

def generate_txn_no():
    return f"TXN-{uuid.uuid4().hex[:10].upper()}"

def get_last_running_balance(account_no):
    """Return last running_balance for account_no (member account)."""
    last = db.session.query(Transaction.running_balance).filter_by(account_no=account_no).order_by(Transaction.id.desc()).limit(1).scalar()
    return Decimal(last) if last is not None else Decimal('0.00')

def apply_gl_effects(debit_code, credit_code, amount):
    """
    Update GLAccount balances. This function expects proper GL account rows exist.
    It adjusts balances according to account type conventions.
    """
    # lock both GL rows for update to avoid race conditions
    debit_acc = db.session.execute(select(GLAccount).where(GLAccount.gl_code == debit_code).with_for_update()).scalar_one_or_none()
    credit_acc = db.session.execute(select(GLAccount).where(GLAccount.gl_code == credit_code).with_for_update()).scalar_one_or_none()

    if not debit_acc or not credit_acc:
        raise ValueError("GL accounts not found")

    # Accounting rule: for Assets/Expenses, debits increase balances; for Liabilities/Income/Equity, credits increase balances.
    # We assume GLAccount.account_type stores 'Asset', 'Liability', 'Income', 'Expense', 'Equity'
    def adjust(acc, delta, is_debit):
        # if is_debit True -> apply debit; else apply credit
        typ = (acc.account_type or "").lower()
        if is_debit:
            if typ in ('asset', 'expense'):
                acc.balance = acc.balance + delta
            else:
                acc.balance = acc.balance - delta
        else:
            # credit
            if typ in ('liability', 'income', 'equity'):
                acc.balance = acc.balance + delta
            else:
                acc.balance = acc.balance - delta

    adjust(debit_acc, amount, is_debit=True)
    adjust(credit_acc, amount, is_debit=False)
    db.session.flush()
