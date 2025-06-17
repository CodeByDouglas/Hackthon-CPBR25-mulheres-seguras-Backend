from flask import Blueprint, render_template
from app.models.user import User

bp = Blueprint('emergency', __name__)

@bp.route('/ping')
def ping():
    return 'pong-emergency'

@bp.route('/nfc/<token>')
def confirm_emergency(token):
    # Busca o usuário pelo token NFC
    user = User.query.filter_by(token_nfc=token).first()
    
    if not user:
        return "Token NFC inválido", 404
    
    # Renderiza a página de confirmação
    return render_template('confirm_emergency.html')
