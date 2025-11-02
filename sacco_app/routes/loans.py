from flask import Blueprint, render_template, request, jsonify
from extensions import db
from models import Loan, LoanGuarantor, Member, SaccoAccount, LoanSchedule
from forms import LoanDisbursementForm
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/disburse_loan', methods=['GET', 'POST'])
def disburse_loan():
    form = LoanDisbursementForm()
    if form.validate_on_submit():
        member_no = form.member_no.data.strip()
        amount = Decimal(form.amount.data)
        period = form.period.data
        annual_rate = Decimal('12.0')  # you can later make this configurable

        member = Member.query.filter_by(member_no=member_no).first()
        if not member:
            return jsonify({"error": "Member not found"}), 400

        # --- Member savings check ---
        savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
        if not savings_acc:
            return jsonify({"error": "Member has no savings account"}), 400

        max_loan = savings_acc.balance * 3
        if amount > max_loan:
            return jsonify({"error": f"Loan exceeds 3x member savings ({max_loan})"}), 400

        # --- Validate guarantors ---
        total_guaranteed = Decimal(0)
        guarantors_data = []
        for gform in form.guarantors.entries:
            g_no = gform.data['guarantor_no'].strip()
            g_amt = Decimal(gform.data['amount_guaranteed'])

            g_savings = SaccoAccount.query.filter_by(member_no=g_no, account_type='SAVINGS').first()
            if not g_savings:
                return jsonify({"error": f"Guarantor {g_no} has no savings account"}), 400
            if g_amt > g_savings.balance:
                return jsonify({"error": f"Guarantor {g_no} cannot guarantee more than their savings"}), 400

            total_guaranteed += g_amt
            guarantors_data.append((g_no, g_amt))

        if total_guaranteed < amount:
            return jsonify({"error": "Entire loan amount not fully guaranteed"}), 400

        # --- Generate next loan number ---
        last_loan = Loan.query.order_by(Loan.id.desc()).first()
        next_no = f"LN{(last_loan.id + 1) if last_loan else 1:04d}"

        # --- Create loan and accounts ---
        loan_account = f"{member_no}_LN{next_no[-1]}"
        int_account = f"{member_no}_INT{next_no[-1]}"

        new_loan = Loan(
            loan_no=next_no,
            member_no=member_no,
            loan_account=loan_account,
            interest_account=int_account,
            amount=amount,
            period=period,
            interest_rate=annual_rate
        )
        db.session.add(new_loan)
        db.session.flush()

        for g_no, g_amt in guarantors_data:
            db.session.add(LoanGuarantor(loan_id=new_loan.id, guarantor_no=g_no, amount_guaranteed=g_amt))

        # --- Create loan & interest accounts ---
        db.session.add_all([
            SaccoAccount(account_no=loan_account, member_no=member_no, account_type='LOAN', balance=amount),
            SaccoAccount(account_no=int_account, member_no=member_no, account_type='INTEREST', balance=0)
        ])

        # --- Generate monthly repayment schedule ---
        monthly_principal = (amount / period).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        monthly_rate = (annual_rate / Decimal(12 * 100)).quantize(Decimal('0.0001'))

        balance = amount
        start_date = datetime.utcnow()

        for i in range(1, period + 1):
            interest_due = (balance * monthly_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            principal_due = monthly_principal
            due_date = (start_date + timedelta(days=30 * i)).date()

            schedule = LoanSchedule(
                loan_id=new_loan.id,
                due_date=due_date,
                principal_due=principal_due,
                interest_due=interest_due
            )
            db.session.add(schedule)

            balance -= principal_due
            if balance < 0:
                balance = Decimal(0)

        db.session.commit()
        return jsonify({"success": True, "message": f"Loan {next_no} successfully disbursed and schedule created"}), 200

    return render_template('admin/disburse_loan.html', form=form)
