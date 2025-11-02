import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from sacco_app.extensions import db
from sacco_app.models import Member, SaccoAccount
from sacco_app.models.loan import Loan, LoanGuarantor, LoanSchedule


def disburse_loan(member_no, amount, period_months, guarantors_data, interest_rate=12.0):
    """
    guarantors_data = [
        {"guarantor_no": "M0002", "amount_guaranteed": 10000},
        {"guarantor_no": "M0003", "amount_guaranteed": 15000},
    ]
    """
    # 1️⃣ Fetch applicant savings
    sacco_acct = SaccoAccount.query.filter_by(member_no=member_no).first()
    if not sacco_acct:
        raise ValueError("Member has no SACCO savings account")

    savings_balance = Decimal(sacco_acct.balance or 0)

    # 2️⃣ Rule: Loan <= 3 × savings
    if Decimal(amount) > savings_balance * 3:
        raise ValueError(f"Loan exceeds 3x savings limit. Max allowed: {savings_balance * 3}")

    # 3️⃣ Rule: Entire loan must be guaranteed
    total_guaranteed = sum([Decimal(g['amount_guaranteed']) for g in guarantors_data])
    if total_guaranteed < Decimal(amount):
        raise ValueError(f"Loan not fully guaranteed. Guaranteed {total_guaranteed}, needed {amount}")

    # 4️⃣ Rule: Guarantor cannot exceed their savings
    for g in guarantors_data:
        guar = SaccoAccount.query.filter_by(member_no=g['guarantor_no']).first()
        if not guar:
            raise ValueError(f"Guarantor {g['guarantor_no']} has no savings account")
        if Decimal(g['amount_guaranteed']) > Decimal(guar.balance or 0):
            raise ValueError(f"Guarantor {g['guarantor_no']} cannot guarantee more than their savings")

    # 5️⃣ Create Loan Record
    loan_no = f"LN{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4].upper()}"
    loan = Loan(
        loan_no=loan_no,
        member_no=member_no,
        amount=Decimal(amount),
        interest_rate=Decimal(interest_rate),
        period_months=period_months,
        balance=Decimal(amount),
        status='active',
        disbursed_date=datetime.now()
    )
    db.session.add(loan)
    db.session.flush()

    # 6️⃣ Add guarantors
    for g in guarantors_data:
        db.session.add(LoanGuarantor(
            loan_id=loan.id,
            guarantor_no=g['guarantor_no'],
            amount_guaranteed=Decimal(g['amount_guaranteed'])
        ))

    # 7️⃣ Generate repayment schedule (flat interest on reducing balance)
    monthly_rate = Decimal(interest_rate) / Decimal(100 * 12)
    outstanding = Decimal(amount)
    installment_date = datetime.now().date()

    for i in range(1, period_months + 1):
        interest = (outstanding * monthly_rate).quantize(Decimal('0.01'))
        principal = (Decimal(amount) / Decimal(period_months)).quantize(Decimal('0.01'))
        due_date = installment_date + timedelta(days=30 * i)

        db.session.add(LoanSchedule(
            loan_id=loan.id,
            due_date=due_date,
            principal_due=principal,
            interest_due=interest
        ))

        outstanding -= principal

    db.session.commit()
    return loan_no
def generate_loan_schedule(loan, rate_per_annum=12.0):
    """
    Generates monthly loan repayment schedule.
    Interest is calculated on reducing balance.
    """
    principal = Decimal(loan.amount)
    months = loan.period_months
    monthly_rate = Decimal(rate_per_annum) / Decimal('12.0') / Decimal('100.0')
    installment_principal = principal / months

    balance = principal
    schedules = []

    for i in range(1, months + 1):
        interest_due = balance * monthly_rate
        total_due = installment_principal + interest_due
        due_date = loan.disbursed_date + timedelta(days=30 * i)

        schedules.append(LoanSchedule(
            loan_no=loan.loan_no,
            member_no=loan.member_no,
            due_date=due_date,
            principal_due=installment_principal.quantize(Decimal('0.01')),
            interest_due=interest_due.quantize(Decimal('0.01')),
            total_due=total_due.quantize(Decimal('0.01'))
        ))

        # Also create monthly interest tracking entry
        month_str = due_date.strftime("%Y-%m")
        interest_record = LoanInterest(
            loan_no=loan.loan_no,
            member_no=loan.member_no,
            month=month_str,
            interest_due=interest_due.quantize(Decimal('0.01'))
        )
        db.session.add(interest_record)

        # Reduce balance
        balance -= installment_principal

    db.session.add_all(schedules)
