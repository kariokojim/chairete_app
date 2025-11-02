from sacco_app import create_app
from sacco_app.extensions import db
from sacco_app.models import User  # adjust if your user model is named differently
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin user already exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@sacco.local',
            password_hash=generate_password_hash('admin123'),  # default password
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created: username='admin', password='admin123'")
    else:
        print("⚠️ Admin user already exists.")
