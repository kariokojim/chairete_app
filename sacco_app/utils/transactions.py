# sacco_app/utils/transactions.py
from sacco_app.extensions import db
from sacco_app.models import Member, Transaction,GLAccount,GLTransaction,SaccoAccount
from datetime import datetime
from decimal import Decimal
import random, uuid

import datetime
import random
import string

def generate_txn_no(prefix="TXN"):
    """
    Generate a unique transaction number like: TXN20251018-AB1234
    """
    now = datetime.datetime.now().strftime("%Y%m%d")  # Date part
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    txn_no = f"{prefix}{now}-{random_part}"
    return txn_no


def post_savings(member_no, amount, user, narration, bank_txn_date):
    
    sacco_acct = SaccoAccount.query.filter_by(member_no=member_no).first()
    if not sacco_acct:
        raise ValueError(f"No Sacco account found for member {member_no}")
    account_no = sacco_acct.account_number  # ✅ fetched dynamically from DB

            # ✅ 2. Update SACCO account balance
    old_balance = sacco_acct.balance or Decimal('0.00')
    new_balance = old_balance + amount
    sacco_acct.balance = new_balance
    txn_no = f"TXN{uuid.uuid4().hex[:10].upper()}"  # e.g. TXN4A6F9B7C2E


    # 1️⃣ Post member savings record
    txn = Transaction(
        txn_no = txn_no,
        member_no=member_no,
        tran_type='CREDIT',
        amount=amount,
        running_balance=new_balance,
        account_no=account_no,
        posted_by=user,
        narration=narration,
        bank_txn_date=bank_txn_date,
        created_at=datetime.now()
    )
    db.session.add(txn)

    # 2️⃣ Get GL accounts
    savings_gl = GLAccount.query.filter_by(gl_code='SAVINGS').first()   # e.g. Savings Control
    bank_gl = GLAccount.query.filter_by(gl_code='BANK').first()      # e.g. Bank Account

    if not savings_gl or not bank_gl:
        raise Exception("Missing GL setup for savings or bank account")

    # 3️⃣ Create GL transactions (Double entry)
    gl_debit = GLTransaction(
        txn_no = txn_no,
        gl_code='SAVINGS',
        amount=amount,
        tran_type='DR',
        narration=f"Savings deposit by {member_no}: {narration}",
        posted_by=user,
        created_at=datetime.now()
    )

    gl_credit = GLTransaction(
        txn_no = txn_no,
        gl_code='BANK',
        amount=amount,
        tran_type ='CR',
        narration=f"Savings deposit by {member_no}: {narration}",
        posted_by=user,
        created_at=datetime.now()
    )

    db.session.add_all([gl_debit, gl_credit])
    db.session.commit()

    return txn.txn_no
def process_loan_repayment(member_no, amount, narration, bank_txn_date, posted_by):
    """
    Apply repayment only to installments whose due_date <= bank_txn_date.
    Allocation order: Interest -> Principal, then any remainder -> member savings.
    No prepayment of future installments.
    """
    from sacco_app import db
    from sacco_app.models import Member, Loan, LoanSchedule, SaccoAccount, Transaction
    from datetime import datetime
    from decimal import Decimal
    import uuid
    from sqlalchemy import or_, and_

    # --- Parse inputs
    txn_date = datetime.strptime(bank_txn_date, "%Y-%m-%d")
    txn_date_only = txn_date.date()
    amount = Decimal(str(amount))
    if amount <= 0:
        raise Exception("Repayment amount must be greater than zero.")

    # --- Entities
    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        raise Exception(f"Member {member_no} not found.")

    loan = Loan.query.filter_by(member_no=member_no, status='Active').first()
    if not loan:
        raise Exception("No active loan found for this member.")

    # Member & GL accounts
    member_loan_acc = SaccoAccount.query.filter_by(account_number=loan.loan_account).first()
    member_interest_acc = SaccoAccount.query.filter_by(account_number=loan.interest_account).first()
    member_savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()

    gl_cash = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
    gl_loan_control = SaccoAccount.query.filter_by(account_number='M000GL_LOAN').first()
    gl_interest_income = SaccoAccount.query.filter_by(account_number='M000GL_LN_INT').first()
    gl_savings_control = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()

    if not all([member_loan_acc, member_interest_acc, member_savings_acc, gl_cash, gl_loan_control, gl_interest_income, gl_savings_control]):
        raise Exception("One or more required accounts are missing (member or GL).")

    # --- Collect ONLY past-due (or partially paid) schedules as of txn_date
    schedules = LoanSchedule.query.filter(
        LoanSchedule.loan_no == loan.loan_no,
        LoanSchedule.due_date <= txn_date_only,
        or_(
            LoanSchedule.principal_paid < LoanSchedule.principal_due,
            LoanSchedule.interest_paid < LoanSchedule.interest_due
        )
    ).order_by(LoanSchedule.due_date, LoanSchedule.installment_no).all()

    # If nothing is due as of txn date, entire amount goes to savings
    apply_to_schedules = True
    if not schedules:
        apply_to_schedules = False

    remaining = amount
    txn_ref = f"TXN{uuid.uuid4().hex[:10].upper()}"
    transactions = []

    # --- 1) Dr CASH for total received
    gl_cash.balance += amount
    transactions.append(Transaction(
        txn_no=txn_ref,
        member_no=member_no,
        account_no=gl_cash.account_number,
        gl_account='CASH',
        tran_type='ASSET',
        debit_amount=amount,
        credit_amount=Decimal('0.00'),
        reference=txn_ref,
        narration=narration or f"Loan repayment received from {member_no}",
        bank_txn_date=txn_date,
        posted_by=posted_by,
        running_balance=gl_cash.balance
    ))

    # --- 2) Allocate to interest then principal for DUE/PARTIAL schedules only
    if apply_to_schedules and remaining > 0:
        for sch in schedules:
            if remaining <= 0:
                break

            # Interest first
            interest_due_left = (sch.interest_due - sch.interest_paid)
            if remaining > 0 and interest_due_left > 0:
                pay_interest = min(remaining, interest_due_left)
                sch.interest_paid += pay_interest
                remaining -= pay_interest

                # Member interest (Cr) and GL interest income (Cr)
                member_interest_acc.balance -= pay_interest
                transactions.append(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no=member_no,
                    account_no=member_interest_acc.account_number,
                    gl_account='MEMBER_INTEREST',
                    tran_type='ASSET',
                    debit_amount=Decimal('0.00'),
                    credit_amount=pay_interest,
                    reference=txn_ref,
                    narration=f"Interest repayment - inst {sch.installment_no}",
                    bank_txn_date=txn_date,
                    posted_by=posted_by,
                    running_balance=member_interest_acc.balance
                ))

                gl_interest_income.balance += pay_interest
                transactions.append(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no='M000GL',
                    account_no=gl_interest_income.account_number,
                    gl_account='INTEREST_INCOME',
                    tran_type='INCOME',
                    debit_amount=Decimal('0.00'),
                    credit_amount=pay_interest,
                    reference=txn_ref,
                    narration=f"Interest income from {member_no}",
                    bank_txn_date=txn_date,
                    posted_by=posted_by,
                    running_balance=gl_interest_income.balance
                ))

            # Then principal
            principal_due_left = (sch.principal_due - sch.principal_paid)
            if remaining > 0 and principal_due_left > 0:
                pay_principal = min(remaining, principal_due_left)
                sch.principal_paid += pay_principal
                loan.balance -= pay_principal
                remaining -= pay_principal

                # Member loan (Cr) and GL loan control (Cr)
                member_loan_acc.balance -= pay_principal
                transactions.append(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no=member_no,
                    account_no=member_loan_acc.account_number,
                    gl_account='MEMBER_LOAN',
                    tran_type='ASSET',
                    debit_amount=Decimal('0.00'),
                    credit_amount=pay_principal,
                    reference=txn_ref,
                    narration=f"Principal repayment - inst {sch.installment_no}",
                    bank_txn_date=txn_date,
                    posted_by=posted_by,
                    running_balance=member_loan_acc.balance
                ))

                gl_loan_control.balance -= pay_principal
                transactions.append(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no='M000GL',
                    account_no=gl_loan_control.account_number,
                    gl_account='LOAN_CONTROL',
                    tran_type='ASSET',
                    debit_amount=Decimal('0.00'),
                    credit_amount=pay_principal,
                    reference=txn_ref,
                    narration=f"Loan receivable reduction - {member_no}",
                    bank_txn_date=txn_date,
                    posted_by=posted_by,
                    running_balance=gl_loan_control.balance
                ))

            # Update schedule status
            if sch.principal_paid >= sch.principal_due and sch.interest_paid >= sch.interest_due:
                sch.status = 'PAID'
            else:
                sch.status = 'PARTIAL'

    # --- 3) Any remainder (no prepayment of future): send to savings
    if remaining > 0:
        member_savings_acc.balance += remaining
        gl_savings_control.balance += remaining

        transactions.append(Transaction(
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
            member_no=member_no,
            account_no=member_savings_acc.account_number,
            gl_account='SAVINGS',
            tran_type='LIABILITY',
            debit_amount=Decimal('0.00'),
            credit_amount=remaining,
            reference=txn_ref,
            narration=f"Excess funds to savings ({member_no})",
            bank_txn_date=txn_date,
            posted_by=posted_by,
            running_balance=member_savings_acc.balance
        ))
        transactions.append(Transaction(
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
            member_no='M000GL',
            account_no=gl_savings_control.account_number,
            gl_account='SAVINGS_CONTROL',
            tran_type='LIABILITY',
            debit_amount=Decimal('0.00'),
            credit_amount=remaining,
            reference=txn_ref,
            narration=f"Savings control posting for {member_no}",
            bank_txn_date=txn_date,
            posted_by=posted_by,
            running_balance=gl_savings_control.balance
        ))

    # --- 4) Close loan if fully settled
    if loan.balance <= 0:
        loan.status = 'Cleared'
        loan.balance = Decimal('0.00')

    # --- Commit
    db.session.add_all(transactions)
    db.session.commit()

    # Build a friendly message
    if apply_to_schedules:
        msg = f"Loan repayment of {amount:.2f} posted for {member_no} (as of {txn_date_only})."
        if remaining > 0:
            msg += f" Excess {remaining:.2f} moved to savings."
    else:
        msg = f"No installments due as of {txn_date_only}. Entire {amount:.2f} moved to savings."

    return msg


#######

def regenerate_remaining_schedules(loan, effective_date):
    """
    Recalculates remaining loan schedules after prepayment.
    Keeps past/paid installments unchanged.
    Shortens the loan period while keeping EMI constant.
    """
    from sacco_app import db
    from sacco_app.models import LoanSchedule
    from decimal import Decimal, ROUND_HALF_UP
    from dateutil.relativedelta import relativedelta

    # Get all unpaid or partial schedules
    unpaid_schedules = LoanSchedule.query.filter(
        LoanSchedule.loan_no == loan.loan_no,
        LoanSchedule.status != 'PAID'
    ).order_by(LoanSchedule.installment_no).all()

    if not unpaid_schedules:
        return

    # Use the EMI (total_due) from the first unpaid schedule
    sample_schedule = unpaid_schedules[0]
    old_emi = (sample_schedule.principal_due + sample_schedule.interest_due).quantize(Decimal('0.01'))
    principal_balance = loan.balance
    if principal_balance <= 0:
        # Loan is fully paid
        for s in unpaid_schedules:
            db.session.delete(s)
        db.session.flush()
        return

    # --- Remove old unpaid schedules
    for s in unpaid_schedules:
        db.session.delete(s)
    db.session.flush()

    # --- Rate setup
    annual_rate = Decimal(loan.interest_rate)
    monthly_rate = (annual_rate / Decimal(100)) / Decimal(12)

    # --- Determine new number of months (shorter term)
    # n = log(P / (P - r*B)) / log(1+r)
    # where:
    #   P = EMI
    #   r = monthly_rate
    #   B = balance
    import math
    if monthly_rate > 0:
        try:
            n = math.log(float(old_emi) / (float(old_emi) - float(monthly_rate * principal_balance))) / math.log(1 + float(monthly_rate))
        except (ZeroDivisionError, ValueError):
            n = 1
    else:
        n = principal_balance / old_emi

    n = math.ceil(n)
    remaining_months = max(1, n)

    # --- Rebuild shortened schedule
    principal_balance = principal_balance.quantize(Decimal('0.01'))
    first_due_date = effective_date + relativedelta(months=1)

    for i in range(1, remaining_months + 1):
        interest_due = (principal_balance * monthly_rate).quantize(Decimal('0.01'))
        principal_due = (old_emi - interest_due).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # On last month, pay off any balance rounding
        if i == remaining_months:
            principal_due = principal_balance
            total_due = (principal_due + interest_due).quantize(Decimal('0.01'))
        else:
            total_due = old_emi

        due_date = first_due_date + relativedelta(months=i - 1)

        schedule = LoanSchedule(
            loan_no=loan.loan_no,
            member_no=loan.member_no,
            installment_no=i,
            due_date=due_date,
            principal_due=principal_due,
            interest_due=interest_due,
            principal_paid=Decimal('0.00'),
            interest_paid=Decimal('0.00'),
            status='DUE'
        )
        db.session.add(schedule)

        principal_balance -= principal_due
        if principal_balance <= 0:
            break

    db.session.flush()

#LOAN PRE-PAYMENT

def process_loan_prepayment(member_no, amount, narration, bank_txn_date, posted_by):
    """
    Processes a loan prepayment:
    - Pays any due interest and principal first.
    - Remaining amount reduces the loan principal directly.
    - Regenerates future schedules after prepayment.
    """
    from sacco_app import db
    from sacco_app.models import Member, Loan, LoanSchedule, SaccoAccount, Transaction
    from datetime import datetime, date
    from decimal import Decimal
    from dateutil.relativedelta import relativedelta
    import uuid

    txn_date = datetime.strptime(bank_txn_date, '%Y-%m-%d')
    amount = Decimal(str(amount))
    if amount <= 0:
        raise Exception("Prepayment amount must be greater than zero.")

    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        raise Exception(f"Member {member_no} not found.")

    loan = Loan.query.filter_by(member_no=member_no, status='Active').first()
    if not loan:
        raise Exception("No active loan found for this member.")

    # Accounts
    member_loan_acc = SaccoAccount.query.filter_by(account_number=loan.loan_account).first()
    member_interest_acc = SaccoAccount.query.filter_by(account_number=loan.interest_account).first()
    gl_cash = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
    gl_loan_control = SaccoAccount.query.filter_by(account_number='M000GL_LOAN').first()
    gl_interest_income = SaccoAccount.query.filter_by(account_number='M000GL_LN_INT').first()

    if not all([member_loan_acc, member_interest_acc, gl_cash, gl_loan_control, gl_interest_income]):
        raise Exception("Missing GL or member accounts for this operation.")

    txn_ref = f"TXN{uuid.uuid4().hex[:10].upper()}"
    remaining = amount
    transactions = []

    # --- 1️⃣ Dr Cash (money received)
    gl_cash.balance += remaining
    transactions.append(Transaction(
        txn_no=txn_ref,
        member_no=member_no,
        account_no=gl_cash.account_number,
        gl_account='CASH',
        tran_type='ASSET',
        debit_amount=remaining,
        credit_amount=Decimal('0'),
        reference=txn_ref,
        narration=f"Loan prepayment received from {member_no}",
        bank_txn_date=txn_date,
        posted_by=posted_by,
        running_balance=gl_cash.balance
    ))

    # --- 2️⃣ Pay all due interest first
    due_schedules = LoanSchedule.query.filter(
        LoanSchedule.loan_no == loan.loan_no,
        LoanSchedule.due_date <= txn_date.date(),
        (LoanSchedule.interest_paid < LoanSchedule.interest_due) |
        (LoanSchedule.principal_paid < LoanSchedule.principal_due)
    ).order_by(LoanSchedule.installment_no).all()

    for schedule in due_schedules:
        if remaining <= 0:
            break

        # Pay interest first
        interest_due = schedule.interest_due - schedule.interest_paid
        if interest_due > 0:
            pay_interest = min(remaining, interest_due)
            schedule.interest_paid += pay_interest
            remaining -= pay_interest

            member_interest_acc.balance -= pay_interest
            gl_interest_income.balance += pay_interest

            transactions.append(Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                member_no=member_no,
                account_no=member_interest_acc.account_number,
                gl_account='MEMBER_INTEREST',
                tran_type='ASSET',
                debit_amount=Decimal('0'),
                credit_amount=pay_interest,
                reference=txn_ref,
                narration=f"Interest repayment installment {schedule.installment_no}",
                bank_txn_date=txn_date,
                posted_by=posted_by,
                running_balance=member_interest_acc.balance
            ))

        # Then pay principal
        if remaining > 0:
            principal_due = schedule.principal_due - schedule.principal_paid
            if principal_due > 0:
                pay_principal = min(remaining, principal_due)
                schedule.principal_paid += pay_principal
                loan.balance -= pay_principal
                member_loan_acc.balance -= pay_principal
                gl_loan_control.balance -= pay_principal
                remaining -= pay_principal

                transactions.append(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no=member_no,
                    account_no=member_loan_acc.account_number,
                    gl_account='MEMBER_LOAN',
                    tran_type='ASSET',
                    debit_amount=Decimal('0'),
                    credit_amount=pay_principal,
                    reference=txn_ref,
                    narration=f"Principal repayment installment {schedule.installment_no}",
                    bank_txn_date=txn_date,
                    posted_by=posted_by,
                    running_balance=member_loan_acc.balance
                ))

        # Update schedule status
        if schedule.principal_paid >= schedule.principal_due and schedule.interest_paid >= schedule.interest_due:
            schedule.status = 'PAID'
        elif schedule.principal_paid > 0 or schedule.interest_paid > 0:
            schedule.status = 'PARTIAL'

    # --- 3️⃣ Apply remaining amount as prepayment (reduce principal directly)
    if remaining > 0:
        loan.balance -= remaining
        if loan.balance < 0:
            loan.balance = Decimal('0.00')

        member_loan_acc.balance -= remaining
        gl_loan_control.balance -= remaining

        transactions.append(Transaction(
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
            member_no=member_no,
            account_no=member_loan_acc.account_number,
            gl_account='MEMBER_LOAN',
            tran_type='ASSET',
            debit_amount=Decimal('0'),
            credit_amount=remaining,
            reference=txn_ref,
            narration="Loan prepayment (principal reduction)",
            bank_txn_date=txn_date,
            posted_by=posted_by,
            running_balance=member_loan_acc.balance
        ))

    # --- 4️⃣ Commit repayment before restructuring
    db.session.add_all(transactions)
    db.session.flush()

    # --- 5️⃣ Regenerate remaining future schedules
    regenerate_remaining_schedules(loan, txn_date.date())

    db.session.commit()

    # --- 6️⃣ Close loan if fully cleared
    if loan.balance <= 0:
        loan.status = 'Cleared'
        db.session.commit()

    return f"Loan prepayment of {amount:.2f} processed successfully. Schedules updated."
#Would you like the regeneration logic to shorten the loan period (same installment, fewer months)
