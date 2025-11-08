from flask import Flask, redirect, url_for
from flask_login import current_user
from .config import Config
from .extensions import db, login_manager, migrate, csrf
#from .models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from sacco_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from sacco_app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        # Smart redirect: if logged in, send to dashboard
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'staff':
                return redirect(url_for('staff.dashboard'))
            else:
                return redirect(url_for('member.dashboard'))
        return redirect(url_for('auth.login'))
        # Health check
    @app.route("/ping")
    def ping():
        return {"status": "ok", "message": "Sacco app running!"}, 200
    return app
