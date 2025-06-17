from flask import Blueprint, render_template
from app.models.user import User
from app.models.emergency_call import EmergencyCall

bp = Blueprint('tracking', __name__)

@bp.route('/<token_nfc>/<int:call_id>')
def tracking_page(token_nfc, call_id):
    # Busca o usuário pelo token NFC
    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return "Usuário não encontrado", 404

    # Busca o chamado de emergência
    emergency_call = EmergencyCall.query.get(call_id)
    if not emergency_call:
        return "Chamado não encontrado", 404

    # Verifica se o chamado pertence ao usuário
    if emergency_call.user_id != user.id:
        return "Acesso não autorizado", 403

    # Verifica se o chamado está ativo
    if emergency_call.status != "Ativo":
        return "Este chamado já foi encerrado", 403

    # Prepara os dados para o template
    last_location = None
    if emergency_call.route and len(emergency_call.route) > 0:
        last_location = emergency_call.route[-1]
    else:
        # Se não houver rota, usa a localização atual
        if emergency_call.localizacao_atual:
            lat, lng = emergency_call.localizacao_atual.split(',')
            last_location = {'lat': float(lat), 'lng': float(lng)}
        else:
            # Coordenadas padrão (Brasil)
            last_location = {'lat': -15.7801, 'lng': -47.9292}

    return render_template('tracking.html',
                         user=user,
                         last_location=last_location,
                         route=emergency_call.route)
