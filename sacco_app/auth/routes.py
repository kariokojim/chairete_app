from flask import (
    render_template, redirect, url_for,
    flash, request, current_app
)
from flask_login import (
    login_user, logout_user,
    login_required, current_user
)

from sacco_app.extensions import db
from sacco_app.models import User
from sacco_app.forms import LoginForm
from sacco_app.utils.audit import log_activity

from . import auth_bp

import smtplib
from email.message import EmailMessage


# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # ---- USER NOT FOUND ----
        if not user:
            log_activity(
                action="Failed login attempt",
                entity_type="USER",
                entity_id=form.username.data,
                event_type="LOGIN_FAILED",
                details="Invalid username",
                auto_commit=True
            )
            flash("Invalid username or password.", "danger")
            return render_template('auth/login.html', form=form)

        # ---- ACCOUNT LOCKED ----
        if user.is_account_locked():
            log_activity(
                action="Login blocked (account locked)",
                entity_type="USER",
                entity_id=user.id,
                event_type="LOGIN_LOCKED",
                details="Login attempt while account locked",
                auto_commit=True
            )
            flash(
                "Account locked due to multiple failed logins. "
                "Try again later.",
                "danger"
            )
            return render_template('auth/login.html', form=form)

        # ---- PASSWORD CHECK ----
        if user.check_password(form.password.data):
            login_user(user)

            # reset counters
            user.failed_login_attempts = 0
            user.account_locked_until = None
            db.session.commit()

            log_activity(
                action="User login",
                entity_type="USER",
                entity_id=user.id,
                event_type="LOGIN",
                details=f"User {user.username} logged in successfully",
                auto_commit=True
            )

            return redirect(url_for('admin.dashboard'))

        # ---- WRONG PASSWORD ----
        user.register_failed_login()
        db.session.commit()

        log_activity(
            action="Failed login attempt",
            entity_type="USER",
            entity_id=user.id,
            event_type="LOGIN_FAILED",
            details=f"Failed login attempt #{user.failed_login_attempts}",
            auto_commit=True
        )

        if user.is_account_locked():
            log_activity(
                action="Account locked",
                entity_type="USER",
                entity_id=user.id,
                event_type="ACCOUNT_LOCKED",
                details="Account locked due to failed logins",
                auto_commit=True
            )
            flash(
                "Your account has been locked due to multiple "
                "failed login attempts.",
                "danger"
            )
        else:
            flash("Invalid username or password.", "danger")

    return render_template('auth/login.html', form=form)

# ----------------------------------------------------
# LOGOUT
# ----------------------------------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    username = current_user.username

    logout_user()

    log_activity(
        action="User logout",
        entity_type="USER",
        entity_id=user_id,
        event_type="LOGOUT",
        details=f"User {username} logged out",
        auto_commit=True
    )

    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


# ----------------------------------------------------
# FORGOT PASSWORD
# ----------------------------------------------------
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            log_activity(
                action="Password reset request failed",
                entity_type="USER",
                entity_id=email,
                event_type="RESET_REQUEST_FAILED",
                details="Reset requested for non-existent email",
                auto_commit=True
            )
            flash("Email not found.", "danger")
            return redirect(url_for('auth.forgot_password'))

        token = user.get_reset_token()
        reset_link = url_for(
            'auth.reset_password',
            token=token,
            _external=True
        )

        send_password_reset_email(user.email, reset_link)

        log_activity(
            action="Password reset requested",
            entity_type="USER",
            entity_id=user.id,
            event_type="RESET_REQUEST",
            details=f"Reset link sent to {user.email}",
            auto_commit=True
            
        )

        flash(
            "A password reset link has been sent to your email.",
            "success"
        )
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


# ----------------------------------------------------
# RESET PASSWORD
# ----------------------------------------------------
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)

    if not user:
        log_activity(
            action="Invalid password reset token",
            entity_type="USER",
            entity_id=None,
            event_type="RESET_INVALID_TOKEN",
            details="Expired or invalid reset token used",
            auto_commit=True
        )
        flash("Invalid or expired token.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')

        if not password or len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(request.url)

        # ✅ HASHED PASSWORD (CRITICAL)
        user.set_password(password)
        db.session.commit()

        log_activity(
            action="Password reset successful",
            entity_type="USER",
            entity_id=user.id,
            event_type="RESET_SUCCESS",
            details="User reset password successfully",
            auto_commit=True
        )

        flash("Your password has been reset. Login now.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')


# ----------------------------------------------------
# EMAIL SENDER
# ----------------------------------------------------
from sacco_app.utils.email_utils import send_email

def send_password_reset_email(to_email, reset_url):
    body = f"""
    A password reset was requested for your SACCO account.

    Click the link below to reset your password:

    {reset_url}

    If you did not request this, please ignore this email.
    """

    send_email(
        to_email=to_email,
        subject="SACCO System Password Reset",
        body=body
    )

