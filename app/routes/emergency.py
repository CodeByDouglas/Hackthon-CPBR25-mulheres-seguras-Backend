from flask import Blueprint, render_template, request, jsonify
from app.models.database import db
from app.models.user import User
from app.models.emergency_call import EmergencyCall
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime

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

@bp.route('/confirm/<token>', methods=['POST'])
def create_emergency(token):
    # Busca o usuário pelo token NFC
    user = User.query.filter_by(token_nfc=token).first()
    
    if not user:
        return jsonify({"success": False, "error": "Token NFC inválido"}), 404
    
    # Verifica se já existe um chamado ativo
    active_call = EmergencyCall.query.filter_by(
        user_id=user.id,
        status="Ativo"
    ).first()
    
    if active_call:
        return jsonify({"success": False, "error": "Já existe um chamado ativo para este usuário"}), 400
    
    # Cria um novo chamado de emergência
    new_call = EmergencyCall(
        user_id=user.id,
        status="Ativo",
        route=[],
        token_nfc=token,
        localizacao_atual=None
    )
    
    try:
        db.session.add(new_call)
        db.session.commit()
        return jsonify({
            "success": True,
            "call_id": new_call.id,
            "message": "Chamado de emergência criado com sucesso"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Erro ao criar chamado: {str(e)}"}), 500

@bp.route('/abort/<token>', methods=['POST'])
def abort_emergency(token):
    # Busca o usuário pelo token NFC
    user = User.query.filter_by(token_nfc=token).first()
    
    if not user:
        return jsonify({"success": False, "error": "Token NFC inválido"}), 404
    
    # Busca o chamado ativo
    active_call = EmergencyCall.query.filter_by(
        user_id=user.id,
        status="Ativo"
    ).first()
    
    if not active_call:
        return jsonify({"success": False, "error": "Não há chamado ativo para este usuário"}), 404
    
    # Atualiza o status do chamado
    active_call.status = "Abortado"
    active_call.data_fim = datetime.now()
    
    try:
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Chamado abortado com sucesso"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Erro ao abortar chamado: {str(e)}"}), 500

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

@bp.route('/success/active')
def emergency_active_page():
    return render_template('emergency_active.html')

@bp.route('/success/aborted')
def emergency_aborted_page():
    return render_template('emergency_aborted.html')

@bp.route('/close-call', methods=['POST'])
def close_call():
    data = request.get_json()
    token_nfc = data.get('token_nfc')
    if not token_nfc:
        return jsonify({"success": False, "error": "Token NFC não fornecido"}), 400

    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return jsonify({"success": False, "error": "Usuário não encontrado para o token informado"}), 404

    active_call = EmergencyCall.query.filter_by(user_id=user.id, status="Ativo").first()
    if not active_call:
        return jsonify({"success": False, "error": "Nenhum chamado ativo encontrado para este usuário"}), 404

    active_call.status = "Encerrado"
    active_call.end_time = datetime.now().time()
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Chamado encerrado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Erro ao encerrar chamado: {str(e)}"}), 500

@bp.route('/add-contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    token_nfc = data.get('token_nfc')
    contact_data = data.get('contact')
    if not token_nfc or not contact_data:
        return jsonify({"success": False, "error": "Token NFC e dados do contato são obrigatórios"}), 400

    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return jsonify({"success": False, "error": "Usuário não encontrado para o token informado"}), 404

    from app.models.contact import Contact
    new_contact = Contact(
        user_id=user.id,
        nome=contact_data.get('nome'),
        telefone=contact_data.get('telefone'),
        email=contact_data.get('email')
    )
    try:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"success": True, "message": "Contato cadastrado com sucesso", "contact_id": new_contact.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Erro ao cadastrar contato: {str(e)}"}), 500
