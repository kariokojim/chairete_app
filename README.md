SACCO App - Admin Final (Postgres, full)

Default DATABASE_URL in sacco_app/config.py is set to:
postgresql+psycopg2://postgres:postgres@localhost:5432/sacco_db

Setup:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# run alembic migrations (flask db upgrade)
python create_admin.py
python seed_chart_data.py
python run.py
