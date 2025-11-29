from flask import Blueprint, render_template, redirect, url_for, flash, request,jsonify,send_file
from flask_login import login_required,current_user
from datetime import datetime, timedelta
from sacco_app.extensions import db,csrf
from sacco_app.models import User,Member,generate_account_number,SaccoAccount,Transaction, Loan,LoanGuarantor, LoanSchedule, LoanInterest,AuditLog
from sacco_app.forms import UserForm,AddMemberForm,LoanRepaymentForm,OpenAccountForm,PaymentPostingForm,LoanDisbursementForm,GuarantorForm,MemberDepositSearchForm
from werkzeug.security import generate_password_hash
from sacco_app.utils.transactions import post_savings
from decimal import Decimal
from io import BytesIO
from flask import make_response, request
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import random, uuid
import pandas as pd
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import current_app

def role_required_admin():
    return current_user.is_authenticated and current_user.role == 'admin'


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# List Users
@admin_bp.route('/users/list', methods=['GET'])
@login_required
def list_users():
    if not role_required_admin():
        return 'forbidden', 403
    users = User.query.all()
    return render_template('admin/list_users.html', users=users)


# Create User (GET: show form, POST: create user)
@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()
        password = form.password.data.strip()
        role = form.role.data

        # extra backend validation
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('admin.create_user'))

        # create the user
        user = User(username=username, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully!", "success")
        return redirect(url_for('admin.list_users'))  # redirect anywhere you want

    # Render the form if GET or validation failed
    return render_template("admin/create_user.html", form=form)

##generate or add new member
def generate_member_no():
    # Get last member
    last_member = Member.query.order_by(Member.member_no.desc()).first()
    if not last_member or not last_member.member_no:
        return "M0001"
    # Extract numeric part and increment
    last_no = int(last_member.member_no[1:])  # Remove the 'M'
    next_no = last_no + 1
    return f"M{next_no:04d}"
# Add New Member
@admin_bp.route('/members/add', methods=['GET','POST'], endpoint='add_member')
@login_required
def add_member_view():
    if not role_required_admin():
        flash("You are not authorized!", "danger")
        return redirect(url_for('admin.dashboard'))

    form = AddMemberForm()
    if form.validate_on_submit():
        new_member = Member(
            member_no=generate_member_no(),
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            dob=form.dob.data,
            id_no=form.id_no.data,
            congregation=form.congregation.data,
            gender=form.gender.data,
            created_by=current_user.id
        )
        db.session.add(new_member)
        db.session.commit()
        flash(f"Member {new_member.member_no} added successfully!", "success")
        return redirect(url_for('admin.list_members'))

    return render_template('admin/add_member.html', form=form)
''''
# List Members
@admin_bp.route('/members/list', endpoint='list_members')
@login_required
def list_members_view():
    if not role_required_admin():
        flash("You are not authorized!", "danger")
        return redirect(url_for('admin.dashboard'))

    members = Member.query.all()
    return render_template('admin/list_members.html', members=members)
 '''
# List Members 
@admin_bp.route('/members/list')
@login_required
def list_members():
    if current_user.role != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('admin.dashboard'))

    page = request.args.get('page', 1, type=int)
    members = Member.query.with_entities(
        Member.id,
        Member.member_no,
        Member.name,
        Member.phone,
        Member.congregation
    ).paginate(page=page, per_page=10)

    # If AJAX request, return only the table fragment as HTML
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/_member_table.html', members=members)

    # Otherwise render full page (with container and pagination)
    return render_template('admin/list_members.html', members=members)
    
@admin_bp.route('/members/account/open', methods=['GET', 'POST'])
@login_required
def open_account():
    form = OpenAccountForm()
    if form.validate_on_submit():
        member_no = form.member_no.data.strip()
        account_type = form.account_type.data

        member = Member.query.filter_by(member_no=member_no).first()
        if not member:
            flash("Member not found.", "danger")
            return redirect(url_for('admin.open_account'))

        account_number = generate_account_number(member_no, account_type)
        new_account = SaccoAccount(
            member_no=member_no,
            account_number=account_number,
            account_type=account_type,
            created_by=current_user.username
        )

        db.session.add(new_account)
        db.session.commit()

        flash(f"{account_type} account opened successfully with account number {account_number}", "success")
        return redirect(url_for('admin.open_account'))

    return render_template('admin/open_account.html', form=form)
@admin_bp.route('/get_member_name', methods=['GET'])
@login_required
def get_member_name():
    member_no = request.args.get('member_no')
    member = Member.query.filter_by(member_no=member_no).first()
    if member:
        return jsonify({'name': member.name})
    else:
        return jsonify({'name': ''})
# Route to DISPLAY the form

# Route to display the deposit form
@admin_bp.route('/transactions/post', methods=['GET'])
@login_required
def post_transaction():
    from sacco_app.forms import PaymentPostingForm
    form = PaymentPostingForm()
    return render_template('admin/post_transaction.html', form=form)


# Route to handle deposit posting (savings)
@admin_bp.route('/transactions/post/savings', methods=['POST'])
@login_required
def post_savings_transaction():
    try:
        member_no = request.form.get('member_no')
        amount = Decimal(request.form.get('amount', '0'))
        narration = request.form.get('narration')
        bank_txn_date = request.form.get('bank_txn_date')

        if not (member_no and amount > 0):
            flash("Invalid member or amount.", "danger")
            return redirect(url_for('admin.post_transaction'))

        member = Member.query.filter_by(member_no=member_no).first()
        if not member:
            flash(f"Member {member_no} not found.", "danger")
            return redirect(url_for('admin.post_transaction'))

        txn_date = datetime.strptime(bank_txn_date, '%Y-%m-%d') if bank_txn_date else datetime.now()

        # 1️⃣ Member’s savings account
        member_savings_acc = SaccoAccount.query.filter_by(
            member_no=member_no, account_type='SAVINGS'
        ).first()
        if not member_savings_acc:
            flash("Member does not have a savings account.", "danger")
            return redirect(url_for('admin.post_transaction'))

        # 2️⃣ Cash control account (M000GL_CASH)
        cash_acc = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
        account_no_cash_acc=cash_acc.account_number,

        # 3️⃣ Savings control account (M000GL_SAVINGS)
        savings_ctrl_acc = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()

        if not (cash_acc and savings_ctrl_acc):
            flash("Cash or savings control account missing.", "danger")
            return redirect(url_for('admin.post_transaction'))

        txn_no = f"TXN{uuid.uuid4().hex[:10].upper()}"  # e.g. TXN4A6F9B7C2E

        # ---------- TRANSACTION LOGIC ----------
        # Debit: Cash (money received)
        # Credit: Member Savings
        # Credit: Savings Control (liability increase)
        transactions = []

        # Debit Cash Account
        cash_acc.balance += amount
        cash_acc_running_balance=cash_acc.balance
        txn1 = Transaction(
            txn_no=txn_no,
            member_no=member_no,
            account_no=account_no_cash_acc,
            gl_account='CASH_ACC',
            tran_type='ASSET',
            debit_amount=amount,
            reference=txn_no,
            credit_amount=Decimal('0'),
            narration=f"Deposit by {member_no} - {narration}",
            bank_txn_date=txn_date,
            posted_by=current_user.username,
            running_balance=cash_acc_running_balance
        )
        transactions.append(txn1)

        # Credit Member Savings Account
        member_savings_acc.balance += amount
        txn_no2 = f"TXN{uuid.uuid4().hex[:10].upper()}"
        txn2 = Transaction(
            txn_no=txn_no2,
            member_no=member_no,
            account_no=member_savings_acc.account_number,
            gl_account='SAVINGS',
            tran_type='SAVINGS',
            debit_amount=Decimal('0'),
            reference=txn_no,
            credit_amount=amount,
            narration=f"Deposit to Savings ({member_no})",
            bank_txn_date=txn_date,
            posted_by=current_user.username,
            running_balance=member_savings_acc.balance,
            created_at=datetime.now()
        )
        transactions.append(txn2)
        txn_no3 = f"TXN{uuid.uuid4().hex[:10].upper()}"
        # Credit Savings Control Account
        savings_ctrl_acc.balance += amount
        txn3 = Transaction(
            txn_no=txn_no3,
            member_no='M000GL',
            account_no=savings_ctrl_acc.account_number,
            gl_account='SAVINGS_CONTROL',
            tran_type='LIABILITY',
            debit_amount=Decimal('0'),
            reference=txn_no,
            credit_amount=amount,
            narration=f"Savings control posting for {member_no}",
            bank_txn_date=txn_date,
            posted_by=current_user.username,
            running_balance=savings_ctrl_acc.balance,
            created_at=datetime.now()
        )
        transactions.append(txn3)

        # ---------- COMMIT ----------
        for t in transactions:
            db.session.add(t)
        db.session.commit()

        flash(f"Deposit of {amount:.2f} posted successfully for member {member_no}.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error posting deposit: {str(e)}", "danger")

    return redirect(url_for('admin.list_member_deposits'))
    
 #list member deposits

@admin_bp.route('/member-deposits', methods=['GET', 'POST'])
@login_required
def list_member_deposits():
    form = MemberDepositSearchForm()
    deposits = []
    member = None

    if request.method == 'POST' and form.validate_on_submit():
        member_no = form.member_no.data.strip()
        start_date = form.start_date.data
        end_date = form.end_date.data

        # Fetch member
        member = Member.query.filter_by(member_no=member_no).first()

        if not member:
            flash(f"Member {member_no} not found.", "danger")
            # ✅ Re-render the same page (not redirect) to avoid loop
            return render_template('admin/list_member_deposits.html',form=form,deposits=[],member= None)

        # ✅ Query only member savings transactions
        deposits = Transaction.query.filter(
            Transaction.member_no == member_no,
            Transaction.bank_txn_date.between(start_date, end_date),
            Transaction.tran_type == 'SAVINGS'
        ).order_by(Transaction.id.asc()).all()

        return render_template(
            'admin/list_member_deposits.html',
            form=form,
            deposits=deposits,
            member=member
        )

    # Default GET request — show empty form
    return render_template(
        'admin/list_member_deposits.html',
        form=form,
        deposits=[],
        member=None
    )
    
    # display name on form
from flask import jsonify

@admin_bp.route('/api/member_info/<member_no>')
@login_required
def api_member_info(member_no):
    """Return basic member info and savings balance for AJAX."""
    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404

    savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
    savings_balance = float(savings_acc.balance) if savings_acc else 0.00

    return jsonify({
        'member_no': member.member_no,
        'member_name': member.name,
        'savings_balance': savings_balance
    })



    
    #LOAN DISBURSMENT
@admin_bp.route('/loans/disburse', methods=['GET', 'POST'])
@login_required
def disburse_loan():
    """Loan disbursement route – creates loan, GL entries, guarantors, and schedules."""
    from decimal import Decimal
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    import uuid, re

    from sacco_app import db
    from sacco_app.models import (
        Member, Loan, LoanGuarantor, LoanSchedule,
        SaccoAccount, Transaction
    )

    form = LoanDisbursementForm()

    # --- helper to parse guarantors from dynamic form fields
    def parse_guarantors(formdata):
        idxs = set()
        pattern = re.compile(r"^guarantors\[(\d+)\]\[(member_no|amount_guaranteed)\]$")
        for k in formdata.keys():
            m = pattern.match(k)
            if m:
                idxs.add(int(m.group(1)))
        parsed = []
        for i in sorted(list(idxs)):
            gno = (formdata.get(f"guarantors[{i}][member_no]") or "").strip()
            gamt = formdata.get(f"guarantors[{i}][amount_guaranteed]") or "0"
            if gno:
                try:
                    parsed.append({"member_no": gno, "amount_guaranteed": Decimal(str(gamt))})
                except Exception:
                    parsed.append({"member_no": gno, "amount_guaranteed": Decimal("0")})
        return parsed

    # --- show validation errors clearly
    if request.method == 'POST' and not form.validate_on_submit():
        def flatten_errors(errors):
            msg_list = []
            for field, msgs in errors.items():
                if isinstance(msgs, (list, tuple)):
                    for m in msgs:
                        if isinstance(m, dict):
                            for subfield, submsg in m.items():
                                msg_list.append(f"{field}.{subfield}: {', '.join(submsg) if isinstance(submsg, list) else submsg}")
                        else:
                            msg_list.append(f"{field}: {m}")
                else:
                    msg_list.append(f"{field}: {msgs}")
            return "; ".join(msg_list)

        errs = flatten_errors(form.errors)
        flash(f"Form did not validate: {errs or 'Check required fields'}", "warning")
        return render_template('admin/disburse_loan.html', form=form)

    # --- MAIN logic
    if form.validate_on_submit():
        try:
            # --- Input values
            member_no = form.member_no.data.strip()
            loan_amount = Decimal(str(form.loan_amount.data)).quantize(Decimal('0.01'))
            loan_period = int(form.loan_period.data)
            loan_type = (getattr(form, 'loan_type', None).data or 'normal').lower().strip()
            guarantors = parse_guarantors(request.form)

            # --- Loan constants
            PROCESSING_FEE_RATE = Decimal('0.005')   # 0.5%
            ANNUAL_RATE = Decimal('15.0')            # % per year
            monthly_rate = (ANNUAL_RATE / Decimal('100')) / Decimal('12')

            processing_fee = (loan_amount * PROCESSING_FEE_RATE).quantize(Decimal('0.01'))
            net_disbursed = (loan_amount - processing_fee).quantize(Decimal('0.01'))

            # --- Member check
            member = Member.query.filter_by(member_no=member_no).first()
            if not member:
                flash(f"Member {member_no} not found.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
            if not savings_acc or savings_acc.balance <= 0:
                flash("Member has no savings or balance is zero.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            if loan_amount > (savings_acc.balance * 3):
                flash("Loan amount exceeds 3× member savings.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # --- Active/top-up logic
            active_loan = Loan.query.filter(
                Loan.member_no == member_no,
                Loan.status.in_(["Active", "Disbursed"]),
                Loan.balance > 0
            ).first()

            if loan_type != 'topup' and active_loan:
                flash("Member already has an active loan. Only a top-up is allowed.", "danger")
                return render_template('admin/disburse_loan.html', form=form)
            if loan_type == 'topup' and not active_loan:
                flash("No active loan to top-up.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # --- Required GLs
            gl_cash = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
            gl_loan_control = SaccoAccount.query.filter_by(account_number='M000GL_LOAN').first()
            gl_fee_income = SaccoAccount.query.filter_by(account_number='M000GL_REG_FEE').first()
            if not all([gl_cash, gl_loan_control, gl_fee_income]):
                flash("Missing GL accounts (Cash / Loan Control / Fee Income).", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # --- Ensure member loan & interest accounts exist
            loan_acct_no = f"{member_no}_LOAN"
            int_acct_no = f"{member_no}_INTEREST"

            loan_acct = SaccoAccount.query.filter_by(account_number=loan_acct_no).first()
            if not loan_acct:
                loan_acct = SaccoAccount(member_no=member_no, account_number=loan_acct_no,
                                         account_type='LOAN', created_by=current_user.username,
                                         balance=Decimal('0.00'))
                db.session.add(loan_acct)

            int_acct = SaccoAccount.query.filter_by(account_number=int_acct_no).first()
            if not int_acct:
                int_acct = SaccoAccount(member_no=member_no, account_number=int_acct_no,
                                        account_type='INTEREST', created_by=current_user.username,
                                        balance=Decimal('0.00'))
                db.session.add(int_acct)
            db.session.flush()

            # --- Validate guarantors
            total_guaranteed = Decimal('0.00')
            for g in guarantors:
                g_member_no = g["member_no"]
                g_amount = g["amount_guaranteed"]
                g_sav = SaccoAccount.query.filter_by(member_no=g_member_no, account_type='SAVINGS').first()
                if not g_sav:
                    flash(f"Guarantor {g_member_no} has no savings account.", "danger")
                    return render_template('admin/disburse_loan.html', form=form)
                if g_amount > g_sav.balance:
                    flash(f"Guarantor {g_member_no} cannot guarantee more than their savings.", "danger")
                    return render_template('admin/disburse_loan.html', form=form)
                total_guaranteed += g_amount
            if guarantors and total_guaranteed < loan_amount:
                flash("Total guaranteed amount is less than loan amount.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # --- Loan number
            last_loan = Loan.query.order_by(Loan.id.desc()).first()
            loan_no = f"LN{(last_loan.id + 1) if last_loan else 1:04d}"

            # --- Create Loan record
            new_loan = Loan(
                loan_no=loan_no,
                member_no=member_no,
                loan_account=loan_acct_no,
                interest_account=int_acct_no,
                loan_amount=loan_amount,
                loan_period=loan_period,
                balance=loan_amount,
                interest_rate=ANNUAL_RATE,
                status='Active',
                disbursed_by=current_user.id,
                created_at=datetime.now(),
                disbursed_date=datetime.now().date(),
                loan_type=loan_type
            )
            db.session.add(new_loan)
            db.session.flush()

            # --- Save guarantors
            for g in guarantors:
                db.session.add(LoanGuarantor(
                    loan_no=loan_no,
                    guarantor_no=g["member_no"],
                    member_no=member_no,
                    amount_guaranteed=g["amount_guaranteed"]
                ))

            # --- GL Postings
            txn_ref = f"TXN{uuid.uuid4().hex[:10].upper()}"
            transactions = []

            # 1️⃣ Dr Member Loan
            loan_acct.balance += loan_amount
            transactions.append(Transaction(
                txn_no=txn_ref, member_no=member_no, account_no=loan_acct.account_number,
                gl_account='MEMBER_LOAN', tran_type='ASSET',
                debit_amount=loan_amount, credit_amount=Decimal('0.00'),
                reference=txn_ref, narration=f"Loan disbursement - {loan_no}",
                bank_txn_date=datetime.now(), posted_by=current_user.username,
                running_balance=loan_acct.balance
            ))

            # 2️⃣ Dr GL Loan Control
            gl_loan_control.balance += loan_amount
            transactions.append(Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}", member_no='M000GL',
                account_no=gl_loan_control.account_number, gl_account='LOAN_CONTROL',
                tran_type='ASSET', debit_amount=loan_amount, credit_amount=Decimal('0.00'),
                reference=txn_ref, narration=f"Loan control debit for {loan_no}",
                bank_txn_date=datetime.now(), posted_by=current_user.username,
                running_balance=gl_loan_control.balance
            ))

            # 3️⃣ Cr Fee Income
            gl_fee_income.balance += processing_fee
            transactions.append(Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}", member_no='M000GL',
                account_no=gl_fee_income.account_number, gl_account='FEE_INCOME',
                tran_type='INCOME', debit_amount=Decimal('0.00'), credit_amount=processing_fee,
                reference=txn_ref, narration=f"Loan processing fee ({loan_no})",
                bank_txn_date=datetime.now(), posted_by=current_user.username,
                running_balance=gl_fee_income.balance
            ))

            # 4️⃣ Cr Cash
            gl_cash.balance -= net_disbursed
            transactions.append(Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}", member_no='M000GL',
                account_no=gl_cash.account_number, gl_account='CASH',
                tran_type='ASSET', debit_amount=Decimal('0.00'), credit_amount=net_disbursed,
                reference=txn_ref, narration=f"Loan disbursed to {member_no} ({loan_no})",
                bank_txn_date=datetime.now(), posted_by=current_user.username,
                running_balance=gl_cash.balance
            ))

            db.session.add_all(transactions)

# --- Generate repayment schedule (include running principal balance)
            if monthly_rate > 0:
                emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** loan_period) / ((1 + monthly_rate) ** loan_period - 1)
            else:
                emi = loan_amount / loan_period
            emi = emi.quantize(Decimal('0.01'))

            principal_balance = loan_amount
            first_due_date = datetime.now().date() + relativedelta(months=1)

            for i in range(1, loan_period + 1):
                interest_due = (principal_balance * monthly_rate).quantize(Decimal('0.01'))
                principal_due = (emi - interest_due).quantize(Decimal('0.01'))

                # Last installment — clear rounding residual
                if i == loan_period:
                    principal_due = principal_balance.quantize(Decimal('0.01'))

                # Add fee to first installment interest
                extra_fee = processing_fee if i == 1 else Decimal('0.00')

                # Update balance AFTER this payment
                new_balance = (principal_balance - principal_due).quantize(Decimal('0.01'))

                due_date = first_due_date + relativedelta(months=i - 1)

                schedule = LoanSchedule(
                    loan_no=new_loan.loan_no,
                    member_no=member_no,
                    installment_no=i,
                    due_date=due_date,
                    principal_due=principal_due,
                    interest_due=(interest_due + extra_fee).quantize(Decimal('0.01')),
                    principal_balance=new_balance,     # ✅ now stored
                    principal_paid=Decimal('0.00'),
                    interest_paid=Decimal('0.00'),
                    status='DUE'
                )
                db.session.add(schedule)

                # move to next balance
                principal_balance = new_balance

            # ✅ single commit
            db.session.commit()
            flash(f"Loan {loan_no} disbursed successfully! Schedules created, and processing fee added to 1st installment.", "success")
            return redirect(url_for('admin.list_loans'))

        except Exception as e:
            db.session.rollback()
            import traceback; traceback.print_exc()
            flash(f"Disbursement failed: {str(e)}", "danger")
            return render_template('admin/disburse_loan.html', form=form)

    # --- GET request
    return render_template('admin/disburse_loan.html', form=form)

@admin_bp.route('/loans/list', methods=['GET'])
@login_required
def list_loans():
    loans = Loan.query.all()
    return render_template('admin/list_loans.html', loans=loans)


@admin_bp.route("/loans/preview_schedule", methods=["POST"])
@login_required
def preview_loan_schedule():
    """Preview a reducing-balance loan repayment schedule before disbursement"""
    from decimal import Decimal
    from datetime import datetime, timedelta

    member_no = request.form.get("member_no")
    loan_amount = Decimal(request.form.get("loan_amount", "0"))
    loan_period = int(request.form.get("loan_period", "12"))
    annual_rate = Decimal(request.form.get("interest_rate", "15")) / 100

    monthly_rate = annual_rate / 12
    principal_balance = loan_amount
    n = loan_period
    r = monthly_rate

    # Calculate EMI
    if r == 0:
        emi = (loan_amount / n).quantize(Decimal('0.01'))
    else:
        emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        emi = emi.quantize(Decimal('0.01'))

    schedule = []
    for i in range(1, n + 1):
        interest_due = (principal_balance * r).quantize(Decimal('0.0125'))
        principal_due = (emi - interest_due).quantize(Decimal('0.0125'))

        if i == n:
            principal_due = principal_balance
            emi = principal_due + interest_due

        schedule.append({
            "installment_no": i,
            "due_date": (datetime.now() + timedelta(days=30 * i)).strftime("%Y-%m-%d"),
            "principal_due": principal_due,
            "interest_due": interest_due,
            "total_due": (principal_due + interest_due),
            "balance_after": (principal_balance - principal_due).quantize(Decimal('0.0125'))
        })
        principal_balance -= principal_due

    total_interest = sum(item["interest_due"] for item in schedule)
    total_payment = sum(item["total_due"] for item in schedule)

    return render_template(
        "admin/loan_schedule_preview.html",
        schedule=schedule,
        loan_amount=loan_amount,
        total_interest=total_interest,
        total_payment=total_payment,
        emi=emi,
        loan_period=loan_period,
        annual_rate=annual_rate * 100,
        member_no=member_no
    )
@admin_bp.route("/loans/schedule_pdf", methods=["POST"])
@login_required
@csrf.exempt
def download_loan_schedule_pdf():
    member_no = request.form.get("member_no")
    loan_amount = Decimal(request.form.get("loan_amount", "0"))
    loan_period = int(request.form.get("loan_period", "12"))
    annual_rate = Decimal(request.form.get("interest_rate", "12")) / 100

    monthly_rate = annual_rate / 12
    principal_balance = loan_amount
    n = loan_period
    r = monthly_rate

    # --- Calculate fixed EMI for reducing balance loan ---
    if r == 0:
        emi = (loan_amount / n).quantize(Decimal('0.01'))
    else:
        emi = (loan_amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        emi = emi.quantize(Decimal('0.01'))

    schedule = []
    total_principal = Decimal('0.00')
    total_interest = Decimal('0.00')
    total_payment = Decimal('0.00')

    for i in range(1, n + 1):
        interest_due = (principal_balance * r).quantize(Decimal('0.01'))
        principal_due = (emi - interest_due).quantize(Decimal('0.01'))

        if i == n:
            # Adjust last installment for rounding
            principal_due = principal_balance
            emi = principal_due + interest_due

        total_principal += principal_due
        total_interest += interest_due
        total_payment += (principal_due + interest_due)

        schedule.append([
            str(i),
            (datetime.now() + timedelta(days=30 * i)).strftime("%Y-%m-%d"),
            f"{principal_due:.2f}",
            f"{interest_due:.2f}",
            f"{(principal_due + interest_due):.2f}",
            f"{(principal_balance - principal_due):.2f}",
        ])
        principal_balance -= principal_due

    # Add totals row
    schedule.append([
        "",
        "TOTALS",
        f"{total_principal:.2f}",
        f"{total_interest:.2f}",
        f"{total_payment:.2f}",
        ""
    ])

    # --- Generate PDF ---
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("<b>Loan Repayment Schedule</b>", styles["Title"])
    info = Paragraph(
        f"Member No: {member_no}<br/>"
        f"Loan Amount: Ksh {loan_amount:,}<br/>"
        f"Loan Period: {loan_period} months<br/>"
        f"Interest Rate: {annual_rate * 100}%<br/>"
        f"Monthly Installment (EMI): Ksh {emi:,}",
        styles["Normal"]
    )

    elements.append(title)
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(info)
    elements.append(Spacer(1, 0.7 * cm))

    table_data = [["#", "Due Date", "Principal (Ksh)", "Interest (Ksh)", "Total Payment (Ksh)", "Balance After (Ksh)"]] + schedule

    table = Table(table_data, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, -1), (-1, -1), colors.whitesmoke),  # Total row shading
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))
    elements.append(table)

    doc.build(elements)
    pdf_value = buffer.getvalue()
    buffer.close()

    response = make_response(pdf_value)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=LoanSchedule_{member_no}.pdf"
    return response
    
#UPLOAD TRANSACTIONS
# in sacco_app/routes/admin.py
@admin_bp.route('/upload_member_savings', methods=['GET', 'POST'])
@login_required
def upload_member_savings():
    from sacco_app.forms import UploadMemberSavingsForm
    import uuid

    form = UploadMemberSavingsForm()

    if form.validate_on_submit():
        file = form.file.data
        if not file:
            flash("Please select an Excel (.xlsx) file to upload.", "danger")
            return redirect(url_for('admin.upload_member_savings'))

        # ✅ Read Excel file
        df = pd.read_excel(file)
        required_cols = {'bank_txn_date', 'credit_amount', 'narration', 'member_no', 'account_no'}
        if not required_cols.issubset(df.columns):
            flash(f"Missing required columns. Expected: {', '.join(required_cols)}", "danger")
            return redirect(url_for('admin.upload_member_savings'))


        success_count = 0
        failed_rows = []

        for i, row in df.iterrows():
            member_no = str(row.get('member_no')).strip()
            narration = str(row.get('narration', '')).strip()
            bank_txn_date = row.get('bank_txn_date')
            credit_amount = Decimal(row.get('credit_amount', 0) or 0)
            account_no = str(row.get('account_no', '')).strip()

            try:
                member = Member.query.filter_by(member_no=member_no).first()
                if not member:
                    failed_rows.append({
                        'row': i+1,
                        'member_no': member_no,
                        'error': 'Member not found'
                    })
                    continue

                txn_date = pd.to_datetime(bank_txn_date).to_pydatetime() if pd.notnull(bank_txn_date) else datetime.now()

                # Get accounts
                member_savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
                cash_acc = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
                savings_ctrl_acc = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()

                if not (member_savings_acc and cash_acc and savings_ctrl_acc):
                    failed_rows.append({
                        'row': i+1,
                        'member_no': member_no,
                        'error': 'Missing required accounts'
                    })
                    continue

                # Generate transactions
                txn_no = f"TXN{uuid.uuid4().hex[:10].upper()}"

                # Debit Cash
                cash_acc.balance += credit_amount
                db.session.add(Transaction(
                    txn_no=txn_no,
                    member_no=member_no,
                    account_no=cash_acc.account_number,
                    gl_account='CASH_ACC',
                    tran_type='ASSET',
                    debit_amount=credit_amount,
                    credit_amount=Decimal('0'),
                    reference=txn_no,
                    narration=f"Deposit by {member_no} - {narration}",
                    bank_txn_date=txn_date,
                    posted_by=current_user.username,
                    running_balance=cash_acc.balance
                ))

                # Credit Member Savings
                member_savings_acc.balance += credit_amount
                db.session.add(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no=member_no,
                    account_no=member_savings_acc.account_number,
                    gl_account='SAVINGS',
                    tran_type='SAVINGS',
                    debit_amount=Decimal('0'),
                    credit_amount=credit_amount,
                    reference=txn_no,
                    narration=narration,
                    bank_txn_date=txn_date,
                    posted_by=current_user.username,
                    running_balance=member_savings_acc.balance,
                    created_at=datetime.now()
                ))

                # Credit Savings Control
                savings_ctrl_acc.balance += credit_amount
                db.session.add(Transaction(
                    txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                    member_no='M000GL',
                    account_no=savings_ctrl_acc.account_number,
                    gl_account='SAVINGS_CONTROL',
                    tran_type='LIABILITY',
                    debit_amount=Decimal('0'),
                    credit_amount=credit_amount,
                    reference=txn_no,
                    narration=f"{narration} - {member_no}",
                    bank_txn_date=txn_date,
                    posted_by=current_user.username,
                    running_balance=savings_ctrl_acc.balance,
                    created_at=datetime.now()
                ))

                db.session.commit()
                success_count += 1

            except Exception as e:
                db.session.rollback()
                failed_rows.append({
                    'row': i+1,
                    'member_no': member_no,
                    'error': str(e)
                })

        flash(f"Upload completed: {success_count} succeeded, {len(failed_rows)} failed.", 'info')

        # Pass failed rows to template
        return render_template('admin/upload_results.html', failed_rows=failed_rows, success_count=success_count)

    return render_template('admin/upload_member_savings.html', form=form)

#loan_ repayment master
@admin_bp.route('/api/member_loan_info/<member_no>')
@login_required
def api_member_loan_info(member_no):
    """Return detailed member + loan info for AJAX repayment/prepayment forms."""
    from sacco_app.models import Member, Loan, LoanSchedule, SaccoAccount
    from datetime import date

    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404

    loan = Loan.query.filter_by(member_no=member_no, status='Active').first()
    savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()

    savings_balance = float(savings_acc.balance) if savings_acc else 0.0
    loan_balance = float(loan.balance) if loan else 0.0
    loan_no = loan.loan_no if loan else None

    # 🧮 Compute due amount up to today
    total_due = 0.0
    if loan:
        due_schedules = LoanSchedule.query.filter(
            LoanSchedule.loan_no == loan.loan_no,
            LoanSchedule.due_date <= date.today()
        ).all()

        total_due = sum(
            float((s.principal_due - s.principal_paid) + (s.interest_due - s.interest_paid))
            for s in due_schedules
        )

    return jsonify({
        'member_no': member.member_no,
        'member_name': member.name,
        'loan_no': loan_no,
        'loan_balance': loan_balance,
        'due_amount': round(total_due, 2),
        'savings_balance': savings_balance
    })
    #loan repayment

#loan_ repayment master
@admin_bp.route('/loan-repayment', methods=['GET', 'POST'])
@login_required
def loan_repayment():
    form = LoanRepaymentForm()
    if form.validate_on_submit():
        member_no = form.member_no.data.strip()
        amount = Decimal(form.amount.data)
        narration = form.narration.data
        bank_txn_date = form.bank_txn_date.data.strftime('%Y-%m-%d')

        # Import helper for posting repayment
        from sacco_app.utils.transactions import process_loan_repayment
        try:
            process_loan_repayment(member_no, amount, narration, bank_txn_date, current_user.username)
            flash(f"Loan repayment of {amount} for {member_no} posted successfully.", "success")
            return redirect(url_for('admin.loan_repayment'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error posting repayment: {str(e)}", "danger")

    return render_template('admin/loan_repayment.html', form=form)
#LOAN PREPAYMENT
@admin_bp.route('/loan-prepayment', methods=['GET', 'POST'])
@login_required
def loan_prepayment():
    """Loan prepayment form — posts directly to principal, no interest."""
    from sacco_app.utils.transactions import process_loan_prepayment
    from sacco_app import db

    form = LoanRepaymentForm()

    if form.validate_on_submit():
        try:
            msg = process_loan_prepayment(
                member_no=form.member_no.data.strip(),
                amount=form.amount.data,
                narration=form.narration.data,
                bank_txn_date=form.bank_txn_date.data.strftime("%Y-%m-%d"),
                posted_by=current_user.username
            )
            db.session.commit()
            flash(msg, "success")
            return redirect(url_for('admin.loan_prepayment'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error posting prepayment: {str(e)}", "danger")

    return render_template('admin/loan_prepayment.html', form=form)
#dashboard data

# ===========================================
# UPLOAD LOAN REPAYMENTS FROM EXCEL
# ===========================================
@admin_bp.route('/upload_loan_repayments', methods=['GET', 'POST'])
@login_required
def upload_loan_repayments():
    from sacco_app.forms import UploadMemberSavingsForm  # reuse same form
    import uuid
    from decimal import Decimal
    from datetime import datetime

    form = UploadMemberSavingsForm()  # same form: single file upload

    if form.validate_on_submit():
        file = form.file.data
        if not file:
            flash("Please select an Excel (.xlsx) file to upload.", "danger")
            return redirect(url_for('admin.upload_loan_repayments'))

        df = pd.read_excel(file)
        required_cols = {'bank_txn_date', 'credit_amount', 'narration', 'member_no'}
        if not required_cols.issubset(df.columns):
            flash(f"Missing required columns. Expected: {', '.join(required_cols)}", "danger")
            return redirect(url_for('admin.upload_loan_repayments'))

        success_count = 0
        failed_rows = []

        for i, row in df.iterrows():
            member_no = str(row.get('member_no')).strip()
            narration = str(row.get('narration', '')).strip()
            bank_txn_date = row.get('bank_txn_date')
            credit_amount = Decimal(row.get('credit_amount', 0) or 0)

            try:
                member = Member.query.filter_by(member_no=member_no).first()
                if not member:
                    failed_rows.append({'row': i+1, 'member_no': member_no, 'error': 'Member not found'})
                    continue

                txn_date = pd.to_datetime(bank_txn_date).to_pydatetime() if pd.notnull(bank_txn_date) else datetime.now()

                # Get accounts
                member_savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
                gl_cash = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
                gl_loan_control = SaccoAccount.query.filter_by(account_number='M000GL_LOAN').first()
                gl_interest_income = SaccoAccount.query.filter_by(account_number='M000GL_LN_INT').first()
                gl_savings_ctrl = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()

                loan = Loan.query.filter_by(member_no=member_no, status='Active').first()

                remaining = credit_amount
                txn_ref = f"TXN{uuid.uuid4().hex[:10].upper()}"

                # 1️⃣ Debit Cash (money in)
                gl_cash.balance += credit_amount
                db.session.add(Transaction(
                    txn_no=txn_ref,
                    member_no=member_no,
                    account_no=gl_cash.account_number,
                    gl_account='CASH',
                    tran_type='ASSET',
                    debit_amount=credit_amount,
                    credit_amount=Decimal('0'),
                    reference=txn_ref,
                    narration=f"Loan repayment from {member_no} - {narration}",
                    bank_txn_date=txn_date,
                    posted_by=current_user.username,
                    running_balance=gl_cash.balance
                ))

                # If member has an active loan, apply interest and principal
                if loan:
                    schedules = LoanSchedule.query.filter(
                        LoanSchedule.loan_no == loan.loan_no,
                        LoanSchedule.status.in_(['DUE', 'PARTIAL'])
                    ).order_by(LoanSchedule.installment_no).all()

                    for sched in schedules:
                        if remaining <= 0:
                            break

                        # --- Pay interest first
                        interest_due = sched.interest_due - sched.interest_paid
                        if remaining > 0 and interest_due > 0:
                            pay_interest = min(remaining, interest_due)
                            sched.interest_paid += pay_interest
                            remaining -= pay_interest

                            # GL: Interest income
                            gl_interest_income.balance += pay_interest
                            db.session.add(Transaction(
                                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                                member_no='M000GL',
                                account_no=gl_interest_income.account_number,
                                gl_account='INTEREST_INCOME',
                                tran_type='INCOME',
                                debit_amount=Decimal('0'),
                                credit_amount=pay_interest,
                                reference=txn_ref,
                                narration=f"Interest income - {member_no}",
                                bank_txn_date=txn_date,
                                posted_by=current_user.username,
                                running_balance=gl_interest_income.balance
                            ))

                        # --- Then principal
                        principal_due = sched.principal_due - sched.principal_paid
                        if remaining > 0 and principal_due > 0:
                            pay_principal = min(remaining, principal_due)
                            sched.principal_paid += pay_principal
                            loan.balance -= pay_principal
                            remaining -= pay_principal

                            # GL: Loan control decrease
                            gl_loan_control.balance -= pay_principal
                            db.session.add(Transaction(
                                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                                member_no='M000GL',
                                account_no=gl_loan_control.account_number,
                                gl_account='LOAN_CONTROL',
                                tran_type='ASSET',
                                debit_amount=Decimal('0'),
                                credit_amount=pay_principal,
                                reference=txn_ref,
                                narration=f"Principal repayment - {member_no}",
                                bank_txn_date=txn_date,
                                posted_by=current_user.username,
                                running_balance=gl_loan_control.balance
                            ))

                        # Update schedule status
                        if sched.principal_paid >= sched.principal_due and sched.interest_paid >= sched.interest_due:
                            sched.status = 'PAID'
                        else:
                            sched.status = 'PARTIAL'

                    # If loan fully paid
                    if loan.balance <= 0:
                        loan.balance = Decimal('0.00')
                        loan.status = 'Cleared'

                # 2️⃣ Remaining → savings
                if remaining > 0:
                    member_savings_acc.balance += remaining
                    gl_savings_ctrl.balance += remaining

                    db.session.add(Transaction(
                        txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                        member_no=member_no,
                        account_no=member_savings_acc.account_number,
                        gl_account='SAVINGS',
                        tran_type='SAVINGS',
                        debit_amount=Decimal('0'),
                        credit_amount=remaining,
                        reference=txn_ref,
                        narration=f"Excess to savings - {narration}",
                        bank_txn_date=txn_date,
                        posted_by=current_user.username,
                        running_balance=member_savings_acc.balance
                    ))

                db.session.commit()
                success_count += 1

            except Exception as e:
                db.session.rollback()
                failed_rows.append({'row': i+1, 'member_no': member_no, 'error': str(e)})

        flash(f"Upload completed: {success_count} succeeded, {len(failed_rows)} failed.", 'info')
        return render_template('admin/upload_results.html', failed_rows=failed_rows, success_count=success_count)

    return render_template('admin/upload_loan_repayments.html', form=form)
    
    
    #dashboardrds
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard summary."""
    from sacco_app.models import Member, SaccoAccount, Loan, LoanSchedule
    from sqlalchemy import func, or_, text
    from datetime import date, timedelta

    # Helper to format money
    def fmt(n):
        return f"{float(n or 0):,.2f}"

    # ----------------------------
    # 1. TOTAL MEMBERS
    # ----------------------------
    total_members = Member.query.count()

    # ----------------------------
    # 2. TOTAL SAVINGS
    # ----------------------------
    total_savings = db.session.query(
        func.coalesce(func.sum(SaccoAccount.balance), 0)
    ).filter(
        SaccoAccount.account_type == 'SAVINGS',
        SaccoAccount.account_number != 'M000GL_SAVINGS'
    ).scalar()

    # ----------------------------
    # 3. TOTAL SHARE CAPITAL
    # ----------------------------
    total_share_capital = db.session.query(
        func.coalesce(func.sum(SaccoAccount.balance), 0)
    ).filter(SaccoAccount.account_type == 'SHARE_CAPITAL').scalar()

    # ----------------------------
    # 4. TOTAL LOANS OUTSTANDING
    # ----------------------------
    total_loans = db.session.query(
        func.coalesce(func.sum(Loan.balance), 0)
    ).filter(
        Loan.status.in_(['Active', 'Disbursed'])
    ).scalar()

    # ----------------------------
    # 5. MEMBERS WITH ZERO SAVINGS BALANCE
    # ----------------------------
    members_zero_balance = db.session.execute(
        text("""
            SELECT COUNT(*) FROM (
                SELECT m.member_no, COALESCE(SUM(s.balance), 0) AS bal
                FROM members m
                LEFT JOIN sacco_accounts s 
                    ON m.member_no = s.member_no 
                    AND s.account_type = 'SAVINGS'
                GROUP BY m.member_no
                HAVING COALESCE(SUM(s.balance), 0) = 0
            ) x;
        """)
    ).scalar()

    # ----------------------------
    # 6. INSTALLMENT DUE THIS MONTH
    # ----------------------------
    installment_due = db.session.query(
        func.coalesce(func.sum(
            (LoanSchedule.principal_due - LoanSchedule.principal_paid) +
            (LoanSchedule.interest_due - LoanSchedule.interest_paid)
        ), 0)
    ).filter(
        func.date_trunc('month', LoanSchedule.due_date) ==
        func.date_trunc('month', date.today()),
        LoanSchedule.status != 'PAID'
    ).scalar()

    # ----------------------------
    # 7. PRINCIPAL ARREARS (OVERDUE)
    # ----------------------------
    principal_arrears = db.session.query(
        func.coalesce(func.sum(
            LoanSchedule.principal_due - LoanSchedule.principal_paid
        ), 0)
    ).filter(
        LoanSchedule.due_date < date.today(),
        LoanSchedule.status != 'PAID'
    ).scalar()

    # ----------------------------
    # 8. INTEREST ARREARS (OVERDUE)
    # ----------------------------
    interest_arrears = db.session.query(
        func.coalesce(func.sum(
            LoanSchedule.interest_due - LoanSchedule.interest_paid
        ), 0)
    ).filter(
        LoanSchedule.due_date < date.today(),
        LoanSchedule.status != 'PAID'
    ).scalar()

    # ----------------------------
    # 9. LOANS NOT PAID IN LAST 2 MONTHS (Using loan_no)
    # ----------------------------
    two_months_ago = date.today() - timedelta(days=60)

    recent_paid_loans = db.session.query(LoanSchedule.loan_no).filter(
        LoanSchedule.due_date >= two_months_ago,
        or_(LoanSchedule.principal_paid > 0, LoanSchedule.interest_paid > 0)
    ).distinct()

    loans_not_paid_2_months = db.session.query(Loan.loan_no).filter(
        Loan.status.in_(['Active', 'Disbursed']),
        ~Loan.loan_no.in_(recent_paid_loans)
    ).count()

    # ----------------------------
    # SEND ALL TO TEMPLATE
    # ----------------------------
    return render_template(
        'admin/dashboard.html',
        total_members=total_members,
        total_savings=fmt(total_savings),
        total_share_capital=fmt(total_share_capital),
        total_loans=fmt(total_loans),

        members_zero_balance=members_zero_balance,
        installment_due=fmt(installment_due),

        principal_arrears=fmt(principal_arrears),
        interest_arrears=fmt(interest_arrears),

        loans_not_paid_2_months=loans_not_paid_2_months,
    )

# ---------- Savings Statement (PDF) ----------
@admin_bp.route('/reports/savings-statement', methods=['GET'])
@login_required
def savings_statement_form():
    # Simple form UI (uses base.html styles)
    return render_template('admin/savings_statement_form.html')


@admin_bp.route('/reports/savings-statement/pdf', methods=['POST', 'GET'])
@login_required
def savings_statement_pdf():
    """
    Generates a professional SACCO savings statement PDF with logo, header, and signature section.
    """
    from sacco_app.models import Member, SaccoAccount, Transaction
    from sqlalchemy import and_
    from flask import current_app, send_file
    from decimal import Decimal
    from io import BytesIO
    from datetime import datetime, date
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
    )
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

    # --- Parameters
    member_no = (request.values.get('member_no') or '').strip()
    start_str = request.values.get('start_date')
    end_str = request.values.get('end_date')
    today = date.today()

    if not member_no:
        flash("Member number is required.", "warning")
        return redirect(url_for('admin.savings_statement_form'))

    start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else date(today.year, 1, 1)
    end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today

    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        flash(f"Member {member_no} not found.", "danger")
        return redirect(url_for('admin.savings_statement_form'))

    savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
    if not savings_acc:
        flash("Savings account not found.", "danger")
        return redirect(url_for('admin.savings_statement_form'))

    account_no = savings_acc.account_number

    # --- Opening balance before period
    txns_before = Transaction.query.filter(
        Transaction.account_no == account_no,
        Transaction.bank_txn_date < datetime.combine(start_date, datetime.min.time())
    ).all()

    opening_balance = Decimal('0.00')
    for t in txns_before:
        opening_balance += Decimal(t.credit_amount or 0) - Decimal(t.debit_amount or 0)

    # --- Period transactions
    txns = Transaction.query.filter(
        Transaction.account_no == account_no,
        and_(
            Transaction.bank_txn_date >= datetime.combine(start_date, datetime.min.time()),
            Transaction.bank_txn_date <= datetime.combine(end_date, datetime.max.time())
        )
    ).order_by(Transaction.bank_txn_date.asc(), Transaction.id.asc()).all()

    rows = []
    run_bal = opening_balance
    total_debits = Decimal('0.00')
    total_credits = Decimal('0.00')

    def fmt(x): return f"{Decimal(x):,.2f}"
    def safe(s): return s or ""

    for t in txns:
        dr = Decimal(t.debit_amount or 0)
        cr = Decimal(t.credit_amount or 0)
        run_bal += cr - dr
        total_debits += dr
        total_credits += cr
        rows.append([
            t.bank_txn_date.strftime("%Y-%m-%d"),
            safe(t.narration),
            fmt(dr) if dr else "",
            fmt(cr) if cr else "",
            fmt(run_bal)
        ])

    closing_balance = opening_balance + total_credits - total_debits

    # --- PDF setup
    buffer = BytesIO()
    filename = f"SAVINGS_{member_no}_{start_date}_to_{end_date}.pdf"
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=2 * cm, bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle("header", fontSize=14, leading=18, alignment=TA_LEFT, textColor=colors.HexColor("#002060"))
    sub_style = ParagraphStyle("sub", fontSize=10, textColor=colors.gray, spaceAfter=4)
    normal_style = styles["Normal"]

    story = []

    # --- Professional Header (Logo + Info)
    logo_path = current_app.root_path + "/static/img/logo.png"
    try:
        logo = Image(logo_path, width=3.0 * cm, height=3.0 * cm)
    except Exception:
        logo = Paragraph("<b>SACCO LOGO</b>", styles["Normal"])

    header_info = [
        [Paragraph("<b>PCEA CHAIRETE SACCO LTD</b>", ParagraphStyle(
            "sacco_name", fontSize=14, alignment=TA_LEFT, textColor=colors.HexColor("#002060"), leading=16
        ))],
        [Spacer(1, 1)],
        [Paragraph(f"<b>Member:</b> {member.name} ({member.member_no})", sub_style)],
        [Paragraph(f"<b>Account:</b> {account_no}", sub_style)],
        [Paragraph(f"<b>Period:</b> {start_date} to {end_date}", sub_style)],
    ]

    header_table = Table(
        [[logo, Table(header_info, colWidths=[11 * cm])]],
        colWidths=[3 * cm, 12 * cm]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    # --- Divider line
    story.append(Table([[""]], colWidths=[20 * cm], style=[
        ('LINEBELOW', (0, 0), (-1, -1), 0.75, colors.HexColor("#004080"))
    ]))
    story.append(Spacer(1, 5))

    # --- Section title
    story.append(Paragraph("<b>Member Savings Statement</b>", ParagraphStyle(
        "section_title", fontSize=12, leading=14, textColor=colors.HexColor("#002060"), alignment=TA_CENTER
    )))

    # --- Transaction table
    data = [["Date", "Narration", "Debit (KSh)", "Credit (KSh)", "Balance (KSh)"]]
    data.extend(rows if rows else [["", "No transactions in this period.", "", "", ""]])

    tx_table = Table(data, colWidths=[2.2 * cm, 9 * cm, 2.8 * cm, 2.8 * cm, 3 * cm], repeatRows=1)
    tx_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white])
    ]))
    story.append(tx_table)
    story.append(Spacer(1, 20))

    # --- Signature section
    sig_data = [["Prepared By: ______________________", "Verified By: ______________________"]]
    sig_table = Table(sig_data, colWidths=[7 * cm, 7 * cm])
    sig_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(sig_table)

    # --- Footer
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(A4[0]-1.5*cm, 1.2*cm,
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Page {canvas.getPageNumber()}")
        canvas.setFont("Helvetica-Bold", 40)
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.drawCentredString(A4[0]/2, A4[1]/2, "CONFIDENTIAL")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')


### LOAN PDF STATEMENT GENERATION

# ---------- Loan Statement (PDF) ----------
@admin_bp.route('/reports/loan-statement', methods=['GET'])
@login_required
def loan_statement_form():
    """Simple form to choose member and date range for loan statement"""
    return render_template('admin/loan_statement_form.html')


@admin_bp.route('/reports/loan-statement/pdf', methods=['POST', 'GET'])
@login_required
def loan_statement_pdf():
    """
    Generates a professional SACCO loan statement PDF with logo, schedule, and summary section.
    """
    from sacco_app.models import Member, Loan, LoanSchedule
    from flask import current_app, send_file
    from sqlalchemy import and_
    from decimal import Decimal
    from io import BytesIO
    from datetime import datetime, date
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER

    # --- Parameters
    member_no = (request.values.get('member_no') or '').strip()
    start_str = request.values.get('start_date')
    end_str = request.values.get('end_date')
    today = date.today()

    if not member_no:
        flash("Member number is required.", "warning")
        return redirect(url_for('admin.loan_statement_form'))

    start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else date(today.year, 1, 1)
    end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else today

    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        flash(f"Member {member_no} not found.", "danger")
        return redirect(url_for('admin.loan_statement_form'))

    loan = Loan.query.filter(
        Loan.member_no == member_no,
        Loan.status.in_(["Active", "Disbursed", "Cleared"])
    ).order_by(Loan.disbursed_date.desc()).first()

    if not loan:
        flash("No loan found for this member.", "danger")
        return redirect(url_for('admin.loan_statement_form'))

    # --- Fetch loan schedules within range
    schedules = LoanSchedule.query.filter(
        and_(
            LoanSchedule.loan_no == loan.loan_no,
            LoanSchedule.due_date >= start_date,
            LoanSchedule.due_date <= end_date
        )
    ).order_by(LoanSchedule.installment_no.asc()).all()

    # --- Prepare PDF
    buffer = BytesIO()
    filename = f"LOAN_{loan.loan_no}_{start_date}_to_{end_date}.pdf"
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=2 * cm, bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle("header", fontSize=14, leading=18, alignment=TA_LEFT, textColor=colors.HexColor("#002060"))
    sub_style = ParagraphStyle("sub", fontSize=10, textColor=colors.gray, spaceAfter=4)
    normal_style = styles["Normal"]

    story = []

    # --- Professional Header (same as savings statement)
    logo_path = current_app.root_path + "/static/img/logo.png"
    try:
        logo = Image(logo_path, width=3.0 * cm, height=3.0 * cm)
    except Exception:
        logo = Paragraph("<b>SACCO LOGO</b>", styles["Normal"])

    header_info = [
        [Paragraph("<b><u>PCEA CHAIRETE SACCO LTD</u></b>", ParagraphStyle(
            "sacco_name", fontSize=14, alignment=TA_LEFT, textColor=colors.HexColor("#002060"), leading=16
        ))],
        [Spacer(1, 3)],
        [Paragraph(f"<b>Member:</b> {member.name} ({member.member_no})", sub_style)],
        [Paragraph(f"<b>Loan No:</b> {loan.loan_no}", sub_style)],
        [Paragraph(f"<b>Disbursed:</b> {loan.disbursed_date.strftime('%Y-%m-%d')} | <b>Type:</b> {loan.loan_type.title()}", sub_style)],
        [Paragraph(f"<b>Period:</b> {start_date} to {end_date}", sub_style)],
    ]

    header_table = Table(
        [[logo, Table(header_info, colWidths=[11 * cm])]],
        colWidths=[3 * cm, 12 * cm]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    # --- Divider line
    story.append(Table([[""]], colWidths=[17 * cm], style=[
        ('LINEBELOW', (0, 0), (-1, -1), 0.75, colors.HexColor("#004080"))
    ]))
    story.append(Spacer(1, 10))

    # --- Title
    story.append(Paragraph("<b>Loan Statement</b>", ParagraphStyle(
        "section_title", fontSize=12, leading=14, textColor=colors.HexColor("#002060"), alignment=TA_CENTER
    )))
    story.append(Spacer(1, 10))

    # --- Summary Section
    principal = Decimal(loan.loan_amount or 0)
    total_principal_paid = sum(Decimal(s.principal_paid or 0) for s in loan.schedules)
    total_interest_paid = sum(Decimal(s.interest_paid or 0) for s in loan.schedules)
    total_due = sum(Decimal(s.principal_due or 0) + Decimal(s.interest_due or 0) for s in loan.schedules)
    outstanding_balance = Decimal(loan.balance or 0)

    summary_data = [
        ["Principal Amount", f"KSh {principal:,.2f}"],
        ["Total Paid (Principal + Interest)", f"KSh {(total_principal_paid + total_interest_paid):,.2f}"],
        ["Outstanding Balance", f"KSh {outstanding_balance:,.2f}"],
    ]
    summary_table = Table(summary_data, colWidths=[8 * cm, 6 * cm])
    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 12))

    # --- Schedule Table
    data = [["No", "Due Date", "Principal Due", "Interest Due", "Total Due", "Principal Paid", "Interest Paid", "Balance"]]

    if not schedules:
        data.append(["", "No installments in this period", "", "", "", "", "", ""])
    else:
        for s in schedules:
            total_due = Decimal(s.principal_due or 0) + Decimal(s.interest_due or 0)
            total_paid = Decimal(s.principal_paid or 0) + Decimal(s.interest_paid or 0)
            data.append([
                s.installment_no,
                s.due_date.strftime("%Y-%m-%d"),
                f"{Decimal(s.principal_due or 0):,.2f}",
                f"{Decimal(s.interest_due or 0):,.2f}",
                f"{total_due:,.2f}",
                f"{Decimal(s.principal_paid or 0):,.2f}",
                f"{Decimal(s.interest_paid or 0):,.2f}",
                f"{Decimal(s.principal_balance or 0):,.2f}"
            ])

    schedule_table = Table(data, colWidths=[1.2*cm, 2.5*cm, 2.6*cm, 2.6*cm, 2.6*cm, 2.6*cm, 2.6*cm, 2.8*cm], repeatRows=1)
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white])
    ]))
    story.append(schedule_table)
    story.append(Spacer(1, 20))

    # --- Signature Section
    sig_data = [["Prepared By: ______________________", "Verified By: ______________________"]]
    sig_table = Table(sig_data, colWidths=[7 * cm, 7 * cm])
    sig_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(sig_table)

    # --- Footer
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(A4[0] - 1.5 * cm, 1.2 * cm,
                               f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Page {canvas.getPageNumber()}")
        canvas.setFont("Helvetica-Bold", 40)
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.drawCentredString(A4[0] / 2, A4[1] / 2, "CONFIDENTIAL")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

@admin_bp.route('/search_member', methods=['GET'])
@login_required
def search_member():
    """
    Allows searching for a member by member number, name, ID, or phone.
    Returns JSON for AJAX or renders the search form page.
    """
    from sacco_app.models import Member
    from sqlalchemy import or_
    from flask import request, jsonify, render_template

    query = request.args.get('query', '').strip()

    # If AJAX search (query param provided)
    if query:
        results = Member.query.filter(
            or_(
                Member.member_no.ilike(f"%{query}%"),
                Member.name.ilike(f"%{query}%"),
                Member.id_no.ilike(f"%{query}%"),
                Member.phone.ilike(f"%{query}%")
            )
        ).limit(20).all()

        # ✅ Return JSON cleanly for AJAX
        return jsonify([
            {
                "member_no": m.member_no,
                "name": m.name,
                "id_no": m.id_no,
                "phone": m.phone,
            }
            for m in results
        ])

    # ✅ If no query param → render HTML page
    return render_template('admin/search_member.html')

@admin_bp.route('/member/<member_no>', methods=['GET'])
@login_required
def view_member(member_no):
    """
    Displays member profile details when clicked from search results.
    """
    from sacco_app.models import Member, SaccoAccount, Loan

    member = Member.query.filter_by(member_no=member_no).first()

    if not member:
        flash(f"Member {member_no} not found.", "danger")
        return redirect(url_for('admin.search_member'))

    # Get member's savings and loans
    savings = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
    loans = Loan.query.filter_by(member_no=member_no).all()

    return render_template(
        'admin/view_member.html',
        member=member,
        savings=savings,
        loans=loans
    )

#excell reports

@admin_bp.route('/reports/member_loan_summary', methods=['GET'])
@login_required
def generate_member_loan_summary():
    """
    Generates an Excel report summarizing each member's savings, loan, and overdue dues.
    Overdue (loan dues) considers only unpaid principal and interest for schedules with due_date <= today.
    """
    from sacco_app.models import Member, SaccoAccount, Loan, LoanSchedule
    from decimal import Decimal
    from datetime import date
    import pandas as pd
    from io import BytesIO
    from flask import send_file

    today = date.today()
    report_rows = []

    members = Member.query.all()

    for member in members:
        # Savings balance
        savings_acc = SaccoAccount.query.filter_by(member_no=member.member_no, account_type='SAVINGS').first()
        savings_balance = savings_acc.balance if savings_acc else Decimal('0.00')

        # Most recent loan (adjust if you want to aggregate multiple loans)
        loan = Loan.query.filter_by(member_no=member.member_no).order_by(Loan.loan_no.desc()).first()
        if loan:
            original_loan_amount = loan.loan_amount or Decimal('0.00')
            loan_balance = loan.balance or Decimal('0.00')
        else:
            original_loan_amount = Decimal('0.00')
            loan_balance = Decimal('0.00')

        # Compute overdue amounts: sum unpaid principal & interest where due_date <= today
        overdue_principal = Decimal('0.00')
        overdue_interest = Decimal('0.00')

        if loan:
            overdue_schedules = LoanSchedule.query.filter(
                LoanSchedule.loan_no == loan.loan_no,
                LoanSchedule.due_date <= today
            ).all()

            for s in overdue_schedules:
                # outstanding portions (may be zero or positive)
                unpaid_principal = (s.principal_due or Decimal('0.00')) - (s.principal_paid or Decimal('0.00'))
                unpaid_interest = (s.interest_due or Decimal('0.00')) - (s.interest_paid or Decimal('0.00'))

                if unpaid_principal > 0:
                    overdue_principal += unpaid_principal
                if unpaid_interest > 0:
                    overdue_interest += unpaid_interest

        total_overdue = overdue_principal + overdue_interest

        report_rows.append({
            'Member No': member.member_no,
            'Member Name': member.name or '',
            'Savings Balance': float(savings_balance),
            'Original Loan Amount': float(original_loan_amount),
            'Loan Balance': float(loan_balance),
            'Overdue Principal': float(overdue_principal),
            'Overdue Interest': float(overdue_interest),
            'Total Overdue (Dues)': float(total_overdue)
        })

    # Create DataFrame
    df = pd.DataFrame(report_rows, columns=[
        'Member No', 'Member Name', 'Savings Balance', 'Original Loan Amount',
        'Loan Balance', 'Overdue Principal', 'Overdue Interest', 'Total Overdue (Dues)'
    ])

    # Write to Excel in-memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Member Loan Summary', index=False)
        ws = writer.sheets['Member Loan Summary']
        ws.autofilter(0, 0, len(df), len(df.columns) - 1)
        # set column widths nicely
        ws.set_column(0, 1, 20)  # Member No, Member Name
        ws.set_column(2, 4, 18)  # Balances and amounts
        ws.set_column(5, 7, 18)  # Overdue columns

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='member_loan_summary.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


#report for guarantors

@admin_bp.route('/reports/guarantor_report', methods=['GET'])
@login_required
def generate_guarantor_report():
    """
    Generates an Excel report showing all guarantors for each active or disbursed loan.
    Includes borrower info, guarantor info, and guaranteed amounts.
    """
    from sacco_app.models import Member, Loan, LoanGuarantor, SaccoAccount
    from decimal import Decimal
    import pandas as pd
    from io import BytesIO
    from flask import send_file

    report_data = []

    # Fetch all loans that have guarantors
    loans = Loan.query.all()

    for loan in loans:
        borrower = Member.query.filter_by(member_no=loan.member_no).first()
        borrower_name = borrower.name if borrower else "Unknown Member"

        # Loan balance
        loan_balance = loan.balance or Decimal('0.00')

        # Get all guarantors for this loan
        guarantors = LoanGuarantor.query.filter_by(loan_no=loan.loan_no).all()

        for g in guarantors:
            guarantor_member = Member.query.filter_by(member_no=g.guarantor_no).first()
            guarantor_name = guarantor_member.name if guarantor_member else "Unknown Guarantor"

            # Guarantor savings balance
            savings_acc = SaccoAccount.query.filter_by(
                member_no=g.member_no, account_type='SAVINGS'
            ).first()
            guarantor_savings = savings_acc.balance if savings_acc else Decimal('0.00')

            report_data.append({
                "Loan No": loan.loan_no,
                "Borrower No": loan.member_no,
                "Borrower Name": borrower_name,
                "Loan Amount": float(loan.loan_amount),
                "Loan Balance": float(loan_balance),
                "Guarantor No": g.guarantor_no,
                "Guarantor Name": guarantor_name,
                "Amount Guaranteed": float(g.amount_guaranteed),
                "Guarantor Savings": float(guarantor_savings),
            })

    # --- Create DataFrame
    df = pd.DataFrame(report_data, columns=[
        "Loan No", "Borrower No", "Borrower Name", "Loan Amount", "Loan Balance",
        "Guarantor No", "Guarantor Name", "Amount Guaranteed", "Guarantor Savings"
    ])

    # --- Create Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Guarantor Report', index=False)
        ws = writer.sheets['Guarantor Report']
        ws.autofilter(0, 0, len(df), len(df.columns) - 1)
        ws.set_column(0, len(df.columns) - 1, 20)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='guarantor_report.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


#pay loan from savings

@admin_bp.route('/api/member_loan_info', methods=['GET'])
@login_required
def get_member_loan_info():
    """
    Returns member name, savings balance, and active loan info for use in AJAX lookups.
    """
    from sacco_app.models import Member, SaccoAccount, Loan, LoanSchedule
    from decimal import Decimal
    from datetime import date
    from flask import jsonify, request

    member_no = request.args.get('member_no', '').strip()
    if not member_no:
        return jsonify({"error": "Missing member number"}), 400

    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        return jsonify({"error": "Member not found"}), 404

    savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
    savings_balance = float(savings_acc.balance) if savings_acc else 0.00

    loan = Loan.query.filter_by(member_no=member_no, status='Active').first()
    if not loan:
        return jsonify({
            "member_name": member.name,
            "savings_balance": savings_balance,
            "loan_balance": 0.00,
            "amount_due": 0.00
        })

    # Get total amount due (principal + interest due on or before today)
    from sqlalchemy import func
    total_due = db.session.query(
        func.sum((LoanSchedule.principal_due - LoanSchedule.principal_paid) +
                 (LoanSchedule.interest_due - LoanSchedule.interest_paid))
    ).filter(
        LoanSchedule.loan_no == loan.loan_no,
        LoanSchedule.due_date <= date.today()
    ).scalar() or Decimal('0.00')

    return jsonify({
        "member_name": member.name,
        "savings_balance": float(savings_balance),
        "loan_balance": float(loan.balance or 0),
        "amount_due": float(total_due)
    })

@admin_bp.route('/loans/repay_from_savings', methods=['GET', 'POST'])
@login_required
def repay_loan_from_savings():
    """
    Allows repayment of an active loan using funds from member's savings account.
    Now includes Loan Control Account posting.
    """
    from sacco_app.models import Member, Loan, LoanSchedule, SaccoAccount, Transaction
    from decimal import Decimal
    from datetime import datetime
    import uuid

    if request.method == 'POST':
        member_no = request.form.get('member_no').strip()
        amount = Decimal(request.form.get('amount', '0'))
        narration = request.form.get('narration') or "Loan repayment from savings"
        txn_date = datetime.now()

        member = Member.query.filter_by(member_no=member_no).first()
        if not member:
            flash(f"Member {member_no} not found.", "danger")
            return redirect(url_for('admin.repay_loan_from_savings'))

        savings_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type='SAVINGS').first()
        if not savings_acc:
            flash("Member has no savings account.", "danger")
            return redirect(url_for('admin.repay_loan_from_savings'))

        if savings_acc.balance < amount:
            flash("Insufficient savings balance.", "danger")
            return redirect(url_for('admin.repay_loan_from_savings'))

        loan = Loan.query.filter_by(member_no=member_no, status='Active').first()
        if not loan:
            flash("No active loan found for this member.", "danger")
            return redirect(url_for('admin.repay_loan_from_savings'))

        # --- Get GL Accounts
        loan_principal_acc = SaccoAccount.query.filter_by(member_no=member_no,account_type='LOAN').first()
        loan_control_acc = SaccoAccount.query.filter_by(account_number='M000GL_LOAN').first()
        interest_income_acc = SaccoAccount.query.filter_by(account_number='M000GL_LN_INT').first()
        savings_control_acc = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()

        if not all([loan_principal_acc, interest_income_acc, savings_control_acc, loan_control_acc]):
            flash("Required GL accounts missing (Loan/Savings/Control).", "danger")
            return redirect(url_for('admin.repay_loan_from_savings'))

        due_schedule = LoanSchedule.query.filter(
            LoanSchedule.loan_no == loan.loan_no,
            LoanSchedule.status == 'DUE'
        ).order_by(LoanSchedule.due_date).first()

        if not due_schedule:
            flash("No due schedule found for repayment.", "warning")
            return redirect(url_for('admin.repay_loan_from_savings'))

        remaining = amount
        txn_ref = f"TXN{uuid.uuid4().hex[:10].upper()}"
        transactions = []

        # 1️⃣ Deduct from member savings (Credit)
        savings_acc.balance -= amount
        txn_savings = Transaction(
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
            member_no=member_no,
            account_no=savings_acc.account_number,
            gl_account='SAVINGS',
            tran_type='LIABILITY',
            debit_amount=amount,
            credit_amount=Decimal('0'),
            reference=txn_ref,
            narration=f"Loan repayment from savings",
            bank_txn_date=txn_date,
            posted_by=current_user.username,
            running_balance=savings_acc.balance
        )
        transactions.append(txn_savings)

        # 2️⃣ Debit savings control (Dr)
        savings_control_acc.balance -= amount
        txn_ctrl = Transaction(
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
            member_no='M000GL',
            account_no=savings_control_acc.account_number,
            gl_account='SAVINGS_CONTROL',
            tran_type='LIABILITY',
            debit_amount=Decimal('0'),
            credit_amount=amount,
            reference=txn_ref,
            narration=f"Loan repayment (from savings) for {member_no}",
            bank_txn_date=txn_date,
            posted_by=current_user.username,
            running_balance=savings_control_acc.balance
        )
        transactions.append(txn_ctrl)

        # 3️⃣ Pay Interest (Credit Income)
        interest_due = due_schedule.interest_due - due_schedule.interest_paid
        if remaining > 0 and interest_due > 0:
            pay_interest = min(remaining, interest_due)
            remaining -= pay_interest
            due_schedule.interest_paid += pay_interest
            interest_income_acc.balance += pay_interest

            txn_int = Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                member_no=member_no,
                account_no=interest_income_acc.account_number,
                gl_account='INTEREST_INCOME',
                tran_type='INCOME',
                debit_amount=Decimal('0'),
                credit_amount=pay_interest,
                reference=txn_ref,
                narration=f"Interest repayment - {member_no}",
                bank_txn_date=txn_date,
                posted_by=current_user.username,
                running_balance=interest_income_acc.balance
            )
            transactions.append(txn_int)

        # 4️⃣ Pay Principal (reduce loan & loan control)
        principal_due = due_schedule.principal_due - due_schedule.principal_paid
        if remaining > 0 and principal_due > 0:
            pay_principal = min(remaining, principal_due)
            remaining -= pay_principal
            due_schedule.principal_paid += pay_principal
            loan.balance -= pay_principal
            loan_principal_acc.balance -= pay_principal
            loan_control_acc.balance -= pay_principal  # <-- NEW POSTING HERE

            # a) Credit Loan Control
            txn_ctrl_credit = Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                member_no='M000GL',
                account_no=loan_control_acc.account_number,
                gl_account='LOAN_CONTROL',
                tran_type='ASSET',
                debit_amount=Decimal('0'),
                credit_amount=pay_principal,
                reference=txn_ref,
                narration=f"Loan control credit for {member_no}",
                bank_txn_date=txn_date,
                posted_by=current_user.username,
                running_balance=loan_control_acc.balance
            )
            transactions.append(txn_ctrl_credit)

            # b) Debit Loan GL
            txn_principal = Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                member_no=member_no,
                account_no=loan_principal_acc.account_number,
                gl_account='LOAN_PRINCIPAL',
                tran_type='ASSET',
                debit_amount=pay_principal,
                credit_amount=Decimal('0'),
                reference=txn_ref,
                narration=f"Loan principal repayment - {member_no}",
                bank_txn_date=txn_date,
                posted_by=current_user.username,
                running_balance=loan_principal_acc.balance
            )
            transactions.append(txn_principal)

        # 5️⃣ Mark schedule as PAID if fully settled
        if (due_schedule.principal_paid >= due_schedule.principal_due) and (due_schedule.interest_paid >= due_schedule.interest_due):
            due_schedule.status = 'PAID'

        db.session.add_all(transactions)
        db.session.commit()

        flash(f"Loan repayment of KSh {amount} from savings posted successfully.", "success")
        return redirect(url_for('admin.repay_loan_from_savings'))

    return render_template('admin/repay_loan_from_savings.html')

@admin_bp.route('/transactions/reverse', methods=['GET', 'POST'])
@login_required
def reverse_transaction():
    """
    Allows authorized users to reverse a transaction by reference.
    It posts exact opposite entries for the same accounts and updates balances.
    """
    from sacco_app.models import Transaction, SaccoAccount
    from decimal import Decimal
    from datetime import datetime
    import uuid

    if request.method == 'POST':
        ref_no = request.form.get('reference').strip()
        reason = request.form.get('reason', '').strip()

        if not ref_no:
            flash("Reference number is required.", "danger")
            return redirect(url_for('admin.reverse_transaction'))

        # Find transactions with this reference
        original_txns = Transaction.query.filter_by(reference=ref_no).all()

        if not original_txns:
            flash(f"No unreversed transactions found with reference {ref_no}.", "warning")
            return redirect(url_for('admin.reverse_transaction'))

        reversal_ref = f"REV{uuid.uuid4().hex[:10].upper()}"
        reversal_txns = []

        for txn in original_txns:
            # Fetch account
            acc = SaccoAccount.query.filter_by(account_number=txn.account_no).first()
            if not acc:
                continue

            # Reverse the amounts
            debit = txn.credit_amount
            credit = txn.debit_amount

            # Update account running balance
            if debit > 0:
                acc.balance += debit
            if credit > 0:
                acc.balance -= credit

            # Create reversal transaction
            rev = Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                member_no=txn.member_no,
                account_no=txn.account_no,
                gl_account=txn.gl_account,
                tran_type=txn.tran_type,
                debit_amount=debit,
                credit_amount=credit,
                reference=reversal_ref,
                narration=f"Reversal of {txn.txn_no}: {reason}",
                bank_txn_date=datetime.now(),
                posted_by=current_user.username,
                running_balance=acc.balance,
                created_at=datetime.now()
            )
            reversal_txns.append(rev)


        db.session.add_all(reversal_txns)
        db.session.commit()

        flash(f"Transactions reversed successfully. Reversal Ref: {reversal_ref}", "success")
        return redirect(url_for('admin.reverse_transaction'))

    return render_template('admin/reverse_transaction.html')

## generate trial balance and balance sheet
@admin_bp.route('/reports/trial_balance', methods=['GET'])
@login_required
def trial_balance():
    """Generate Trial Balance from GL account balances."""

    from sacco_app.models import SaccoAccount
    from decimal import Decimal

    accounts = SaccoAccount.query.all()

    trial_data = []
    total_debit = Decimal('0.00')
    total_credit = Decimal('0.00')

    for acc in accounts:
        debit = Decimal("0.00")
        credit = Decimal("0.00")

        # Normal accounting treatment
        if acc.account_type in ["ASSET", "EXPENSE"]:
            if acc.balance >= 0:
                debit = acc.balance
            else:
                credit = abs(acc.balance)

        elif acc.account_type in ["LIABILITY", "EQUITY", "INCOME"]:
            if acc.balance >= 0:
                credit = acc.balance
            else:
                debit = abs(acc.balance)

        trial_data.append({
            "account_no": acc.account_number,
            "account_type": acc.account_type,
            "debit": float(debit),
            "credit": float(credit)
        })

        total_debit += debit
        total_credit += credit

    return render_template(
        "admin/trial_balance.html",
        data=trial_data,
        total_debit=float(total_debit),
        total_credit=float(total_credit)
    )


## balance sheet route

@admin_bp.route('/reports/balance_sheet', methods=['GET'])
@login_required
def balance_sheet():
    """Generate Balance Sheet."""

    from sacco_app.models import SaccoAccount
    from decimal import Decimal

    accounts = SaccoAccount.query.all()

    assets = []
    liabilities = []
    equity = []

    total_assets = Decimal('0.00')
    total_liabilities = Decimal('0.00')
    total_equity = Decimal('0.00')

    for acc in accounts:
        if acc.account_type == "ASSET":
            assets.append(acc)
            total_assets += acc.balance

        elif acc.account_type == "LIABILITY":
            liabilities.append(acc)
            total_liabilities += acc.balance

        elif acc.account_type in ["EQUITY", "INCOME"]:  
            equity.append(acc)
            total_equity += acc.balance

    # EQUITY adjustment: equity = income + capital - expenses are already included
    return render_template(
        "admin/balance_sheet.html",
        assets=assets, liabilities=liabilities, equity=equity,
        total_assets=float(total_assets),
        total_liabilities=float(total_liabilities),
        total_equity=float(total_equity),
        total_side=float(total_liabilities + total_equity)
    )

## income and expenditure account

@admin_bp.route('/reports/income_statement', methods=['GET'])
@login_required
def income_statement():
    """
    Generates SACCO Income Statement: Income - Expenses.
    """
    from sacco_app.models import SaccoAccount
    from decimal import Decimal

    income_accounts = SaccoAccount.query.filter_by(account_type='INCOME').all()
    expense_accounts = SaccoAccount.query.filter_by(account_type='EXPENSE').all()

    total_income = sum([acc.balance for acc in income_accounts])
    total_expenses = sum([acc.balance for acc in expense_accounts])

    net_income = total_income - total_expenses

    return render_template(
        "admin/income_statement.html",
        income_accounts=income_accounts,
        expense_accounts=expense_accounts,
        total_income=total_income,
        total_expenses=total_expenses,
        net_income=net_income
    )


### cash Flow 

@admin_bp.route('/reports/cashflow_statement', methods=['GET'])
@login_required
def cashflow_statement():
    """
    Generates simplified SACCO Cash Flow Statement using indirect method.
    """
    from sacco_app.models import SaccoAccount, Transaction
    from decimal import Decimal

    # 1️⃣ Get Net Income from P&L (Income - Expenses)
    income_accounts = SaccoAccount.query.filter_by(account_type='INCOME').all()
    expense_accounts = SaccoAccount.query.filter_by(account_type='EXPENSE').all()

    net_income = sum([acc.balance for acc in income_accounts]) - \
                 sum([acc.balance for acc in expense_accounts])

    # 2️⃣ Change in Working Capital (Assets & Liabilities except cash)
    asset_accounts = SaccoAccount.query.filter_by(account_type='ASSET').all()
    liability_accounts = SaccoAccount.query.filter_by(account_type='LIABILITY').all()

    working_capital_change = sum([acc.balance for acc in liability_accounts]) - \
                             sum([acc.balance for acc in asset_accounts])

    # 3️⃣ Investing = Loans disbursed (negative) and investments posted
    investing_accounts = SaccoAccount.query.filter(
        SaccoAccount.account_number.like('M000GL_INVEST%')
    ).all()

    investing_cashflow = sum([acc.balance for acc in investing_accounts])

    # 4️⃣ Financing = Savings deposits (positive) - withdrawals (negative)
    savings_control = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()
    financing_cashflow = savings_control.balance if savings_control else 0

    # 5️⃣ Total Cash Flow
    net_cashflow = net_income + working_capital_change + investing_cashflow + financing_cashflow

    # 6️⃣ Ending cash balance
    cash_account = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
    ending_cash = cash_account.balance if cash_account else Decimal('0.00')

    return render_template(
        "admin/cashflow_statement.html",
        net_income=net_income,
        working_capital_change=working_capital_change,
        investing_cashflow=investing_cashflow,
        financing_cashflow=financing_cashflow,
        net_cashflow=net_cashflow,
        ending_cash=ending_cash
    )


## GL-Reports

@admin_bp.route('/reports/gl', methods=['GET', 'POST'])
@login_required
def gl_report():
    """
    Generates GL Drill-down report for any SaccoAccount.
    """
    from sacco_app.models import SaccoAccount, Transaction

    accounts = SaccoAccount.query.all()
    transactions = []
    selected_acc = None

    if request.method == 'POST':
        acc_no = request.form.get('account_no')
        selected_acc = SaccoAccount.query.filter_by(account_number=acc_no).first()

        transactions = Transaction.query.filter_by(account_no=acc_no)\
                                        .order_by(Transaction.created_at)\
                                        .all()

    return render_template(
        "admin/gl_report.html",
        accounts=accounts,
        selected_acc=selected_acc,
        transactions=transactions
    )


#### auditing
def log_activity(action, details=None):
    from flask import request
    from sacco_app.models import AuditLog

    ip = request.remote_addr
    
    log = AuditLog(
        user_id=current_user.id,
        action=action,
        details=details,
        ip_address=ip
    )
    db.session.add(log)
    db.session.commit()


@admin_bp.route('/audit_logs')
@login_required
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("admin/audit_logs.html", logs=logs)


from openpyxl import Workbook
from flask import send_file
import io

@admin_bp.route('/export_audit_logs')
@login_required
def export_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Audit Logs"

    # Headers
    ws.append(["User", "Action", "Details", "IP Address", "Timestamp"])

    # Data rows
    for log in logs:
        ws.append([
            log.user.username if log.user else "SYSTEM",
            log.action,
            log.details,
            log.ip_address,
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])

    # Save to memory
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name="audit_logs.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
