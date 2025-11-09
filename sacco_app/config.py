import os
class Config:    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_SECRET_KEY = 'something-secure'
    WTF_CSRF_IGNORE_EXEMPT = True
    WTF_I18N_ENABLED = False

