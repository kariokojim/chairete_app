from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import check_password_hash
from sacco_app.models import User
from sacco_app.extensions import db
from sacco_app.forms import LoginForm
from . import auth_bp  # ✅ This line imports auth_bp from __init__.py
from sacco_app.utils.audit import log_activity


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))  # Already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            log_activity("LOGIN", f"User {user.username} logged in")
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)

    logout_user()
    flash('You have been logged out.', 'info')
    from sacco_app.forms import LoginForm  # ✅ import inside if needed
    form = LoginForm()                     # ✅ create a fresh form instance
    return render_template('auth/login.html', form=form)


##RESET PASSWORDS
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for('auth.forgot_password'))

        token = user.get_reset_token()
        reset_link = url_for('auth.reset_password', token=token, _external=True)

        # SEND RESET EMAIL/SMS
        send_password_reset_email(user.email, reset_link)

        flash("A password reset link has been sent to your email.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or expired token.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        user.set_password(password)  # uses your method
        db.session.commit()

        flash("Your password has been reset. Login now.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')


def send_password_reset_email(to_email, reset_url):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = "SACCO System Password Reset"
    msg['From'] = "sewatyventures@gmail.com"
    msg['To'] = to_email
    msg.set_content(f"""
A password reset was requested. Click the link below:

{reset_url}

If you did not request this, ignore this email.
""")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login("sewatyventures@gmail.com", "cpah wnrt hjkd lvns")
        smtp.send_message(msg)

