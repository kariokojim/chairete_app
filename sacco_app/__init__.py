from flask import Flask, redirect, url_for, flash, request
from flask_login import current_user, logout_user
from datetime import datetime, timedelta
import os
from .config import Config
from .extensions import db, login_manager, migrate, csrf
from sacco_app.utils.sidebar import SIDEBAR_ITEMS

def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app.config['UPLOAD_FOLDER'] = os.path.join(
        BASE_DIR, 'uploads', 'bank_statements'
    )

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.config.from_object(Config)

    # ------------------------------
    # Initialize core extensions
    # ------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "warning"

    # ------------------------------
    # Register Blueprints
    # ------------------------------
    from sacco_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from sacco_app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    # You can register staff/member blueprints here if you have them
    # from sacco_app.routes.staff import staff_bp
    # app.register_blueprint(staff_bp)
    # from sacco_app.routes.member import member_bp
    # app.register_blueprint(member_bp)

    # ------------------------------
    # Session Timeout Middleware
    # ------------------------------
    @app.before_request
    def session_timeout():
        """
        Automatically logs out user after 6 hours of inactivity.
        Updates last_activity on every valid request.
        """
        if current_user.is_authenticated:
            now = datetime.utcnow()

            try:
                # Check inactivity
                if current_user.last_activity and \
                   now - current_user.last_activity > timedelta(seconds=100):

                    logout_user()
                    flash("Session expired due to inactivity.", "warning")
                    return redirect(url_for('auth.login'))

                # Update last activity timestamp
                current_user.last_activity = now
                db.session.commit()

            except Exception:
                # Avoid errors for routes without DB access
                pass

    # ------------------------------
    # Smart homepage redirect
    # ------------------------------
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'staff':
                return redirect(url_for('staff.dashboard'))
            else:
                return redirect(url_for('member.dashboard'))

        return redirect(url_for('auth.login'))

    # ------------------------------
    # Health Check
    # ------------------------------
    
    @app.route("/ping")
    def ping():
        return {"status": "ok", "message": "Sacco app running!"}, 200

    # ------------------------------
    # sidebar menus
    # ------------------------------
       
    @app.context_processor
    def inject_sidebar():
        if not current_user.is_authenticated:
            return dict(sidebar_items=[])

        user_role = current_user.role

        filtered_items = [
            item for item in SIDEBAR_ITEMS
            if user_role in item["roles"]
        ]
        return dict(sidebar_items=filtered_items)

    return app
