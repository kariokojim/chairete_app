from flask import Blueprint, render_template
bp = Blueprint('sacco', __name__, template_folder='templates', url_prefix='')
@bp.route('/')
def index():
    return render_template('sacco/index.html')
