from sacco_app.models import AuditLog
from sacco_app import db
from flask_login import current_user
from flask import request

def log_activity(action, details=None):
    log = AuditLog(
        user_id=current_user.id if current_user.is_authenticated else None,
        action=action,
        details=details,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
