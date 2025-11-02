import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

# === CONFIGURATION ===
BALANCE_DATE = date(2025, 8, 31)   # Balances as of 31-Aug-2025
OUTPUT_FILE = "remaining_schedules_from_sep.xlsx"
MONTHLY_BASE_RATE_DIVISOR = Decimal('12')  # convert annual % to monthly

# === LOAD YOUR EXCEL FILE ===
df = pd.read_excel(r"C:\MyApp\data\running_loans.xlsx")

all_schedules = []

for _, row in df.iterrows():
    loan_no = str(row['loan_no']).strip()
    member_no = str(row['member_no']).strip()
    disb_date = pd.to_datetime(row['disbursement_date']).date()
    loan_amount = Decimal(str(row['loan_amount']))
    principal_balance = Decimal(str(row['principal_balance']))
    interest_rate = Decimal(str(row['interest_rate'])) / 100
    period_months = int(row['period_months'])

    # --- Calculate elapsed and remaining months as of Aug-2025
    months_elapsed = (BALANCE_DATE.year - disb_date.year) * 12 + (BALANCE_DATE.month - disb_date.month)
    months_remaining = max(period_months - months_elapsed, 1)

    # --- Define next due date: one month after balance date
    next_due_date = BALANCE_DATE + relativedelta(months=1)

    # --- Monthly interest rate
    monthly_rate = interest_rate / MONTHLY_BASE_RATE_DIVISOR

    # --- Calculate monthly installment using amortization formula (reducing)
    if monthly_rate > 0:
        emi = principal_balance * (monthly_rate * (1 + monthly_rate) ** months_remaining) / ((1 + monthly_rate) ** months_remaining - 1)
    else:
        emi = principal_balance / months_remaining

    balance = principal_balance

    for i in range(1, months_remaining + 1):
        interest_due = balance * monthly_rate
        principal_due = emi - interest_due
        balance -= principal_due

        all_schedules.append({
            'loan_no': loan_no,
            'member_no': member_no,
            'as_of_balance_date': BALANCE_DATE,
            'installment_no': i,
            'due_date': next_due_date,
            'principal_due': round(principal_due, 2),
            'interest_due': round(interest_due, 2),
            'total_due': round(principal_due + interest_due, 2),
            'remaining_balance': round(balance, 2)
        })

        next_due_date += relativedelta(months=1)

# --- Save to Excel
out_df = pd.DataFrame(all_schedules)
out_df.to_excel(OUTPUT_FILE, index=False)
print(f"✅ Generated {len(out_df)} remaining schedule rows saved to {OUTPUT_FILE}")
