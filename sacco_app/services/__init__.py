from decimal import Decimal
from dateutil.relativedelta import relativedelta
from datetime import date

CENT = Decimal('0.01')

def generate_reducing_balance_schedule(principal, annual_rate, term_months, disbursement_date):
    principal = Decimal(principal).quantize(CENT)
    monthly_rate = Decimal(annual_rate) / Decimal('12')
    principal_each = (principal / term_months).quantize(CENT)
    schedule = []
    outstanding = principal
    for i in range(term_months):
        due = disbursement_date + relativedelta(months=i+1)
        interest = (outstanding * monthly_rate).quantize(CENT)
        if i == term_months - 1:
            principal_due = outstanding
        else:
            principal_due = principal_each
        schedule.append({'due_date': due, 'principal_due': principal_due, 'interest_due': interest})
        outstanding = (outstanding - principal_due).quantize(CENT)
    return schedule
