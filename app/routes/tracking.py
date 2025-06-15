from flask import Blueprint

bp = Blueprint('tracking', __name__)

@bp.route('/ping')
def ping():
    return 'pong-tracking'
