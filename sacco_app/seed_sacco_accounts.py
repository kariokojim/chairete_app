from sacco_app import create_app
from extensions import db
from models import SaccoAccount  # adjust if your model file is named differently
from datetime import datetime

def seed_sacco_accounts():
    app = create_app()
    with app.app_context():
        gl_accounts = [
            {'account_number': 'M000GL_CASH', 'account_type': 'CASH_ACC', 'desc': 'Cash Control Account'},
            {'account_number': 'M000GL_LOAN', 'account_type': 'LOANS', 'desc': 'Loan Control Account'},
            {'account_number': 'M000GL_SAVINGS', 'account_type': 'SAVINGS', 'desc': 'Savings Control Account'},
            {'account_number': 'M000GL_SHARE_CAP', 'account_type': 'EQUITY', 'desc': 'Share Capital Control Account'},
            {'account_number': 'M000GL_LN_INT', 'account_type': 'INCOME', 'desc': 'Loan Interest Income'},
            {'account_number': 'M000GL_LN_APP_FEE', 'account_type': 'INCOME', 'desc': 'Loan Appraisal Fee Income'},
            {'account_number': 'M000GL_REG_FEE', 'account_type': 'INCOME', 'desc': 'Member Registration Fee Income'},
            {'account_number': 'M000GL_MM_INT', 'account_type': 'INCOME', 'desc': 'Money Market Interest Income'},
            {'account_number': 'M000GL_EXPS', 'account_type': 'EXPENSE', 'desc': 'Operational Expenses Account'},
        ]

        for acc in gl_accounts:
            existing = SaccoAccount.query.filter_by(account_number=acc['account_number']).first()
            if not existing:
                new_acc = SaccoAccount(
                    member_no='M000GL',
                    account_number=acc['account_number'],
                    account_type=acc['account_type'],
                    balance=0.00,
                    interest_rate=0.00,
                    limit=100000000.00,
                    status='active',
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    created_by='admin'
                )
                db.session.add(new_acc)
                print(f"Added: {acc['desc']}")
            else:
                print(f"Exists: {acc['desc']}")

        db.session.commit()
        print("✅ SACCO GL control accounts seeded successfully!")

if __name__ == '__main__':
    seed_sacco_accounts()
