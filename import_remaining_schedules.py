import pandas as pd
from sacco_app import db, create_app   # ensure create_app or app import works for your setup
from sacco_app.models import LoanSchedule
from datetime import datetime
from decimal import Decimal

# === 1️⃣ Load your regenerated Excel ===
file_path = "remaining_schedules_from_sep.xlsx"
df = pd.read_excel(file_path)

print(f"Loaded {len(df)} rows from {file_path}")

# === 2️⃣ Create app context ===
app = create_app()  # <-- use this if you have factory pattern
# OR: from sacco_app import app  (if your app is defined globally)

with app.app_context():
    # --- Optional: Clear existing schedules for same loans
    loan_nos = df['loan_no'].unique().tolist()
    print(f"Loans found in file: {loan_nos}")

    confirm = input("⚠️  Delete existing future schedules for these loans? (y/n): ").strip().lower()
    if confirm == 'y':
        deleted = LoanSchedule.query.filter(
            LoanSchedule.loan_no.in_(loan_nos),
            LoanSchedule.status.in_(['DUE', 'PARTIAL'])
        ).delete(synchronize_session=False)
        db.session.commit()
        print(f"Deleted {deleted} old schedule rows.")

    # --- Insert new schedules
    count = 0
    for _, r in df.iterrows():
        sched = LoanSchedule(
            loan_no=str(r['loan_no']).strip(),
            installment_no=int(r['installment_no']),
            due_date=pd.to_datetime(r['due_date']).date(),
            principal_due=Decimal(str(r['principal_due'])),
            interest_due=Decimal(str(r['interest_due'])),
            principal_balance=Decimal(str(r['remaining_balance'])),
            principal_paid=Decimal('0.00'),
            interest_paid=Decimal('0.00'),
            member_no=str(r['member_no']).strip(),
            status='DUE'
        )
        db.session.add(sched)
        count += 1

    db.session.commit()
    print(f"✅ Inserted {count} new schedule rows into database successfully.")
