from decimal import Decimal
from datetime import date
from sacco_app.extensions import db
from sacco_app.models.transactions import Transaction
from sacco_app.models.transactions import GLAccount
from sacco_app.utils.accounting import generate_txn_no, GL_MAP, apply_gl_effects, get_last_running_balance

def post_transaction(member_no, member_account_no, account_type, amount, tran_type, narration, reference, bank_txn_date, posted_by):
    """
    Post a unified transaction:
      - member entry (account_type in ['savings','share_capital','loan','interest'])
      - corresponding GL entry (account_type='gl', account_no = GL code)
    Returns txn_no.
    """
    # Validate
    if account_type not in GL_MAP:
        raise ValueError("Unknown account_type")

    amount = Decimal(amount)
    txn_no = generate_txn_no()
    entries = []

    # 1. Member-side entry
    # compute running balance for this member account (credit increases savings liability)
    # running balance convention: for savings we treat running_balance as member balance (increase for credit)
    last_balance = get_last_running_balance(member_account_no)  # Decimal
    if tran_type == 'credit':
        new_balance = last_balance + amount
    else:
        new_balance = last_balance - amount

    member_entry = Transaction(
        txn_no=txn_no,
        member_no=member_no,
        account_no=member_account_no,
        gl_code=None,
        account_type=account_type,
        tran_type=tran_type,
        amount=amount,
        running_balance=new_balance,
        reference=reference,
        narration=narration,
        bank_txn_date=bank_txn_date,
        posted_by=posted_by
    )
    entries.append(member_entry)

    # 2. GL side entry (opposite)
    mapping = GL_MAP[account_type]
    control_gl = mapping['control']       # e.g., 'GL1001' (Savings control)
    counterparty_gl = mapping['counterparty']  # e.g., 'GL5001' (Cash/Bank) - tweak per business logic

    # determine GL debit/credit relative to member tran_type:
    # if member tran_type is 'credit' (member balance increases), then:
    #   - GL side typically is: Debit counterparty (e.g., Bank), Credit control (Savings)
    # We'll produce one GL entry that balances the member entry
    # We create a single GL entry in unified model; convention: create the GL-side entry with opposite tran_type
    gl_tran_type = 'debit' if tran_type == 'credit' else 'credit'
    # Choose GL account to record under account_no (we'll use control_gl for GL entry)
    gl_entry = Transaction(
        txn_no=txn_no,
        member_no=None,
        account_no=control_gl,         # record to control account
        gl_code=control_gl,
        account_type='gl',
        tran_type=gl_tran_type,
        amount=amount,
        running_balance=None,
        reference=reference,
        narration=f"{narration} (GL auto for {account_type})",
        bank_txn_date=bank_txn_date,
        posted_by=posted_by
    )
    entries.append(gl_entry)

    # 3. Persist and apply GL balance updates in a transaction
    try:
        # Use DB transaction / locking to avoid race conditions
        with db.session.begin_nested():
            db.session.add_all(entries)
            db.session.flush()   # persist rows before GL adjustments

            # apply GL effects: debit counterparty, credit control (amount)
            # Which side should be debited/credited depends on business setup.
            # Here we apply (debit counterparty, credit control) when member credited
            if tran_type == 'credit':
                apply_gl_effects(counterparty_gl, control_gl, amount)
            else:
                # member debited (withdrawal) -> debit control, credit counterparty
                apply_gl_effects(control_gl, counterparty_gl, amount)

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return txn_no
