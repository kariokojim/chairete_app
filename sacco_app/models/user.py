from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

from sacco_app.extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔐 ACCOUNT LOCKOUT FIELDS
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)

    # ---------------------------
    # PASSWORD HANDLING
    # ---------------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ---------------------------
    # ACCOUNT LOCKOUT HELPERS  ✅ ADD HERE
    # ---------------------------
    def is_account_locked(self):
        if self.account_locked_until:
            if datetime.utcnow() < self.account_locked_until:
                return True
            # Auto-unlock when time expires
            self.account_locked_until = None
            self.failed_login_attempts = 0
        return False

    def register_failed_login(self, max_attempts=5, lock_minutes=15):
        self.failed_login_attempts += 1

        if self.failed_login_attempts >= max_attempts:
            self.account_locked_until = (
                datetime.utcnow() + timedelta(minutes=lock_minutes)
            )

    # ---------------------------
    # PASSWORD RESET TOKENS
    # ---------------------------
    def get_reset_token(self, expires_sec=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data.get('user_id')
        except Exception:
            return None
        return User.query.get(user_id)


# --------------------------------
# Flask-Login user loader
# --------------------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
