from flask import Blueprint

bp = Blueprint('emergency', __name__)

@bp.route('/ping')
def ping():
    return 'pong-emergency'
