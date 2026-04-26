import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_this_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:Cariocoh%40100@localhost:5432/sacco_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_SECRET_KEY = 'something-secure'
    WTF_CSRF_IGNORE_EXEMPT = True
    WTF_I18N_ENABLED = False
    SMTP_USER = "sewatyventures@gmail.com"
    SMTP_PASSWORD = "cpah wnrt hjkd lvns"
    MAX_FAILED_LOGINS = 5
    LOCKOUT_MINUTES = 15
    AT_USERNAME = "sandbox"
    AT_API_KEY = "atsk_5682bdeb5546734fda25807ea3bb83e9ef7768e266532c7574549f7f88dd44ea24782dfd"
    CELCOM_SMS_URL = "https://isms.celcomafrica.com/api/services/sendsms"
    CELCOM_PARTNER_ID = "1067"
    CELCOM_API_KEY = "2316d20c5f850cc7b01e3b7d0e6700dc"
    CELCOM_SHORTCODE = "CHAIRETE"




