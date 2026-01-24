from flask import request
from flask_login import current_user
from sacco_app.extensions import db
from sacco_app.models import AuditLog


def log_activity(
    action,
    details=None,
    entity_type=None,
    entity_id=None,
    event_type=None,
    before_data=None,
    after_data=None,
    auto_commit=False   # 👈 DEFAULT FALSE
):
    log = AuditLog(
        user_id=current_user.id if current_user.is_authenticated else None,
        action=action,
        details=details,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id else None,
        event_type=event_type,
        before_data=before_data,
        after_data=after_data,
        ip_address=request.remote_addr
    )

    db.session.add(log)

    if auto_commit:
        db.session.commit()
