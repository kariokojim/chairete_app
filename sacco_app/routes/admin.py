from sacco_app.utils.audit import log_activity
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
from flask_mail import Message
from datetime import datetime
from flask import current_app
from sqlalchemy import text   
from sacco_app.models import NextOfKin, Beneficiary
from sacco_app.utils.receipt_utils import generate_receipt_no
from sacco_app.utils.loan_email_utils import send_loan_schedule_email
from sacco_app.utils.async_tasks import run_async
from sacco_app.utils.receipt_tasks import send_receipt_background





def role_required_admin():
    return current_user.is_authenticated and current_user.role == 'admin'


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# List Users
@admin_bp.route('/users/list', methods=['GET'])
@login_required
def list_users():
    if current_user.role != 'admin':
        flash("You are not authorized to view user management.", "danger")
        return redirect(request.referrer or url_for('admin.dashboard'))

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/list_users.html', users=users)


# Create User (GET: show form, POST: create user)
@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role != 'admin':
        flash("You are not authorized to Create a new user.", "danger")
        return redirect(request.referrer or url_for('admin.dashboard'))
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
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
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
        txn2 = Transaction(
            txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
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
        flash(f"✅ KES {amount:,.2f} successfully posted to {member_no}", "success")

        # -------------------------------------------------
        # 1️⃣ Find the MEMBER savings credit transaction
        # -------------------------------------------------
        member_txn = None
        for t in transactions:
            if t.account_no == member_savings_acc.account_number and t.credit_amount > 0:
                member_txn = t
                break

        if not member_txn:
            flash("Deposit posted but receipt could not be generated.", "warning")
            return redirect(url_for('admin.list_member_deposits'))

        # -------------------------------------------------
        # 2️⃣ Fetch member
        # -------------------------------------------------
        member = Member.query.filter_by(member_no=member_txn.member_no).first()

        # -------------------------------------------------
        # 3️⃣ Queue receipt + email in background
        # -------------------------------------------------
        if member and member.email:
            receipt_no = generate_receipt_no()

            run_async(
                current_app._get_current_object(),
                send_receipt_background,
                member,
                member_txn,
                receipt_no
            )

        else:
            flash("Deposit posted but member has no email for receipt.", "warning")


    except Exception as e:
        db.session.rollback()
        flash(f"Error posting deposit: {str(e)}", "danger")

    return redirect(url_for('admin.post_transaction'))
    
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
            Transaction.tran_type.in_(['SAVINGS', 'LIABILITY'])
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
def generate_schedule_pdf(loan, schedules, member):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>Loan Repayment Schedule</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Member: {member.name}", styles['Normal']))
    elements.append(Paragraph(f"Loan No: {loan.loan_no}", styles['Normal']))
    elements.append(Paragraph(f"Loan Amount: {loan.loan_amount:,.2f}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [["Inst#", "Due Date", "Principal", "Interest", "Premium", "Total", "Balance"]]

    for s in schedules:
        premium = getattr(s, "premium_due", Decimal("0.00"))
        total_due = (s.principal_due + s.interest_due + premium).quantize(Decimal("0.01"))

        data.append([
            s.installment_no,
            s.due_date.strftime("%d-%b-%Y"),
            f"{s.principal_due:,.2f}",
            f"{s.interest_due:,.2f}",
            f"{premium:,.2f}",
            f"{total_due:,.2f}",
            f"{s.principal_balance:,.2f}",
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer


"""Loan disbursement route – creates loan, GL entries, guarantors, and schedules."""
from flask import render_template, request, flash, redirect, url_for, send_file, current_app
from flask_login import login_required, current_user
from decimal import Decimal
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid, re
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from sacco_app.models import (
    Member, Loan, LoanGuarantor, LoanSchedule,
    SaccoAccount, Transaction
)

@admin_bp.route('/loans/disburse', methods=['GET', 'POST'])
@login_required
def disburse_loan():

    form = LoanDisbursementForm()

    # ---------------- GUARANTOR PARSER ----------------
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
                    parsed.append({
                        "member_no": gno,
                        "amount_guaranteed": Decimal(str(gamt))
                    })
                except:
                    parsed.append({
                        "member_no": gno,
                        "amount_guaranteed": Decimal("0.00")
                    })

        return parsed

    # ---------------- FORM VALIDATION ----------------
    if request.method == 'POST' and not form.validate_on_submit():
        flash(f"Form validation failed: {form.errors}", "warning")
        return render_template('admin/disburse_loan.html', form=form)

    if form.validate_on_submit():
        try:
            # ---------------- INPUTS ----------------
            member_no = form.member_no.data.strip()
            loan_amount = Decimal(str(form.loan_amount.data)).quantize(Decimal('0.01'))
            loan_period = int(form.loan_period.data)
            loan_type = (getattr(form, 'loan_type', None).data or 'normal').lower().strip()
            guarantors = parse_guarantors(request.form)

            # ---------------- CONSTANTS ----------------
            PROCESSING_FEE_RATE = Decimal('0.005')   # 0.5%
            INSURANCE_RATE = Decimal('0.015')        # 1.5%
            ANNUAL_RATE = Decimal('15.0')

            monthly_rate = (ANNUAL_RATE / Decimal('100')) / Decimal('12')

            processing_fee = (loan_amount * PROCESSING_FEE_RATE).quantize(Decimal('0.01'))
            insurance_total = (loan_amount * INSURANCE_RATE).quantize(Decimal('0.01'))
            monthly_premium = (insurance_total / loan_period).quantize(Decimal('0.01'))

            net_disbursed = (loan_amount - processing_fee).quantize(Decimal('0.01'))

            # ---------------- MEMBER VALIDATION ----------------
            member = Member.query.filter_by(member_no=member_no).first()
            if not member:
                flash("Member not found.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            savings_acc = SaccoAccount.query.filter_by(
                member_no=member_no,
                account_type='SAVINGS'
            ).first()

            if not savings_acc or savings_acc.balance <= 0:
                flash("Member has insufficient savings.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            if loan_amount > (savings_acc.balance * 3):
                flash("Loan exceeds 3× savings.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # ---------------- ACTIVE LOAN CHECK ----------------
            active_loan = Loan.query.filter(
                Loan.member_no == member_no,
                Loan.status.in_(["Active", "Disbursed"]),
                Loan.balance > 0
            ).first()

            if loan_type != 'topup' and active_loan:
                flash("Member already has an active loan.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            if loan_type == 'topup' and not active_loan:
                flash("No active loan to top-up.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # ---------------- GL ACCOUNTS ----------------
            gl_cash = SaccoAccount.query.filter_by(account_number='M000GL_CASH').first()
            gl_loan_control = SaccoAccount.query.filter_by(account_number='M000GL_LOAN').first()
            gl_fee_income = SaccoAccount.query.filter_by(account_number='M000GL_REG_FEE').first()

            if not all([gl_cash, gl_loan_control, gl_fee_income]):
                flash("Missing GL accounts.", "danger")
                return render_template('admin/disburse_loan.html', form=form)

            # ---------------- MEMBER LOAN ACCOUNTS ----------------
            loan_acct_no = f"{member_no}_LOAN"
            int_acct_no = f"{member_no}_INTEREST"

            loan_acct = SaccoAccount.query.filter_by(account_number=loan_acct_no).first()
            if not loan_acct:
                loan_acct = SaccoAccount(
                    member_no=member_no,
                    account_number=loan_acct_no,
                    account_type='LOAN',
                    created_by=current_user.username,
                    balance=Decimal('0.00')
                )
                db.session.add(loan_acct)

            int_acct = SaccoAccount.query.filter_by(account_number=int_acct_no).first()
            if not int_acct:
                int_acct = SaccoAccount(
                    member_no=member_no,
                    account_number=int_acct_no,
                    account_type='INTEREST',
                    created_by=current_user.username,
                    balance=Decimal('0.00')
                )
                db.session.add(int_acct)

            db.session.flush()

            # ---------------- LOAN NUMBER ----------------
            last_loan = Loan.query.order_by(Loan.id.desc()).first()
            loan_no = f"LN{(last_loan.id + 1) if last_loan else 1:04d}"

            # ---------------- CREATE LOAN ----------------
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

            # ---------------- SAVE GUARANTORS ----------------
            for g in guarantors:
                db.session.add(LoanGuarantor(
                    loan_no=loan_no,
                    guarantor_no=g["member_no"],
                    member_no=member_no,
                    amount_guaranteed=g["amount_guaranteed"]
                ))

            # ---------------- GL POSTINGS ----------------
            txn_ref = f"TXN{uuid.uuid4().hex[:10].upper()}"

            loan_acct.balance += loan_amount
            gl_loan_control.balance += loan_amount
            gl_fee_income.balance += processing_fee
            gl_cash.balance -= net_disbursed

            # ---------------- EMI CALCULATION ----------------
            if monthly_rate > 0:
                emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** loan_period) / \
                      ((1 + monthly_rate) ** loan_period - 1)
            else:
                emi = loan_amount / loan_period

            emi = emi.quantize(Decimal('0.01'))

            # ---------------- SCHEDULE GENERATION ----------------
            principal_balance = loan_amount
            first_due_date = datetime.now().date() + relativedelta(months=1)

            for i in range(1, loan_period + 1):
                interest_due = (principal_balance * monthly_rate).quantize(Decimal('0.01'))
                principal_due = (emi - interest_due).quantize(Decimal('0.01'))

                if i == loan_period:
                    principal_due = principal_balance
                due_date = first_due_date + relativedelta(months=i - 1)

                extra_fee = processing_fee if i == 1 else Decimal('0.00')
                new_balance = (principal_balance - principal_due).quantize(Decimal('0.01'))
                total_due=(principal_due + interest_due + monthly_premium).quantize(Decimal('0.01')),

                db.session.add(LoanSchedule(
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
                ))

                principal_balance = new_balance

            # ✅ SAVE EVERYTHING
            db.session.commit()

            # ---------------- PDF GENERATION ----------------
            schedules = LoanSchedule.query.filter_by(
                loan_no=loan_no
            ).order_by(LoanSchedule.installment_no).all()

            pdf_buffer = generate_schedule_pdf(new_loan, schedules, member)

            # ---------------- EMAIL ----------------
            try:
                if member.email:
                    send_loan_schedule_email(member, new_loan, pdf_buffer)
            except Exception as mail_error:
                current_app.logger.error(f"Loan email failed: {mail_error}")
                flash("Loan disbursed but email failed.", "warning")

            flash(f"Loan {loan_no} disbursed successfully!", "success")
            return send_file(
                    pdf_buffer,
                    as_attachment=True,
                    download_name=f"{loan_no}_Schedule.pdf",
                    mimetype="application/pdf"
                )

            return redirect(url_for('admin.loans_view'))

        except Exception as e:
            db.session.rollback()
            import traceback; traceback.print_exc()
            flash(f"Disbursement failed: {str(e)}", "danger")
            return render_template('admin/disburse_loan.html', form=form)

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
        required_cols = {'bank_txn_date', 'credit_amount', 'narration', 'member_no'}
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
                    narration=f"Deposit for - {member_no}",
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
@admin_bp.route('/deposit-posting', methods=['GET', 'POST'])
@login_required
def deposit_posting():
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
            flash(f"Member posting of {amount} for {member_no} posted successfully.", "success")
            return redirect(url_for('admin.deposit_posting'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error posting : {str(e)}", "danger")

    return render_template('admin/deposit_posting.html', form=form)
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
@admin_bp.route('/upload_bank_postings', methods=['GET', 'POST'])
@login_required
def upload_bank_postings():
    """
    FINAL SACCO LOGIC:
    - No Cash account
    - Evaluate only overdue schedules (due_date < today)
    - Pay INTEREST → PRINCIPAL → remainder to SAVINGS
    - Post entries:
        DR MEMBER_INTEREST    CR M000GL_LN_INT
        DR MEMBER_LOAN        CR M000GL_LOAN
        DR MEMBER_SAVINGS     CR M000GL_SAVINGS
    - Update sacco_accounts.balance every leg
    - Update Transaction.running_balance every leg
    """
    from sacco_app.forms import UploadMemberSavingsForm
    from decimal import Decimal, InvalidOperation
    from datetime import datetime, date
    import pandas as pd
    import uuid

    form = UploadMemberSavingsForm()

    # --- Helpers -------------------------------------------------------------

    def ensure_savings(member_no):
        acc = SaccoAccount.query.filter_by(member_no=member_no, account_type="SAVINGS").first()
        if not acc:
            acc = SaccoAccount(
                member_no=member_no,
                account_number=f"{member_no}_SAVINGS",
                account_type="SAVINGS",
                balance=Decimal("0.00"),
                limit=Decimal("1000000"),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                created_by=current_user.username
            )
            db.session.add(acc)
            db.session.flush()
        return acc

    def ensure_loan_ledgers(member_no):
        """Create LOAN and INTEREST member ledgers only if an active loan exists."""
        loan_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type="LOAN").first()
        if not loan_acc:
            loan_acc = SaccoAccount(
                member_no=member_no,
                account_number=f"{member_no}_LOAN",
                account_type="LOAN",
                balance=Decimal("0.00"),
                limit=Decimal("1000000"),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                created_by=current_user.username
            )
            db.session.add(loan_acc)
            db.session.flush()

        int_acc = SaccoAccount.query.filter_by(member_no=member_no, account_type="INTEREST").first()
        if not int_acc:
            int_acc = SaccoAccount(
                member_no=member_no,
                account_number=f"{member_no}_INTEREST",
                account_type="INTEREST",
                balance=Decimal("0.00"),
                limit=Decimal("0"),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                created_by=current_user.username
            )
            db.session.add(int_acc)
            db.session.flush()

        return loan_acc, int_acc

    # --- Main processing -----------------------------------------------------

    if form.validate_on_submit():
        file = form.file.data
        try:
            df = pd.read_excel(file)
        except:
            flash("Invalid Excel file.", "danger")
            return redirect(url_for('admin.upload_bank_postings'))

        required = {"member_no", "credit_amount", "narration", "bank_txn_date"}
        if not required.issubset(df.columns):
            flash("Missing required columns.", "danger")
            return redirect(url_for('admin.upload_bank_postings'))

        # GLs (confirmed)
        gl_savings = SaccoAccount.query.filter_by(account_number="M000GL_SAVINGS").first()
        gl_loan = SaccoAccount.query.filter_by(account_number="M000GL_LOAN").first()
        gl_interest = SaccoAccount.query.filter_by(account_number="M000GL_LN_INT").first()

        success = 0
        failed = []

        for idx, row in df.iterrows():
            try:
                # Get row values
                member_no = str(row["member_no"]).strip()
                narration = str(row["narration"] or "")
                try:
                    amount = Decimal(row["credit_amount"] or 0)
                except:
                    raise Exception("Invalid amount")

                if pd.isna(row["bank_txn_date"]):
                    txn_date = datetime.utcnow()
                else:
                    txn_date = pd.to_datetime(row["bank_txn_date"]).to_pydatetime()

                member = Member.query.filter_by(member_no=member_no).first()
                if not member:
                    raise Exception("Member not found")

                remaining = amount
                txn_ref = f"UP{uuid.uuid4().hex[:10].upper()}"

                # Ensure savings ledger exists
                m_savings = ensure_savings(member_no)

                # Check for active loan
                loan = Loan.query.filter_by(member_no=member_no, status="Active").first()

                # ----------------------------------------------------------------------
                # CASE 1: MEMBER HAS NO ACTIVE LOAN → full amount goes to savings
                # ----------------------------------------------------------------------
                if not loan:
                    with db.session.no_autoflush:
                        # Debit member savings
                        m_savings.balance += remaining
                        db.session.add(m_savings)

                        db.session.add(Transaction(
                            txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                            member_no=member_no,
                            account_no=m_savings.account_number,
                            gl_account="SAVINGS",
                            tran_type="LIABILITY",
                            debit_amount=Decimal("0"),
                            credit_amount=remaining,
                            running_balance=m_savings.balance,
                            reference=txn_ref,
                            narration=f"{narration}",
                            bank_txn_date=txn_date,
                            posted_by=current_user.username
                        ))

                        # Credit savings control
                        gl_savings.balance += remaining
                        db.session.add(gl_savings)

                        db.session.add(Transaction(
                            txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                            member_no="M000GL",
                            account_no=gl_savings.account_number,
                            gl_account="SAVINGS_CONTROL",
                            tran_type="LIABILITY",
                            debit_amount=Decimal("0"),
                            credit_amount=remaining,
                            running_balance=gl_savings.balance,
                            reference=txn_ref,
                            narration=f"Savings control- {narration}",
                            bank_txn_date=txn_date,
                            posted_by=current_user.username
                        ))

                    db.session.commit()
                    success += 1
                    continue

                # ----------------------------------------------------------------------
                # CASE 2: MEMBER HAS ACTIVE LOAN → PAY DUE INTEREST, THEN PRINCIPAL
                # ----------------------------------------------------------------------

                # Ensure loan & interest ledgers exist
                m_loan, m_interest = ensure_loan_ledgers(member_no)

                # Fetch only overdue schedules
                schedules = LoanSchedule.query.filter(
                    LoanSchedule.loan_no == loan.loan_no,
                    LoanSchedule.status.in_(["DUE", "PARTIAL"]),
                    LoanSchedule.due_date < date.today()
                ).order_by(LoanSchedule.due_date.asc()).all()

                # If no dues → full amount to savings
                if not schedules:
                    with db.session.no_autoflush:
                        m_savings.balance += remaining
                        db.session.add(m_savings)

                        db.session.add(Transaction(
                            txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                            member_no=member_no,
                            account_no=m_savings.account_number,
                            gl_account="SAVINGS",
                            tran_type="LIABILITY",
                            debit_amount=Decimal("0"),
                            credit_amount=remaining,
                            running_balance=m_savings.balance,
                            reference=txn_ref,
                            narration=f"{narration}",
                            bank_txn_date=txn_date,
                            posted_by=current_user.username
                        ))

                        gl_savings.balance += remaining
                        db.session.add(gl_savings)

                        db.session.add(Transaction(
                            txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                            member_no="M000GL",
                            account_no=gl_savings.account_number,
                            gl_account="SAVINGS_CONTROL",
                            tran_type="LIABILITY",
                            debit_amount=Decimal("0"),
                            credit_amount=remaining,
                            running_balance=gl_savings.balance,
                            reference=txn_ref,
                            narration=f"Savings control credit",
                            bank_txn_date=txn_date,
                            posted_by=current_user.username
                        ))

                    db.session.commit()
                    success += 1
                    continue

                # ----------------------------------------------------------------------
                # Apply each overdue schedule
                # ----------------------------------------------------------------------
                for sched in schedules:
                    if remaining <= 0:
                        break

                    # Compute due interest/principal
                    int_due = (Decimal(sched.interest_due or 0) -
                               Decimal(sched.interest_paid or 0))
                    prin_due = (Decimal(sched.principal_due or 0) -
                                Decimal(sched.principal_paid or 0))

                    # --- 1) PAY INTEREST ---
                    if int_due > 0 and remaining > 0:
                        pay = min(remaining, int_due)
                        sched.interest_paid += pay
                        remaining -= pay

                        with db.session.no_autoflush:
                            # DR MEMBER_INTEREST
                            m_interest.balance -= pay
                            db.session.add(m_interest)
                            db.session.add(Transaction(
                                txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                                member_no=member_no,
                                account_no=m_interest.account_number,
                                gl_account="MEMBER_INTEREST",
                                tran_type="ASSET",
                                debit_amount=pay,
                                credit_amount=Decimal("0"),
                                running_balance=m_interest.balance,
                                reference=txn_ref,
                                narration=f"Interest paid - {narration}",
                                bank_txn_date=txn_date,
                                posted_by=current_user.username
                            ))

                            # CR INTEREST CONTROL
                            gl_interest.balance += pay
                            db.session.add(gl_interest)
                            db.session.add(Transaction(
                                txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                                member_no="M000GL",
                                account_no=gl_interest.account_number,
                                gl_account="LOAN_INTEREST_CONTROL",
                                tran_type="INCOME",
                                debit_amount=Decimal("0"),
                                credit_amount=pay,
                                running_balance=gl_interest.balance,
                                reference=txn_ref,
                                narration=f"Interest control credit",
                                bank_txn_date=txn_date,
                                posted_by=current_user.username
                            ))

                    # --- 2) PAY PRINCIPAL ---
                    if prin_due > 0 and remaining > 0:
                        pay = min(remaining, prin_due)
                        sched.principal_paid += pay
                        remaining -= pay

                        with db.session.no_autoflush:
                            # DR MEMBER_LOAN
                            m_loan.balance -= pay
                            db.session.add(m_loan)
                            db.session.add(Transaction(
                                txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                                member_no=member_no,
                                account_no=m_loan.account_number,
                                gl_account="MEMBER_LOAN",
                                tran_type="ASSET",
                                debit_amount=pay,
                                credit_amount=Decimal("0"),
                                running_balance=m_loan.balance,
                                reference=txn_ref,
                                narration=f"Principal paid - {narration}",
                                bank_txn_date=txn_date,
                                posted_by=current_user.username
                            ))

                            # CR LOAN CONTROL
                            gl_loan.balance -= pay
                            db.session.add(gl_loan)
                            db.session.add(Transaction(
                                txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                                member_no="M000GL",
                                account_no=gl_loan.account_number,
                                gl_account="LOAN_CONTROL",
                                tran_type="ASSET",
                                debit_amount=Decimal("0"),
                                credit_amount=pay,
                                running_balance=gl_loan.balance,
                                reference=txn_ref,
                                narration=f"Loan control credit",
                                bank_txn_date=txn_date,
                                posted_by=current_user.username
                            ))

                    # update schedule status
                    if (sched.interest_paid >= sched.interest_due and
                        sched.principal_paid >= sched.principal_due):
                        sched.status = "PAID"
                    else:
                        sched.status = "PARTIAL"

                # Update loan from member loan ledger
                loan.balance = m_loan.balance
                if loan.balance <= 0:
                    loan.balance = Decimal("0")
                    loan.status = "Cleared"

                # ----------------------------------------------------------------------
                # REMAINDER → SAVINGS
                # ----------------------------------------------------------------------
                if remaining > 0:
                    with db.session.no_autoflush:
                        # DR MEMBER_SAVINGS
                        m_savings.balance += remaining
                        db.session.add(m_savings)
                        db.session.add(Transaction(
                            txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                            member_no=member_no,
                            account_no=m_savings.account_number,
                            gl_account="SAVINGS",
                            tran_type="LIABILITY",
                            debit_amount=Decimal("0"),
                            credit_amount=remaining,
                            running_balance=m_savings.balance,
                            reference=txn_ref,
                            narration=f"Remainder to savings - {narration}",
                            bank_txn_date=txn_date,
                            posted_by=current_user.username
                        ))

                        # CR SAVINGS CONTROL
                        gl_savings.balance += remaining
                        db.session.add(gl_savings)
                        db.session.add(Transaction(
                            txn_no=f"TXN{uuid.uuid4().hex[:12].upper()}",
                            member_no="M000GL",
                            account_no=gl_savings.account_number,
                            gl_account="SAVINGS_CONTROL",
                            tran_type="LIABILITY",
                            debit_amount=Decimal("0"),
                            credit_amount=remaining,
                            running_balance=gl_savings.balance,
                            reference=txn_ref,
                            narration=f"Savings control credit",
                            bank_txn_date=txn_date,
                            posted_by=current_user.username
                        ))

                # FINAL COMMIT
                db.session.commit()
                success += 1

            except Exception as e:
                db.session.rollback()
                failed.append({
                    "row": idx + 1,
                    "member_no": row.get("member_no"),
                    "error": str(e)
                })

        return render_template(
            "admin/upload_results.html",
            failed_rows=failed,
            success_count=success
        )

    return render_template("admin/upload_bank_postings.html", form=form)
##PAR dashboard
def get_par_metrics():
    sql = """
    WITH arrears_loans AS (
        SELECT DISTINCT l.loan_no, l.balance
        FROM loans l
        JOIN loan_schedules ls
            ON ls.loan_no = l.loan_no
        WHERE
            l.status IN ('Active')
            AND ls.due_date < CURRENT_DATE
            AND (
                COALESCE(ls.principal_paid,0)
              + COALESCE(ls.interest_paid,0)
            ) < (
                COALESCE(ls.principal_due,0)
              + COALESCE(ls.interest_due,0)
            )
    )
    SELECT
        (SELECT SUM(balance)
         FROM loans
         WHERE status IN ('Active')
        ) AS total_portfolio,

        (SELECT SUM(balance)
         FROM arrears_loans
        ) AS portfolio_at_risk;
    """
    r = db.session.execute(text(sql)).fetchone()

    total = r.total_portfolio or 0
    risk = r.portfolio_at_risk or 0
    par = round((risk / total * 100), 2) if total else 0

    return total, risk, par   

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
    total_portfolio, portfolio_at_risk, par_percentage = get_par_metrics()
    # ----------------------------
    # 1. TOTAL MEMBERS
    # ----------------------------
    total_members = Member.query.filter(Member.member_no != 'M000GL').count()
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
        total_portfolio=total_portfolio,
        portfolio_at_risk=portfolio_at_risk,
        par_percentage=par_percentage
    )

##from sqlalchemy import text


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
        interest_control_acc = SaccoAccount.query.filter_by(account_number='M000GL_LN_INT').first()
        interest_income_acc = SaccoAccount.query.filter_by(member_no=member_no,account_type='INTEREST').first()

        savings_control_acc = SaccoAccount.query.filter_by(account_number='M000GL_SAVINGS').first()

        if not all([loan_principal_acc, interest_income_acc, savings_control_acc, loan_control_acc]):
            flash("Required GL accounts missing (Loan/Savings/Control).", "danger")
            return redirect(url_for('admin.repay_loan_from_savings'))

        due_schedule = LoanSchedule.query.filter(
            LoanSchedule.loan_no == loan.loan_no,
            LoanSchedule.status != 'PAID'
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
                gl_account='MEMBER_INTEREST',
                tran_type='INCOME',
                debit_amount=pay_interest,
                credit_amount=Decimal('0'),
                reference=txn_ref,
                narration=f"Interest Paid - {member_no}",
                bank_txn_date=txn_date,
                posted_by=current_user.username,
                running_balance=interest_income_acc.balance
            )
            transactions.append(txn_int)

            interest_control_acc.balance += pay_interest

            txn_int = Transaction(
                txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
                member_no="M000GL",
                account_no=interest_control_acc.account_number,
                gl_account='LOAN_INTEREST_CONTROL',
                tran_type='INCOME',
                debit_amount=Decimal('0'),
                credit_amount=pay_interest,
                reference=txn_ref,
                narration=f"Interest Paid - {member_no}",
                bank_txn_date=txn_date,
                posted_by=current_user.username,
                running_balance=interest_control_acc.balance
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
                narration=f"Loan principal repayment from savings- {member_no}",
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
                gl_account='MEMBER_LOAN',
                tran_type='ASSET',
                debit_amount=pay_principal,
                credit_amount=Decimal('0'),
                reference=txn_ref,
                narration=f"Principal paid for {member_no}",
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
                acc.balance -= debit
            if credit > 0:
                acc.balance += credit

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
                narration=f"Reversal-{reason}",
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

@admin_bp.route('/audit-logs')
@login_required
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(500).all()
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


##loan statement view_member
@admin_bp.route('/reports/loan-statement2', methods=['GET'])
@login_required
def loan_statement_form_view():
    """Simple form to choose member and date range for loan statement"""
    return render_template('admin/loan_statement_form_view.html')

@admin_bp.route('/reports/loan-statement2', methods=['GET', 'POST'])
@login_required
def loan_statement_view2():
    statement = None
    member_no = None

    if request.method == 'POST':
        member_no = request.form.get('member_no')

        sql = text("""
                            SELECT
                    t.account_no,
                    t.bank_txn_date,
                    t.narration,

                    -- interest paid (display only)
                    CASE 
                        WHEN t.gl_account = 'MEMBER_INTEREST'
                        THEN t.debit_amount ELSE 0
                    END AS interest_paid,

                    -- principal paid (EXCLUDE disbursement)
                    CASE 
                        WHEN t.gl_account = 'MEMBER_LOAN'
                         AND COALESCE(t.credit_amount, 0) = 0   -- repayment only
                        THEN t.debit_amount ELSE 0
                    END AS principal_paid,

                    -- loan balance (already maintained by system)
                    CASE
                        WHEN t.gl_account = 'MEMBER_LOAN'
                        THEN t.running_balance
                        ELSE NULL
                    END AS loan_balance

                FROM transactions t
                WHERE t.member_no  =:member_no
                  AND t.gl_account IN ('MEMBER_LOAN', 'MEMBER_INTEREST')
                ORDER BY created_at, t.bank_txn_date, t.id asc;
        """)

        statement = db.session.execute(
            sql, {"member_no": member_no}
        ).fetchall()

    return render_template(
        'admin/loan_statement_form_view.html',
        statement=statement,
        member_no=member_no
    )


####### view loan schedules

@admin_bp.route('/loans/member-schedules')
@login_required
def view_member_loan_schedules():
    return render_template('admin/view_member_loan_schedules.html')
    
@admin_bp.route('/loans/member-schedules/<member_no>')
@login_required
def fetch_member_loan_schedules(member_no):
    from sacco_app.models import Loan, LoanSchedule

    loans = Loan.query.filter_by(member_no=member_no).all()
    if not loans:
        return jsonify({"error": "No loans found for this member"})

    rows = []
    for loan in loans:
        schedules = LoanSchedule.query.filter_by(
            loan_no=loan.loan_no
        ).order_by(LoanSchedule.installment_no).all()

        for s in schedules:
            rows.append({
                "loan_no": loan.loan_no,
                "installment_no": s.installment_no,
                "due_date": s.due_date.strftime('%Y-%m-%d'),
                "principal_due": float(s.principal_due),
                "principal_paid": float(s.principal_paid),
                "interest_due": float(s.interest_due),
                "interest_paid": float(s.interest_paid),
                "status": s.status
            })

    return jsonify({"schedules": rows})

### upload PDF statements

@admin_bp.route('/bank-pdf', methods=['GET'])
@login_required
def bank_pdf_form():
    return render_template('admin/bank_pdf_upload.html')


@admin_bp.route('/bank-pdf/upload', methods=['POST'])
@login_required
def bank_pdf_upload():

    if 'pdf_file' not in request.files:
        flash("No file selected", "danger")
        return redirect(url_for('admin.bank_pdf_form'))

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        flash("No file selected", "danger")
        return redirect(url_for('admin.bank_pdf_form'))

    if not pdf_file.filename.lower().endswith('.pdf'):
        flash("Only PDF files are allowed", "danger")
        return redirect(url_for('admin.bank_pdf_form'))

    original_name = secure_filename(pdf_file.filename)
    unique_id = uuid.uuid4().hex

    pdf_filename = f"{unique_id}_{original_name}"
    pdf_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        pdf_filename
    )

    pdf_root, _ = os.path.splitext(pdf_filename)
    excel_filename = pdf_root + ".xlsx"
    excel_path = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        excel_filename
    )

    print("PDF PATH  :", pdf_path)
    print("EXCEL PATH:", excel_path)

    pdf_file.save(pdf_path)

    # ---------------- SAFE CONVERSION ----------------
    try:
        convert_bank_pdf_to_excel(pdf_path, excel_path)
    except Exception as e:
        current_app.logger.error(e)
        flash(f"PDF conversion failed: {e}", "danger")
        return redirect(url_for('admin.bank_pdf_form'))

    # ---------------- ENSURE FILE EXISTS ----------------
    if not os.path.exists(excel_path):
        flash("Excel file was not generated.", "danger")
        return redirect(url_for('admin.bank_pdf_form'))

    flash("PDF converted successfully", "success")

    return send_file(
        excel_path,
        as_attachment=True,
        download_name=excel_filename
    )
###FIND MEMBER IN THE MEMBER TABLE
from rapidfuzz import process, fuzz

def find_member_by_name(session, name):
    """
    Attempts to find a member using name.
    Returns (member_no, confidence) or (None, 0)
    """

    if not name:
        return None, 0

    name = name.upper().strip()

    members = session.execute(
        "SELECT member_no, full_name FROM members"
    ).fetchall()

    if not members:
        return None, 0

    # Exact match first
    for m in members:
        if m.name.upper() == name:
            return m.member_no, 100

    # Fuzzy match
    choices = {m.name.upper(): m.member_no for m in members}

    match, score, _ = process.extractOne(
        name,
        choices.keys(),
        scorer=fuzz.token_sort_ratio
    )

    if score >= 85:  # SAFE threshold
        return choices[match], score

    return None, score

####EXTRACT NAME FROM PDF
def extract_name(tx_details):
    """
    Extracts name from transaction details line.
    Example: 00222~ALVIN MAINA
    """

    if "~" in tx_details:
        parts = tx_details.split("~")
        if len(parts) >= 2:
            return parts[-1].strip().upper()

    return ""
####EXTRACT NAME FROM PDF_test
import re
import pdfplumber
import pandas as pd
from datetime import datetime
from collections import defaultdict


# ---------------------------------------------------
# 1. IDENTIFY REAL TRANSACTION DETAILS
# ---------------------------------------------------
def is_transaction_line(text: str) -> bool:
    if not text:
        return False

    t = text.upper()

    if any(k in t for k in ["MPESA", "PESALINK", "POS", "CHQ", "CHEQUE", "01134211013100"]):
        return True

    # phone / reference numbers
    if re.search(r"\d{10,}", t):
        return True

    return False


# ---------------------------------------------------
# 2. EXTRACT CLEAN TX DETAILS FROM SAME ROW
# ---------------------------------------------------
def extract_clean_tx_details_from_row(row_words):
    """
    Extracts ONLY the transaction-details column.
    Stops when numeric money columns start.
    """

    parts = []

    for w in row_words:
        text = w["text"]

        # Stop once money columns begin
        if re.fullmatch(r"[\d,]+\.\d{2}", text):
            break

        # Skip standalone dates
        if re.match(r"\d{2}/\d{2}/\d{4}", text):
            continue

        parts.append(text)

    line = " ".join(parts).strip()

    if is_transaction_line(line):
        return line

    return ""


# ---------------------------------------------------
# 3. NORMALIZE MEMBER NUMBER (SAFE)
# ---------------------------------------------------
def normalize_member_no(tx_details: str) -> str:
    if not tx_details:
        return ""

    text = tx_details.upper().replace("O", "0")

    # STRICT: must follow # or ~
    match = re.search(r"[#~](M?\d{2,5})\b", text)
    if not match:
        return ""

    digits = re.findall(r"\d", match.group(1))
    if not digits:
        return ""

    return f"M{''.join(digits).zfill(4)}"


# ---------------------------------------------------
# 4. MAIN CONVERTER (CREDIT-ONLY)
# ---------------------------------------------------
def convert_bank_pdf_to_excel(pdf_path, excel_path):

    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            words = page.extract_words(use_text_flow=False)
            if not words:
                continue

            # -----------------------------------
            # GROUP WORDS BY VISUAL ROW (Y AXIS)
            # -----------------------------------
            rows_by_y = defaultdict(list)
            for w in words:
                rows_by_y[round(w["top"], 1)].append(w)

            sorted_rows = sorted(rows_by_y.items(), key=lambda x: x[0])

            # -----------------------------------
            # PROCESS EACH ROW
            # -----------------------------------
            for y, row_words in sorted_rows:

                # Sort left → right (CRITICAL)
                row_words = sorted(row_words, key=lambda w: w["x0"])
                texts = [w["text"] for w in row_words]
                row_text = " ".join(texts).upper()

                # Must explicitly be a CREDIT row
                if "CR" not in row_text:
                    continue

                # Reject explicit debit rows
                if any(x in row_text for x in [" DR", "DB", "DEBIT"]):
                    continue

                # ---- DATE ----
                date_match = next(
                    (t for t in texts if re.match(r"\d{2}/\d{2}/\d{4}", t)),
                    None
                )
                if not date_match:
                    continue

                tx_date = datetime.strptime(date_match, "%d/%m/%Y")

                # -----------------------------------
                # CREDIT-ONLY AMOUNT EXTRACTION
                # -----------------------------------
                numeric_values = []
                for t in texts:
                    if re.fullmatch(r"[\d,]+\.\d{2}", t):
                        try:
                            numeric_values.append(float(t.replace(",", "")))
                        except ValueError:
                            pass

                # Expect Debit | Credit | Balance
                if len(numeric_values) < 2:
                    continue

                debit = numeric_values[0]
                credit = numeric_values[1]

                # Reject debits
                if debit > 0:
                    continue

                # Reject zero / invalid credits
                if credit <= 0:
                    continue

                # -----------------------------------
                # TRANSACTION DETAILS
                # -----------------------------------

                # 1️⃣ SAME ROW (preferred)
                tx_details = extract_clean_tx_details_from_row(row_words)

                # 2️⃣ FALLBACK: LOOK ABOVE
                if not tx_details:
                    tx_lines = []

                    for prev_y, prev_words in reversed(sorted_rows):
                        if prev_y >= y:
                            continue

                        prev_words = sorted(prev_words, key=lambda w: w["x0"])
                        prev_text = " ".join(w["text"] for w in prev_words).strip()

                        # Stop at transaction boundary
                        if (
                            "CR" in prev_text.upper() or
                            re.search(r"\d{2}/\d{2}/\d{4}", prev_text)
                        ):
                            break

                        if is_transaction_line(prev_text):
                            tx_lines.insert(0, prev_text)

                    tx_details = " ".join(tx_lines).strip()

                member_no = normalize_member_no(tx_details)
                narration = tx_details[:35] if tx_details else ""

                rows.append({
                    "bank_txn_date": tx_date,
                    "credit_amount": credit,
                    "narration": narration,
                    "member_no": member_no,
                    "transaction_details": tx_details
                })

    if not rows:
        raise ValueError("No valid credit transactions found")

    # -----------------------------------
    # EXPORT TO EXCEL
    # -----------------------------------
    df = pd.DataFrame(rows)
    df["credit_amount"] = df["credit_amount"].astype(float)

    df.to_excel(excel_path, index=False)

###LIST LOANS PENDING
@admin_bp.route('/loans')
@login_required
def loans_view():
    sql = """
    SELECT
        l.member_no,
        l.loan_amount AS principal_amount,
        (ls.principal_due + ls.interest_due) AS monthly_total_repayment,
        l.balance,
        l.disbursed_date,
        l.loan_period,
        l.status
    FROM loans l
    LEFT JOIN loan_schedules ls
        ON ls.loan_no = l.loan_no
       AND ls.status = 'DUE'
       AND ls.installment_no = (
            SELECT MIN(installment_no)
            FROM loan_schedules
            WHERE loan_no = l.loan_no
              AND status = 'DUE'
       )
    ORDER BY l.disbursed_date DESC
    """
    result = db.session.execute(text(sql)).fetchall()
    return render_template('admin/loans.html', loans=result)

#### LOAN ARREARS
@admin_bp.route('/loans/arrears')
@login_required
def loan_arrears_view():
    sql = """
    SELECT
        a.member_number,
        a.loan_number,
        a.monthly_repayment,
        a.total_due_amount,
        a.no_of_months_not_paid,
        t.last_date_paid,
        a.loan_balance,
        a.principle_amount
    FROM (
        SELECT
            l.loan_no AS loan_number,
            l.member_no AS member_number,

            -- 🔹 Monthly repayment = oldest unpaid installment
            MIN(
                COALESCE(ls.principal_due,0) + COALESCE(ls.interest_due,0)
            ) AS monthly_repayment,

            -- 🔹 Total arrears (all overdue installments)
            SUM(
                (COALESCE(ls.principal_due,0) + COALESCE(ls.interest_due,0))
              - (COALESCE(ls.principal_paid,0) + COALESCE(ls.interest_paid,0))
            ) AS total_due_amount,

            COUNT(*) AS no_of_months_not_paid,

            l.balance AS loan_balance,
            l.loan_amount AS principle_amount

        FROM loans l
        JOIN loan_schedules ls
            ON ls.loan_no = l.loan_no

        WHERE
            l.status IN ('Active')
            AND ls.due_date < CURRENT_DATE
            AND (
                COALESCE(ls.principal_paid,0)
              + COALESCE(ls.interest_paid,0)
            ) < (
                COALESCE(ls.principal_due,0)
              + COALESCE(ls.interest_due,0)
            )

        GROUP BY
            l.loan_no,
            l.member_no,
            l.balance,
            l.loan_amount
    ) a

    LEFT JOIN (
        SELECT
            member_no,
            MAX(bank_txn_date) AS last_date_paid
        FROM transactions
        WHERE tran_type IN ('ASSET')
        GROUP BY member_no
    ) t ON t.member_no = a.member_number

    ORDER BY
        a.no_of_months_not_paid DESC,
        a.total_due_amount DESC;
    """
    arrears = db.session.execute(text(sql)).fetchall()
    return render_template('admin/loan_arrears.html', arrears=arrears)

###AUTO LOAD LOAN SCEDULES
from datetime import date

@admin_bp.route('/loans/<loan_no>/schedules')
@login_required
def view_loan_schedules_auto(loan_no):
    loan = Loan.query.filter_by(loan_no=loan_no).first_or_404()

    schedules = LoanSchedule.query.filter_by(
        loan_no=loan_no
    ).order_by(LoanSchedule.installment_no).all()

    return render_template(
        'admin/member_loan_schedules.html',
        loan=loan,
        schedules=schedules,
        today=date.today()   

    )

###export loan schedules to PDF
@admin_bp.route('/loans/<loan_no>/schedules/excel')
@login_required
def export_loan_schedules_excel(loan_no):
    import pandas as pd
    from flask import send_file
    from io import BytesIO

    schedules = LoanSchedule.query.filter_by(
        loan_no=loan_no
    ).order_by(LoanSchedule.installment_no).all()

    data = [{
        'Installment': s.installment_no,
        'Due Date': s.due_date,
        'Principal Due': s.principal_due,
        'Interest Due': s.interest_due,
        'Principal Paid': s.principal_paid or 0,
        'Interest Paid': s.interest_paid or 0,
        'Status': s.status
    } for s in schedules]

    df = pd.DataFrame(data)

    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='Loan Schedules')
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=f'loan_schedules_{loan_no}.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
@admin_bp.route('/loans/<loan_no>/schedules/pdf')
@login_required
def export_loan_schedules_pdf(loan_no):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from io import BytesIO

    loan = Loan.query.filter_by(loan_no=loan_no).first_or_404()
    schedules = LoanSchedule.query.filter_by(
        loan_no=loan_no
    ).order_by(LoanSchedule.installment_no).all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(
        f"<b>Loan Schedules</b><br/>Member: {loan.member_no} | Loan No: {loan.loan_no}",
        styles['Normal']
    ))

    table_data = [[
        'Inst', 'Due Date', 'Principal Due', 'Interest Due',
        'Principal Paid', 'Interest Paid', 'Status'
    ]]

    for s in schedules:
        table_data.append([
            s.installment_no,
            s.due_date.strftime('%Y-%m-%d'),
            f"{s.principal_due:,.2f}",
            f"{s.interest_due:,.2f}",
            f"{(s.principal_paid or 0):,.2f}",
            f"{(s.interest_paid or 0):,.2f}",
            s.status
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (2,1), (-2,-1), 'RIGHT'),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'loan_schedules_{loan_no}.pdf',
        mimetype='application/pdf'
    )


###RECALCULATE INTEREST ON LOANS DUE
@admin_bp.route('/loans/<loan_no>/recalculate-interest')
@login_required
def recalculate_loan_interest(loan_no):

    loan = Loan.query.filter_by(loan_no=loan_no).first_or_404()

    schedules = LoanSchedule.query.filter(
        LoanSchedule.loan_no == loan_no
    ).order_by(LoanSchedule.installment_no).all()

    if not schedules:
        flash('No schedules found.', 'info')
        return redirect(request.referrer)

    today = date.today()
    monthly_rate = Decimal(loan.interest_rate) / Decimal(100) / Decimal(12)

    # Start with actual outstanding balance
    outstanding_balance = loan.balance

    for s in schedules:

        # If schedule already fully paid → skip
        if s.principal_paid >= s.principal_due:
            continue

        # Past due month
        if s.due_date < today:

            # Interest on full outstanding (no reduction)
            interest = outstanding_balance * monthly_rate
            s.interest_due = round(interest, 2)

            # DO NOT reduce outstanding balance
            # because principal not paid

        else:
            # Future schedule → assume reducing balance
            interest = outstanding_balance * monthly_rate
            s.interest_due = round(interest, 2)

            # Reduce only by scheduled principal
            outstanding_balance -= s.principal_due

    db.session.commit()

    flash('Loan interest recalculated successfully.', 'success')
    return redirect(request.referrer)
##ARREARS AS PDF 

@admin_bp.route('/loans/arrears/pdf')
@login_required
def export_loan_arrears_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from io import BytesIO
    from datetime import date

    sql = """
    SELECT
        a.member_number,
        a.loan_no,
        a.monthly_repayment,
        a.no_of_months_not_paid,
        a.total_due_amount,
        a.loan_balance,
        a.principle_amount,
        t.last_date_paid
    FROM (
        SELECT
            l.loan_no,
            l.member_no AS member_number,

            MIN(
                COALESCE(ls.principal_due,0) + COALESCE(ls.interest_due,0)
            ) AS monthly_repayment,

            SUM(
                (COALESCE(ls.principal_due,0) + COALESCE(ls.interest_due,0))
              - (COALESCE(ls.principal_paid,0) + COALESCE(ls.interest_paid,0))
            ) AS total_due_amount,

            COUNT(*) AS no_of_months_not_paid,

            l.balance AS loan_balance,
            l.loan_amount AS principle_amount

        FROM loans l
        JOIN loan_schedules ls
            ON ls.loan_no = l.loan_no
        WHERE
            l.status IN ('Active')
            AND ls.due_date < CURRENT_DATE
            AND (
                COALESCE(ls.principal_paid,0)
              + COALESCE(ls.interest_paid,0)
            ) < (
                COALESCE(ls.principal_due,0)
              + COALESCE(ls.interest_due,0)
            )
        GROUP BY
            l.loan_no,
            l.member_no,
            l.balance,
            l.loan_amount
    ) a
    LEFT JOIN (
        SELECT
            member_no,
            MAX(bank_txn_date) AS last_date_paid
        FROM transactions
        WHERE tran_type IN ('ASSET')
        GROUP BY member_no
    ) t ON t.member_no = a.member_number
    ORDER BY
        a.no_of_months_not_paid DESC,
        a.total_due_amount DESC;
    """

    rows = db.session.execute(text(sql)).fetchall()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(
        "<b>Loan Arrears Summary Report</b>", styles['Title']
    ))
    elements.append(Paragraph(
        f"Report Date: {date.today().strftime('%Y-%m-%d')}", styles['Normal']
    ))
    elements.append(Spacer(1, 12))

    table_data = [[
        'Member No', 'Loan No', 'Monthly Repayment',
        'Months in Arrears', 'Total Arrears',
        'Loan Balance', 'Principal', 'Last Paid'
    ]]

    total_arrears = 0

    for r in rows:
        total_arrears += r.total_due_amount or 0
        table_data.append([
            r.member_number,
            r.loan_no,
            f"{r.monthly_repayment:,.2f}",
            r.no_of_months_not_paid,
            f"{r.total_due_amount:,.2f}",
            f"{r.loan_balance:,.2f}",
            f"{r.principle_amount:,.2f}",
            r.last_date_paid.strftime('%Y-%m-%d') if r.last_date_paid else 'Never'
        ])

    table_data.append([
        '', '', '', 'TOTAL',
        f"{total_arrears:,.2f}", '', '', ''
    ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('BACKGROUND', (0,-1), (-1,-1), colors.whitesmoke),
        ('ALIGN', (2,1), (-2,-2), 'RIGHT'),
        ('TEXTCOLOR', (4,1), (4,-2), colors.red),
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONT', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='loan_arrears_summary.pdf',
        mimetype='application/pdf'
    )


###Calculate %PAR
@admin_bp.route('/loans/par')
@login_required
def loan_par_view():
    sql = """
    WITH arrears_loans AS (
        SELECT DISTINCT l.loan_no, l.balance
        FROM loans l
        JOIN loan_schedules ls
            ON ls.loan_no = l.loan_no
        WHERE
            l.status IN ('Active')
            AND ls.due_date < CURRENT_DATE
            AND (
                COALESCE(ls.principal_paid,0)
              + COALESCE(ls.interest_paid,0)
            ) < (
                COALESCE(ls.principal_due,0)
              + COALESCE(ls.interest_due,0)
            )
    )
    SELECT
        (SELECT SUM(balance)
         FROM loans
         WHERE status IN ('Active')
        ) AS total_portfolio,

        (SELECT SUM(balance)
         FROM arrears_loans
        ) AS portfolio_at_risk;
    """

    result = db.session.execute(text(sql)).fetchone()

    total = result.total_portfolio or 0
    risk = result.portfolio_at_risk or 0
    par = round((risk / total * 100), 2) if total else 0

    return render_template(
        'admin/loan_par.html',
        total_portfolio=total,
        portfolio_at_risk=risk,
        par_percentage=par
    )
@admin_bp.route('/members/beneficiaries', methods=['POST'])
@login_required
def save_beneficiaries():
    member_no = request.form.get('member_no')
    if not member_no:
        flash('Member not specified', 'danger')
        return redirect(request.referrer)

    names = request.form.getlist('ben_full_name[]')
    relations = request.form.getlist('ben_relationship[]')
    contacts = request.form.getlist('ben_contact[]')
    percentages = request.form.getlist('ben_percentage[]')

    # ---------- BASIC VALIDATION ----------
    if not names:
        flash('Please add at least one beneficiary', 'danger')
        return redirect(request.referrer)

    if not (len(names) == len(relations) == len(contacts) == len(percentages)):
        flash('Beneficiary rows are inconsistent. Please review.', 'danger')
        return redirect(request.referrer)

    # ---------- FIELD-LEVEL VALIDATION ----------
    total_percentage = 0
    beneficiaries_data = []

    for i in range(len(names)):
        name = names[i].strip()
        relationship = relations[i].strip()
        contact = contacts[i].strip()
        percentage = percentages[i]

        if not name or not relationship or not contact or not percentage:
            flash('All beneficiary fields are required', 'danger')
            return redirect(request.referrer)

        try:
            percentage = float(percentage)
        except ValueError:
            flash('Invalid percentage value', 'danger')
            return redirect(request.referrer)

        if percentage <= 0:
            flash('Beneficiary percentage must be greater than zero', 'danger')
            return redirect(request.referrer)

        total_percentage += percentage

        beneficiaries_data.append({
            "full_name": name,
            "relationship": relationship,
            "contact": contact,
            "percentage": percentage
        })

    # ---------- BUSINESS RULE ----------
    if round(total_percentage, 2) != 100.00:
        flash('Total beneficiary percentage must be exactly 100%', 'danger')
        return redirect(request.referrer)

    # ---------- SAVE ----------
    Beneficiary.query.filter_by(member_no=member_no).delete()

    for b in beneficiaries_data:
        ben = Beneficiary(
            member_no=member_no,
            full_name=b["full_name"],
            relationship=b["relationship"],
            contact=b["contact"],
            percentage=b["percentage"]
        )
        db.session.add(ben)

    # ---------- AUDIT ----------
    log_activity(
        action="Updated beneficiaries",
        entity_type="BENEFICIARY",
        entity_id=member_no,
        event_type="UPDATE",
        details=f"{len(beneficiaries_data)} beneficiaries saved",
        after_data=beneficiaries_data
    )

    db.session.commit()
    flash('Beneficiaries updated successfully', 'success')
    return redirect(request.referrer)



## ADD NEXT OF KINS

@admin_bp.route('/members/next-of-kin', methods=['POST'])
@login_required
def save_next_of_kin():
    member_no = request.form.get('member_no')
    if not member_no:
        flash('Member not specified', 'danger')
        return redirect(request.referrer)

    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        flash('Invalid member selected', 'danger')
        return redirect(request.referrer)

    # ✅ MATCH FORM FIELD NAMES
    full_name = request.form.get('full_name')
    if not full_name or not full_name.strip():
        flash('Next of kin full name is required', 'danger')
        return redirect(request.referrer)

    relationship = request.form.get('relationship')
    phone = request.form.get('phone')
    id_number = request.form.get('id_number')

    nok = NextOfKin.query.filter_by(member_no=member_no).first()
    if not nok:
        nok = NextOfKin(member_no=member_no)
        db.session.add(nok)

    nok.full_name = full_name.strip()
    nok.relationship = relationship.strip() if relationship else None
    nok.phone = phone.strip() if phone else None
    nok.id_number = id_number.strip() if id_number else None

    log_activity(
        action="Saved next of kin",
        entity_type="NEXT_OF_KIN",
        entity_id=member_no,
        event_type="UPDATE",
        details=f"NOK: {nok.full_name}"
    )

    db.session.commit()
    flash('Next of kin saved successfully', 'success')
    return redirect(request.referrer)


##member update

@admin_bp.route('/members/update', methods=['POST'])
@login_required
def update_member():
    print("LOG_ACTIVITY FROM:", log_activity.__module__)
    print("LOG_ACTIVITY SIG:", __import__("inspect").signature(log_activity))

    member_no = request.form.get('member_no')
    member = Member.query.filter_by(member_no=member_no).first_or_404()

    before = {
        "name": member.name,
        "phone": member.phone,
        "email": member.email,
        "id_no": member.id_no
    }

    member.name = request.form.get('name')
    member.phone = request.form.get('phone')
    member.email = request.form.get('email')
    member.id_no = request.form.get('id_no')
    member.congregation = request.form.get('congregation')
    member.gender = request.form.get('gender')

    after = {
        "name": member.name,
        "phone": member.phone,
        "email": member.email,
        "id_no": member.id_no
    }

    log_activity(
        action="Updated member profile",
        entity_type="MEMBER",
        entity_id=member.member_no,
        event_type="UPDATE",
        before_data=before,
        after_data=after
    )

    db.session.commit()
    flash("Member updated successfully", "success")
    return redirect(request.referrer)

@admin_bp.route('/members')
@login_required
def members_list():
    members = Member.query.order_by(Member.member_no).all()

    return render_template(
        'admin/members_list.html',
        members=members
    )


@admin_bp.route('/view-member', methods=['GET', 'POST'])
@login_required
def view_member_lookup():
    member = None
    next_of_kin = None
    beneficiaries = []

    if request.method == 'POST':
        member_no = request.form.get('member_no')

        member = Member.query.filter_by(member_no=member_no).first()

        if member:
            next_of_kin = NextOfKin.query.filter_by(member_no=member_no).first()
            beneficiaries = Beneficiary.query.filter_by(member_no=member_no).all()
        else:
            flash('Member not found', 'danger')

    return render_template(
        'admin/view_member_lookup.html',
        member=member,
        next_of_kin=next_of_kin,
        beneficiaries=beneficiaries
    )


@admin_bp.route('/users/<int:user_id>/unlock', methods=['POST'])
@login_required
def unlock_user(user_id):
    # 🔐 Ensure only admins can unlock
    if current_user.role != 'admin':
        flash("Unauthorized action.", "danger")
        return redirect(request.referrer)

    user = User.query.get_or_404(user_id)

    # Reset lockout fields
    user.failed_login_attempts = 0
    user.account_locked_until = None
    db.session.commit()

    # Audit log
    log_activity(
        action="Admin unlocked user account",
        entity_type="USER",
        entity_id=user.id,
        event_type="ACCOUNT_UNLOCKED",
        details=f"User {user.username} unlocked by admin {current_user.username}",
        auto_commit=True
    )

    flash(f"User {user.username} has been unlocked.", "success")
    return redirect(request.referrer)
    
### chart of accounts reports

from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from flask import render_template
from sacco_app.extensions import db
from sacco_app.models.transactions import Transaction
from sacco_app.models.gl_opening_balance import GLOpeningBalance
from flask_login import login_required


def coa_data(from_date, to_date):
    rows = (
        db.session.query(
            Transaction.gl_account,
            func.coalesce(func.sum(Transaction.debit_amount), 0).label("debit"),
            func.coalesce(func.sum(Transaction.credit_amount), 0).label("credit")
        )
        .filter(Transaction.created_at.between(from_date, to_date))
        .group_by(Transaction.gl_account)
        .all()
    )

    data = []

    for r in rows:
        opening = (
            db.session.query(GLOpeningBalance.opening_balance)
            .filter(
                GLOpeningBalance.gl_account == r.gl_account,
                GLOpeningBalance.year == from_date.year
            )
            .scalar()
        ) or 0

        balance = opening + (r.debit - r.credit)

        data.append({
            "gl_account": r.gl_account,
            "opening": opening,
            "debit": r.debit,
            "credit": r.credit,
            "balance": balance
        })

    return data


from datetime import date,time
@admin_bp.route('/coa-balances')
@login_required
def coa_balances():
        # ✅ ALWAYS define selected_year
    selected_year = int(request.args.get('year', date.today().year))

    jan_1 = date(selected_year, 1, 1)

    # If viewing current year, stop at today; otherwise Dec 31
    if selected_year == date.today().year:
        end_date = date.today()
    else:
        end_date = date(selected_year, 12, 31)

    month_start = date(selected_year, end_date.month, 1)
    today = date.today()

    # -------- DATE RANGES --------
    jan_1 = date(today.year, 1, 1)
    month_start = date(today.year, today.month, 1)

    # -------- MAIN DATA --------
    ytd = coa_data(jan_1, today)
    month = coa_data(month_start, today)
    start_today = datetime.combine(date.today(), time.min)
    end_today = datetime.combine(date.today(), time.max)

    today_data = coa_data(start_today, end_today)


    # -------- MONTH vs LAST MONTH --------
    last_month_start = month_start - relativedelta(months=1)
    last_month_end = month_start - relativedelta(days=1)

    current_month = {
        r["gl_account"]: r["debit"] - r["credit"]
        for r in coa_data(month_start, today)
    }

    last_month = {
        r["gl_account"]: r["debit"] - r["credit"]
        for r in coa_data(last_month_start, last_month_end)
    }

    comparison = []
    for gl, current in current_month.items():
        prev = last_month.get(gl, 0)
        comparison.append({
            "gl_account": gl,
            "change": current - prev
        })

    return render_template(
        "admin/coa_balances.html",
        ytd=ytd,
        month=month,
        today=today_data,
        comparison={c["gl_account"]: c["change"] for c in comparison},
        selected_year=selected_year
    )


##coa REPORT TOEXCELL
from datetime import date,time
from sqlalchemy import func, case
from openpyxl import Workbook
from flask import send_file
import io

@admin_bp.route('/coa/export/<period>')
@login_required
def export_coa(period):
    today = date.today()

    if period == "ytd":
        from_date = date(today.year, 1, 1)
    elif period == "month":
        from_date = date(today.year, today.month, 1)
    elif period == "today":
        from_date = today
    else:
        flash("Invalid export period", "danger")
        return redirect(request.referrer)

    rows = (
        db.session.query(
            Transaction.gl_account,
            func.sum(
                case((Transaction.debit_amount > 0, Transaction.debit_amount), else_=0)
            ).label("debit"),
            func.sum(
                case((Transaction.credit_amount > 0, Transaction.credit_amount), else_=0)
            ).label("credit"),
            (
                func.sum(
                    case((Transaction.debit_amount > 0, Transaction.debit_amount), else_=0)
                ) -
                func.sum(
                    case((Transaction.credit_amount > 0, Transaction.credit_amount), else_=0)
                )
            ).label("balance")
        )
        .filter(Transaction.created_at.between(from_date, today))
        .group_by(Transaction.gl_account)
        .order_by(Transaction.gl_account)
        .all()
    )

    # ---------- Excel ----------
    wb = Workbook()
    ws = wb.active
    ws.title = "COA Balances"

    ws.append(["GL Account", "Debit", "Credit", "Balance"])

    for r in rows:
        ws.append([
            r.gl_account,
            float(r.debit or 0),
            float(r.credit or 0),
            float(r.balance or 0)
        ])

    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name=f"coa_balances_{period}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
####COA GL_DRIL DOWN

@admin_bp.route('/coa/<gl_account>/transactions')
@login_required
def coa_transactions(gl_account):
    from datetime import date

    today = date.today()
    year_start = date(today.year, 1, 1)

    txns = (
        Transaction.query
        .filter(
            Transaction.gl_account == gl_account,
            Transaction.created_at >= year_start
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )

    return render_template(
        "admin/coa_transactions.html",
        gl_account=gl_account,
        transactions=txns
    )


from datetime import date
from sacco_app.services.accounting_service import generate_opening_balances
from sacco_app.utils.audit import log_activity

## GENERATE OPENING BALANCE
@admin_bp.route('/coa/generate-opening/<int:year>', methods=['POST'])
@login_required
def generate_opening(year):
    if current_user.role != 'admin':
        flash("Unauthorized action", "danger")
        return redirect(request.referrer)

    created = generate_opening_balances(year)

    log_activity(
        action="Generate opening balances",
        details=f"Generated {created} opening balances for year {year}"
    )

    flash(
        f"Opening balances generated for {year} "
        f"({created} GL accounts created)",
        "success"
    )

    return redirect(url_for('admin.coa_balances', year=year))

## member_lookup

@admin_bp.route('/members/lookup/<member_no>')
@login_required
def lookup_member(member_no):
    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        return {"found": False}
    return {"found": True, "name": member.name}

#sending sms POSTINGS
@admin_bp.route("/test-sms")
def test_sms():
    from sacco_app.utils.sms import send_sms
    send_sms("+254721313527", "Hello from Chairete SACCO 🚀")
    return "SMS sent"

#charging membership fee

@admin_bp.route("/fees/membership", methods=["GET", "POST"])
@login_required
def charge_membership_fee():
    if request.method == "GET":
        return render_template("admin/charge_membership_fee.html")

    member_no = request.form["member_no"]
    amount = Decimal(request.form["amount"])
    narration = request.form["narration"]

    member = Member.query.filter_by(member_no=member_no).first()
    savings = SaccoAccount.query.filter_by(member_no=member_no, account_type="SAVINGS").first()
    reg_fee = SaccoAccount.query.filter_by(account_number="M000GL_REG_FEE").first()

    if not member or not savings or savings.balance < amount:
        flash("Invalid member or insufficient savings", "danger")
        return redirect(request.url)

    txn_no = f"TXN{uuid.uuid4().hex[:10].upper()}"
    txn_date = datetime.now()

    # Debit member savings
    savings.balance -= amount
    txn1 = Transaction(
        txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
        member_no=member_no,
        account_no=savings.account_number,
        gl_account='SAVINGS',
        tran_type='SAVINGS',
        debit_amount=amount,
        credit_amount=Decimal('0'),
        reference=txn_no,
        narration=narration,
        bank_txn_date=txn_date,
        posted_by=current_user.username,
        running_balance=savings.balance,
        created_at=txn_date
    )

    # Credit registration fee income
    reg_fee.balance += amount
    txn2 = Transaction(
        txn_no=f"TXN{uuid.uuid4().hex[:10].upper()}",
        member_no="M000GL",
        account_no=reg_fee.account_number,
        gl_account='REGFEE',
        tran_type='INCOME',
        debit_amount=Decimal('0'),
        credit_amount=amount,
        reference=txn_no,
        narration=f"{narration} - {member_no}",
        bank_txn_date=txn_date,
        posted_by=current_user.username,
        running_balance=reg_fee.balance,
        created_at=txn_date
    )

    db.session.add_all([txn1, txn2])
    db.session.commit()

    flash(f"KES {amount:,.2f} membership fee charged to {member_no}", "success")
    return redirect(url_for("admin.charge_membership_fee"))

##GUARATORS VIEW
@admin_bp.route('/member-guarantees', methods=['GET', 'POST'])
@login_required
def member_guarantees():
    member_no = None
    guarantees = []
    total_guaranteed = 0

    if request.method == 'POST':
        member_no = request.form.get('member_no').strip()

        sql = text("""
            SELECT 
                lg.loan_no,
                lg.member_no AS borrower_no,
                lg.amount_guaranteed,
                m.name AS borrower_name
            FROM loan_guarantors lg
            LEFT JOIN members m ON m.member_no = lg.member_no
            WHERE lg.guarantor_no = :member_no
        """)

        guarantees = db.session.execute(
            sql, {"member_no": member_no}
        ).fetchall()

        total_guaranteed = sum(
            g.amount_guaranteed for g in guarantees
        )

    return render_template(
        'admin/member_guarantees.html',
        member_no=member_no,
        guarantees=guarantees,
        total_guaranteed=total_guaranteed
    )


@admin_bp.route('/loan-guarantors/<loan_no>')
@login_required
def loan_guarantors(loan_no):

    sql = text("""
        SELECT 
            lg.guarantor_no,
            m.name,
            lg.amount_guaranteed
        FROM loan_guarantors lg
        LEFT JOIN members m ON m.member_no = lg.guarantor_no
        WHERE lg.loan_no = :loan_no
    """)

    guarantors = db.session.execute(
        sql, {"loan_no": loan_no}
    ).fetchall()

    return render_template(
        'admin/loan_guarantors.html',
        guarantors=guarantors,
        loan_no=loan_no
    )

@admin_bp.route('/active-loan-guarantors', methods=['GET', 'POST'])
@login_required
def active_loan_guarantors():

    member_no = None
    loan = None
    guarantors = []
    total_guaranteed = 0

    if request.method == 'POST':
        member_no = request.form.get('member_no').strip()

        # 1️⃣ Get active loan for member
        loan_sql = text("""
            SELECT loan_no, loan_amount, balance
            FROM loans
            WHERE member_no = :member_no
              AND balance > 0
            ORDER BY id DESC
            LIMIT 1
        """)

        loan = db.session.execute(
            loan_sql, {"member_no": member_no}
        ).fetchone()

        # 2️⃣ If loan exists, get guarantors
        if loan:
            guarantor_sql = text("""
            SELECT 
                lg.guarantor_no,
                m.name,
                m.phone,
                lg.amount_guaranteed
            FROM loan_guarantors lg
            LEFT JOIN members m 
                   ON m.member_no = lg.guarantor_no
            WHERE lg.loan_no = :loan_no
            """)


            guarantors = db.session.execute(
                guarantor_sql, {"loan_no": loan.loan_no}
            ).fetchall()

            total_guaranteed = sum(
                g.amount_guaranteed for g in guarantors
            )

    return render_template(
        'admin/active_loan_guarantors.html',
        member_no=member_no,
        loan=loan,
        guarantors=guarantors,
        total_guaranteed=total_guaranteed
    )
    
##loan statement
from flask import render_template, request, flash
from flask_login import login_required
from sqlalchemy import text
from sacco_app.models import Member
from sacco_app.extensions import db


@admin_bp.route('/loan-statement_new', methods=['GET', 'POST'])
@login_required
def loan_statement_new():
    member = None
    loan = None
    schedules = []
    totals = {
        "principal_due": 0,
        "interest_due": 0,
        "principal_paid": 0,
        "interest_paid": 0
    }
    arrears_principal = 0
    arrears_interest = 0

    if request.method == 'POST':
        member_no = request.form.get('member_no')

        # 1️⃣ Get MEMBER (MODEL – important for base.html)
        member = Member.query.filter_by(member_no=member_no).first()

        if not member:
            flash("Member not found", "danger")
            return render_template("admin/loan_statement_form_new.html")

        # 2️⃣ Get ACTIVE LOAN
        loan = db.session.execute(text("""
            SELECT *
            FROM loans
            WHERE member_no = :member_no
              AND status = 'Active'
            ORDER BY created_at DESC
            LIMIT 1
        """), {"member_no": member_no}).fetchone()

        if not loan:
            flash("This member has no active loan", "warning")
            return render_template(
                "admin/loan_statement_form_new.html",
                member=member
            )

        # 3️⃣ Get LOAN SCHEDULE
        schedules = db.session.execute(text("""
            SELECT
                installment_no,
                due_date,
                principal_due,
                interest_due,
                principal_paid,
                interest_paid,
                principal_balance,
                status
            FROM loan_schedules
            WHERE loan_no = :loan_no
            ORDER BY installment_no ASC
        """), {"loan_no": loan.loan_no}).fetchall()

        # 4️⃣ Totals & arrears calculation
        for s in schedules:
            totals["principal_due"] += s.principal_due or 0
            totals["interest_due"] += s.interest_due or 0
            totals["principal_paid"] += s.principal_paid or 0
            totals["interest_paid"] += s.interest_paid or 0

            arrears_principal += max(0, (s.principal_due or 0) - (s.principal_paid or 0))
            arrears_interest += max(0, (s.interest_due or 0) - (s.interest_paid or 0))

    return render_template(
        "admin/loan_statement_form_new.html",
        member=member,
        loan=loan,
        schedules=schedules,
        totals=totals,
        arrears_principal=arrears_principal,
        arrears_interest=arrears_interest
    )

@admin_bp.route('/loan-statement-pdf-new', methods=['GET', 'POST'])
@login_required
def loan_statement_pdf_new():
    """
    Generates a professional SACCO loan statement PDF
    using loans + loan_schedules tables.
    """

    from flask import current_app, send_file, request, flash, redirect, url_for
    from sacco_app.models import Member
    from sacco_app.extensions import db
    from sqlalchemy import text
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

    # ---------------- Parameters ----------------
    member_no = (request.values.get('member_no') or '').strip()
    today = date.today()

    if not member_no:
        flash("Member number is required.", "warning")
        return redirect(url_for('admin.loan_statement_new'))

    # ---------------- Member ----------------
    member = Member.query.filter_by(member_no=member_no).first()
    if not member:
        flash("Member not found.", "danger")
        return redirect(url_for('admin.loan_statement_new'))

    # ---------------- Loan ----------------
    loan = db.session.execute(text("""
        SELECT *
        FROM loans
        WHERE member_no = :member_no
          AND status = 'Active'
        ORDER BY created_at DESC
        LIMIT 1
    """), {"member_no": member_no}).fetchone()

    if not loan:
        flash("No active loan found for this member.", "warning")
        return redirect(url_for('admin.loan_statement_new'))

    # ---------------- Loan Schedules ----------------
    schedules = db.session.execute(text("""
        SELECT
            installment_no,
            due_date,
            principal_due,
            interest_due,
            principal_paid,
            interest_paid,
            principal_balance,
            status
        FROM loan_schedules
        WHERE loan_no = :loan_no
        ORDER BY installment_no ASC
    """), {"loan_no": loan.loan_no}).fetchall()

    # ---------------- Totals ----------------
    principal_amount = Decimal(loan.loan_amount or 0)
    total_principal_paid = sum(Decimal(s.principal_paid or 0) for s in schedules)
    total_interest_paid = sum(Decimal(s.interest_paid or 0) for s in schedules)
    outstanding_balance = Decimal(loan.balance or 0)

    # ---------------- PDF Setup ----------------
    buffer = BytesIO()
    filename = f"LOAN_{loan.loan_no}.pdf"

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "header", fontSize=14, leading=18,
        alignment=TA_LEFT, textColor=colors.HexColor("#002060")
    )
    sub_style = ParagraphStyle(
        "sub", fontSize=10, textColor=colors.gray, spaceAfter=4
    )

    story = []

    # ---------------- Header ----------------
    logo_path = current_app.root_path + "/static/img/logo.png"
    try:
        logo = Image(logo_path, width=3 * cm, height=3 * cm)
    except Exception:
        logo = Paragraph("<b>SACCO LOGO</b>", styles["Normal"])

    header_info = [
        [Paragraph("<b><u>PCEA CHAIRETE SACCO LTD</u></b>",
                   ParagraphStyle("sacco", fontSize=14, textColor=colors.HexColor("#002060")))],
        [Paragraph(f"<b>Member:</b> {member.name} ({member.member_no})", sub_style)],
        [Paragraph(f"<b>Loan No:</b> {loan.loan_no}", sub_style)],
        [Paragraph(
            f"<b>Disbursed:</b> {loan.disbursed_date.strftime('%Y-%m-%d')} | "
            f"<b>Type:</b> {loan.loan_type}",
            sub_style
        )],
    ]

    header_table = Table(
        [[logo, Table(header_info, colWidths=[11 * cm])]],
        colWidths=[3 * cm, 12 * cm]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 10))

    # ---------------- Title ----------------
    story.append(Paragraph("<b>Loan Statement</b>", ParagraphStyle(
        "title", fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor("#002060")
    )))
    story.append(Spacer(1, 12))

    # ---------------- Summary ----------------
    summary_data = [
        ["Principal Amount", f"KSh {principal_amount:,.2f}"],
        ["Total Principal Paid", f"KSh {total_principal_paid:,.2f}"],
        ["Total Interest Paid", f"KSh {total_interest_paid:,.2f}"],
        ["Total Paid (Principal + Interest)", f"KSh {(total_principal_paid + total_interest_paid):,.2f}"],
        ["Outstanding Balance", f"KSh {outstanding_balance:,.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[8 * cm, 6 * cm])
    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 12))

    # ---------------- Schedule Table ----------------
    data = [[
        "No", "Due Date",
        "Principal Due", "Interest Due",
        "Principal Paid", "Interest Paid",
        "Balance", "Status"
    ]]

    if not schedules:
        data.append(["", "No installments found", "", "", "", "", "", ""])
    else:
        for s in schedules:
            data.append([
                s.installment_no,
                s.due_date.strftime("%Y-%m-%d"),
                f"{Decimal(s.principal_due or 0):,.2f}",
                f"{Decimal(s.interest_due or 0):,.2f}",
                f"{Decimal(s.principal_paid or 0):,.2f}",
                f"{Decimal(s.interest_paid or 0):,.2f}",
                f"{Decimal(s.principal_balance or 0):,.2f}",
                s.status
            ])

    schedule_table = Table(
        data,
        colWidths=[1.2*cm, 2.5*cm, 2.6*cm, 2.6*cm, 2.6*cm, 2.6*cm, 2.8*cm, 2.0*cm],
        repeatRows=1
    )
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (2, 1), (-2, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))

    story.append(schedule_table)
    story.append(Spacer(1, 20))

    # ---------------- Footer ----------------
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(
            A4[0] - 1.5 * cm, 1.2 * cm,
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Page {canvas.getPageNumber()}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


##MONTHLY BALANCE FOR MEMBERS
from sqlalchemy import func
from datetime import date
from sacco_app.models.monthly_balance import MemberMonthlyBalance
def generate_monthly_balances(year, month):
    SAVINGS_GLS = ("SAVINGS", "LIABILITY")
    start_date = date(year, month, 1)
    end_date = date(year + (month == 12), (month % 12) + 1, 1)

    members = Member.query.all()

    for member in members:
        # Previous month closing
        prev = MemberMonthlyBalance.query.filter(
            MemberMonthlyBalance.member_id == member.id,
            (MemberMonthlyBalance.year < year) |
            (
                (MemberMonthlyBalance.year == year) &
                (MemberMonthlyBalance.month < month)
            )
        ).order_by(
            MemberMonthlyBalance.year.desc(),
            MemberMonthlyBalance.month.desc()
        ).first()


        opening_balance = prev.closing_balance if prev else 0

        # Deposits → credit to SAVINGS
        deposits = db.session.query(
            func.coalesce(func.sum(Transaction.credit_amount), 0)
        ).filter(
            Transaction.member_no == member.member_no,
            Transaction.gl_account.in_(SAVINGS_GLS),
            Transaction.credit_amount > 0,
            Transaction.bank_txn_date >= start_date,
            Transaction.bank_txn_date < end_date
        ).scalar()

        # Withdrawals → debit from SAVINGS
        withdrawals = db.session.query(
            func.coalesce(func.sum(Transaction.debit_amount), 0)
        ).filter(
            Transaction.member_no == member.member_no,
            Transaction.gl_account.in_(SAVINGS_GLS),
            Transaction.debit_amount > 0,
            Transaction.bank_txn_date >= start_date,
            Transaction.bank_txn_date < end_date
        ).scalar()


        closing_balance = opening_balance + deposits - withdrawals

        record = MemberMonthlyBalance.query.filter_by(
            member_id=member.id,
            year=year,
            month=month
        ).first()

        if not record:
            record = MemberMonthlyBalance(
                member_id=member.id,
                year=year,
                month=month
            )

        record.opening_balance = opening_balance
        record.deposits = deposits
        record.withdrawals = withdrawals
        record.closing_balance = closing_balance

        db.session.add(record)

    db.session.commit()

@admin_bp.route("/generate-monthly-balances", methods=["POST"])
@login_required
def generate_monthly_balances_view():
    year, month = map(int, request.form["month"].split("-"))

    # Safety: prevent duplicate posting
    exists = MemberMonthlyBalance.query.filter_by(
        year=year, month=month
    ).first()

    if exists:
        flash("Monthly balances already posted for this month", "warning")
        return redirect(url_for("admin.monthly_balances"))

    generate_monthly_balances(year, month)

    flash("Monthly balances posted successfully", "success")
    return redirect(url_for("admin.monthly_balances"))

@admin_bp.route("/monthly-balances")
@login_required
def monthly_balances():
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # 🔹 Find most recent year & month
    latest = MemberMonthlyBalance.query.order_by(
        MemberMonthlyBalance.year.desc(),
        MemberMonthlyBalance.month.desc()
    ).first()

    if not latest:
        balances = []
        pagination = None
    else:
        pagination = MemberMonthlyBalance.query.join(Member).filter(
            MemberMonthlyBalance.year == latest.year,
            MemberMonthlyBalance.month == latest.month
        ).order_by(Member.member_no).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        balances = pagination.items

    return render_template(
        "admin/monthly_balances.html",
        balances=balances,
        pagination=pagination,
        mode="latest",
        latest=latest
    )
@admin_bp.route("/monthly-balances/member")
@login_required
def monthly_balances_per_member():
    member_no = request.args.get("member_no")
    year = request.args.get("member_year", type=int)   # ✅ FIX

    if not member_no or not year:
        flash("Please enter member number and year", "warning")
        return redirect(url_for("admin.monthly_balances"))

    member = Member.query.filter_by(member_no=member_no).first()

    balances = []
    if member:
        balances = MemberMonthlyBalance.query.filter_by(
            member_id=member.id,
            year=year
        ).order_by(MemberMonthlyBalance.month).all()

    return render_template(
        "admin/monthly_balances.html",
        balances=balances,
        mode="member",
        member=member,
        year=year
    )


@admin_bp.route("/monthly-balances/month")
@login_required
def monthly_balances_by_month():
    page = request.args.get("page", 1, type=int)
    per_page = 20

    year = request.args.get("filter_year", type=int)
    month = request.args.get("filter_month", type=int)

    if not year or not month:
        flash("Please select both month and year", "warning")
        return redirect(url_for("admin.monthly_balances"))

    pagination = MemberMonthlyBalance.query.join(Member).filter(
        MemberMonthlyBalance.year == year,
        MemberMonthlyBalance.month == month
    ).order_by(Member.member_no).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "admin/monthly_balances.html",
        balances=pagination.items,
        pagination=pagination,
        mode="month",
        year=year,
        month=month
    )

from sqlalchemy import func

def get_opening_balance(member, start_date):
    """
    Determine opening balance for a member at the start of a month.
    Priority:
    1) Previous monthly balance
    2) Fallback to SAVINGS GL balance before the month
    """

    # 1️⃣ Try previous monthly balance
    prev = MemberMonthlyBalance.query.filter(
        MemberMonthlyBalance.member_id == member.id,
        (MemberMonthlyBalance.year * 100 + MemberMonthlyBalance.month) <
        (start_date.year * 100 + start_date.month)
    ).order_by(
        MemberMonthlyBalance.year.desc(),
        MemberMonthlyBalance.month.desc()
    ).first()

    if prev:
        return prev.closing_balance

    # 2️⃣ Fallback to GL (CRITICAL FIX)
    return db.session.query(
        func.coalesce(
            func.sum(Transaction.debit_amount - Transaction.credit_amount),
            0
        )
    ).filter(
        Transaction.member_no == member.member_no,
        Transaction.gl_account == "SAVINGS",
        Transaction.bank_txn_date < start_date
    ).scalar()


from datetime import date
from sqlalchemy import func

from sacco_app.extensions import db
from sacco_app.models.member import Member
from sacco_app.models import Transaction
from sacco_app.models.monthly_balance import MemberMonthlyBalance
from sqlalchemy import text

SAVINGS_GL = ("SAVINGS", "LIABILITY")


def rebuild_monthly_balances(start_year=2019, end_year=2025):
    print("⚠️ Truncating member_monthly_balances...")
    db.session.execute(
        text("TRUNCATE TABLE member_monthly_balances RESTART IDENTITY CASCADE"))
    db.session.commit()

    members = Member.query.all()

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            start_date = date(year, month, 6)
            end_date = date(year + (month == 12), (month % 12) + 1, 1)

            print(f"Processing {year}-{month:02d}...")

            for member in members:
                # 🔹 Get latest previous balance (not strictly previous month)
                opening_balance = get_opening_balance(member, start_date)


                # 🔹 Deposits (credit to SAVINGS)
                deposits = db.session.query(
                    func.coalesce(func.sum(Transaction.credit_amount), 0)
                ).filter(
                    Transaction.member_no == member.member_no,
                    Transaction.gl_account.in_(SAVINGS_GL),
                    Transaction.credit_amount > 0,
                    Transaction.bank_txn_date >= start_date,
                    Transaction.bank_txn_date < end_date
                ).scalar()

                # 🔹 Withdrawals (debit from SAVINGS)
                withdrawals = db.session.query(
                    func.coalesce(func.sum(Transaction.debit_amount), 0)
                ).filter(
                    Transaction.member_no == member.member_no,
                    Transaction.gl_account.in_(SAVINGS_GL),
                    Transaction.debit_amount > 0,
                    Transaction.bank_txn_date >= start_date,
                    Transaction.bank_txn_date < end_date
                ).scalar()


                closing_balance = opening_balance + deposits - withdrawals

                record = MemberMonthlyBalance(
                    member_id=member.id,
                    year=year,
                    month=month,
                    opening_balance=opening_balance,
                    deposits=deposits,
                    withdrawals=withdrawals,
                    closing_balance=closing_balance
                )

                db.session.add(record)

            db.session.commit()

    print("✅ Monthly balances rebuild completed successfully.")

## LOANS BALANCES ADJUSTMENTS
@admin_bp.route('/loans/adjustment', methods=['GET', 'POST'])
@login_required
def loan_adjustment_page():

    loans = []
    member = None
    member_no = None

    if request.method == 'POST':

        member_no = request.form.get('member_no').strip()

        member = Member.query.filter_by(member_no=member_no).first()

        if not member:
            flash("Member not found.", "danger")
        else:
            loans = Loan.query.filter(
                Loan.member_no == member_no,
                Loan.status.in_(["Active", "Disbursed"]),
                Loan.balance > 0
            ).all()

            if not loans:
                flash("No active loans for this member.", "warning")

    return render_template(
        "admin/loan_adjustment_modal.html",
        loans=loans,
        member=member,
        member_no=member_no
    )
"""Loan Adjustment Route – posts increase/decrease adjustments with GL entries."""

from decimal import Decimal
from datetime import datetime
import uuid
from sacco_app.models.loan_adjustment import LoanAdjustment

@admin_bp.route('/loans/adjust', methods=['POST'])
@login_required
def adjust_loan():

    try:
        # ---------------- INPUTS ----------------
        loan_no = request.form.get('loan_no')
        adjustment_type = request.form.get('adjustment_type')  # increase / decrease
        amount = Decimal(request.form.get('amount')).quantize(Decimal('0.01'))
        narration = request.form.get('narration')

        if not loan_no or amount <= 0:
            flash("Invalid adjustment input.", "danger")
            return redirect(request.referrer)

        # ---------------- FETCH LOAN ----------------
        loan = Loan.query.filter_by(loan_no=loan_no).first()

        if not loan:
            flash("Loan not found.", "danger")
            return redirect(request.referrer)

        if loan.status not in ["Active", "Disbursed"]:
            flash("Only active loans can be adjusted.", "danger")
            return redirect(request.referrer)

        # ---------------- ACCOUNTS ----------------
        loan_acct = SaccoAccount.query.filter_by(
            account_number=loan.loan_account
        ).first()

        gl_loan_control = SaccoAccount.query.filter_by(
            account_number='M000GL_LOAN'
        ).first()

        gl_adjustment = SaccoAccount.query.filter_by(
            account_number='M000GL_LOAN_ADJ'
        ).first()

        if not all([loan_acct, gl_loan_control, gl_adjustment]):
            flash("Missing GL accounts for adjustment.", "danger")
            return redirect(request.referrer)

        # ---------------- VALIDATIONS ----------------
        if adjustment_type == "decrease" and loan.balance < amount:
            flash("Adjustment exceeds loan balance.", "danger")
            return redirect(request.referrer)

        # ---------------- TXN REF ----------------
        txn_ref = f"ADJ{uuid.uuid4().hex[:10].upper()}"

        # ---------------- APPLY ADJUSTMENT ----------------
        if adjustment_type == "increase":

            loan.balance += amount
            loan_acct.balance += amount
            gl_loan_control.balance += amount
            gl_adjustment.balance += amount

            dr_account = loan.loan_account
            cr_account = gl_adjustment.account_number

        else:  # decrease

            loan.balance -= amount
            loan_acct.balance -= amount
            gl_loan_control.balance -= amount
            gl_adjustment.balance -= amount
            loan_acct_balance =loan_acct.balance
            gl_loan_control_balance = gl_loan_control.balance 

            dr_account = gl_adjustment.account_number
            cr_account = loan.loan_account

        # ---------------- RECORD TRANSACTION ----------------
        txn = Transaction(
            txn_no=f"ADJ{uuid.uuid4().hex[:10].upper()}",
            reference=txn_ref,
            member_no=loan.member_no,
            account_no=loan.loan_account,
            gl_account="MEMBER_LOAN",
            tran_type="LOAN_ADJST",
            debit_amount=amount,    
            credit_amount=Decimal('0'),            
            narration=narration,
            bank_txn_date=datetime.now(),
            running_balance=loan_acct.balance,
            posted_by=current_user.id,
            created_at=datetime.now()
        )

        db.session.add(txn)
        
        txn = Transaction(
            txn_no=f"ADJ{uuid.uuid4().hex[:10].upper()}",
            reference=txn_ref,
            member_no="M000GL",
            account_no=gl_loan_control.account_number,
            gl_account="LOAN_CONTROL",
            tran_type="ASSET",
            debit_amount=Decimal('0'),    
            credit_amount=amount,            
            narration=f"Loan adjustment{loan.member_no}",
            bank_txn_date=datetime.now(),
            running_balance=gl_loan_control.balance,
            posted_by=current_user.id,
            created_at=datetime.now()
        )

        db.session.add(txn)
        
        
        # ---------------- OPTIONAL: SAVE ADJUSTMENT LOG ----------------
        adjustment = LoanAdjustment(
            loan_no=loan.loan_no,
            member_no=loan.member.member_no,
            amount=amount,
            adjustment_type=adjustment_type,
            narration=narration,
            created_by=current_user.id
        )

        db.session.add(adjustment)

        db.session.commit()

        flash(f"Loan adjustment posted successfully ({txn_ref})", "success")
        return redirect(url_for('admin.loan_adjustment_page'))
    except Exception as e:
        db.session.rollback()
        import traceback; traceback.print_exc()
        flash(f"Loan adjustment failed: {str(e)}", "danger")
        return redirect(request.referrer)