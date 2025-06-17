from flask import Blueprint, render_template, request, jsonify
from app.models.database import db
from app.models.user import User
from app.models.emergency_call import EmergencyCall
from sqlalchemy.orm.attributes import flag_modified

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

@bp.route('/update-location', methods=['POST'])
def update_location():
    # Obtém os dados da requisição
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    token_nfc = data.get('token_nfc')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Valida os dados recebidos
    if not all([token_nfc, latitude, longitude]):
        return jsonify({"error": "Token NFC, latitude e longitude são obrigatórios"}), 400
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({"error": "Latitude e longitude devem ser números"}), 400
    
    # Busca o usuário pelo token NFC
    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    # Busca o chamado ativo do usuário
    active_call = EmergencyCall.query.filter_by(
        user_id=user.id,
        status="Ativo"
    ).first()
    
    if not active_call:
        return jsonify({"error": "Não há chamado ativo para este usuário"}), 404
    
    # Atualiza a rota com a nova localização
    new_location = {"lat": latitude, "lng": longitude}
    
    # Se a rota estiver vazia ou a última localização for diferente, adiciona o novo ponto
    if not active_call.route or active_call.route[-1] != new_location:
        active_call.route.append(new_location)
        flag_modified(active_call, "route")
    
    # Atualiza a localização atual
    active_call.localizacao_atual = f"{latitude},{longitude}"
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Localização atualizada com sucesso",
            "call_id": active_call.id,
            "route_length": len(active_call.route),
            "current_location": new_location
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar localização: {str(e)}"}), 500
