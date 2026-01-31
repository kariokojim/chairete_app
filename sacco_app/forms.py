# alembic env placeholder
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, FormField, PasswordField,SelectField, SubmitField,DateField,DecimalField,FieldList,IntegerField
from wtforms.validators import DataRequired,Email, Length, EqualTo,Optional,NumberRange
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('staff', 'Staff'),('treasurer', 'Treasurer'), ('member', 'Member')], validators=[DataRequired()])
    submit = SubmitField('Create User')
    
class AddMemberForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=60)])
    email = StringField("Email", validators=[Optional(), Length(max=30), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    dob = DateField("Date of Birth", format="%Y-%m-%d", validators=[Optional()])
    id_no = StringField("National ID No", validators=[Optional(), Length(max=20)])
    congregation = StringField("Congregation", validators=[Optional(), Length(max=100)])
    gender = SelectField("Gender", choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female'),('Organization', 'Organization')])
    submit = SubmitField("Save Member")

class OpenAccountForm(FlaskForm):
    member_no = StringField("Member Number", validators=[DataRequired()])
    member_name = StringField("Member Name", render_kw={'readonly': True})
    account_type = SelectField(
        "Account Type",
        choices=[
            ('Savings', 'Savings'),
            ('Interest', 'Interest'),
            ('Share Capital', 'Share Capital'),
            ('Loan Liability', 'Loan Liability')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Open Account")

class PaymentPostingForm(FlaskForm):
    member_no = StringField('Member Number', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    reference = StringField('Reference')
    narration = StringField('Narration')
    bank_txn_date = DateField('Transaction Date', validators=[DataRequired()])
    submit = SubmitField('Post Payment')
    
    
class GuarantorForm(FlaskForm):
    member_no = StringField('Guarantor Member No', validators=[DataRequired()])
    amount_guaranteed = DecimalField('Amount Guaranteed', validators=[DataRequired(), NumberRange(min=1)])


class LoanDisbursementForm(FlaskForm):
    member_no = StringField("Member No", validators=[DataRequired()])
    loan_amount = DecimalField("Loan Amount", validators=[DataRequired()])
    loan_period = IntegerField("Loan Period (Months)", validators=[DataRequired()])
    loan_type = SelectField(
        "Loan Type",
        choices=[
            ('normal', 'Normal Loan'),
            ('topup', 'Top-up Loan'),
            ('emergency', 'Emergency Loan'),
            ('development', 'Development Loan'),
        ],
        default='normal'
    )
    submit = SubmitField("Disburse Loan")

    
class MemberDepositSearchForm(FlaskForm):
    member_no = StringField('Member No', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Search')
    
# sacco_app/forms.py



class UploadMemberSavingsForm(FlaskForm):
    file = FileField('Upload Excel File', validators=[
        FileRequired(),
        FileAllowed(['xlsx'], 'Excel files only!')
    ])
    submit = SubmitField('Upload & Post')


class LoanRepaymentForm(FlaskForm):
    member_no = StringField('Member Number', validators=[DataRequired(), Length(max=20)])
    amount = DecimalField('Amount', validators=[DataRequired()], places=2)
    bank_txn_date = DateField('Transaction Date', format='%Y-%m-%d', validators=[DataRequired()])
    narration = TextAreaField('Narration', default='Member deposit')
    submit = SubmitField('Post Payment')
