from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import check_password_hash
from sacco_app.models import User
from sacco_app.extensions import db
from sacco_app.forms import LoginForm
from . import auth_bp  # ✅ This line imports auth_bp from __init__.py


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))  # Already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
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

