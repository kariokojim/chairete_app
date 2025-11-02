from flask import redirect, url_for

def register_blueprints(app):
    from sacco_app.routes.admin import admin_bp

    app.register_blueprint(admin_bp)

    # Default route -> redirect to login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
