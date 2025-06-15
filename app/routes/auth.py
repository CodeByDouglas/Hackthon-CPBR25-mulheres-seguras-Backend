from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/ping')
def ping():
    return 'pong-auth'
