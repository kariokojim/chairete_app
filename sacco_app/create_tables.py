

from sacco_app import create_app
from sacco_app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    print('Created tables via create_all()')

