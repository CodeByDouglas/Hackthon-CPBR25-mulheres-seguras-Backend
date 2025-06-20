from flask import Blueprint, render_template, request, jsonify
from app.models.database import db
from app.models.user import User
from app.models.emergency_call import EmergencyCall
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime
from app.services.twilio_service import enviar_sms
from app.models.contact import Contact

bp = Blueprint("emergency", __name__)


@bp.route("/ping")
def ping():
    """Endpoint de teste para verificar se o serviço está online."""

    return "pong-emergency"


@bp.route("/nfc/<token>")
def confirm_emergency(token):
    """Renderiza a página de confirmação de emergência ao receber um token NFC válido."""

    user = User.query.filter_by(token_nfc=token).first()
    if not user:
        return "Token NFC inválido", 404
    return render_template("confirm_emergency.html")


@bp.route("/confirm/<token>", methods=["POST"])
def create_emergency(token):
    """Cria um novo chamado de emergência ativo para o usuário do token NFC recebido."""

    user = User.query.filter_by(token_nfc=token).first()
    if not user:
        return jsonify({"success": False, "error": "Token NFC inválido"}), 404
    active_call = EmergencyCall.query.filter_by(user_id=user.id, status="Ativo").first()
    if active_call:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Já existe um chamado ativo para este usuário",
                }
            ),
            400,
        )
    new_call = EmergencyCall(
        user_id=user.id,
        status="Ativo",
        route=[],
        token_nfc=token,
        localizacao_atual=None,
    )
    try:
        db.session.add(new_call)
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "call_id": new_call.id,
                    "message": "Chamado de emergência criado com sucesso",
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": f"Erro ao criar chamado: {str(e)}"}),
            500,
        )


@bp.route("/abort/<token>", methods=["POST"])
def abort_emergency(token):
    """Aborta o chamado de emergência ativo do usuário do token NFC recebido."""

    user = User.query.filter_by(token_nfc=token).first()
    if not user:
        return jsonify({"success": False, "error": "Token NFC inválido"}), 404
    active_call = EmergencyCall.query.filter_by(user_id=user.id, status="Ativo").first()
    if not active_call:
        return (
            jsonify(
                {"success": False, "error": "Não há chamado ativo para este usuário"}
            ),
            404,
        )
    active_call.status = "Abortado"
    active_call.data_fim = datetime.now()
    try:
        db.session.commit()
        return (
            jsonify({"success": True, "message": "Chamado abortado com sucesso"}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": f"Erro ao abortar chamado: {str(e)}"}),
            500,
        )


@bp.route("/update-location", methods=["POST"])
def update_location():
    """Atualiza a localização do usuário durante um chamado ativo."""

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    token_nfc = data.get("token_nfc")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    if not all([token_nfc, latitude, longitude]):
        return (
            jsonify({"error": "Token NFC, latitude e longitude são obrigatórios"}),
            400,
        )
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({"error": "Latitude e longitude devem ser números"}), 400
    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    active_call = EmergencyCall.query.filter_by(user_id=user.id, status="Ativo").first()
    if not active_call:
        return jsonify({"error": "Não há chamado ativo para este usuário"}), 404
    new_location = {"lat": latitude, "lng": longitude}
    if not active_call.route or active_call.route[-1] != new_location:
        active_call.route.append(new_location)
        flag_modified(active_call, "route")
    active_call.localizacao_atual = f"{latitude},{longitude}"
    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Localização atualizada com sucesso",
                    "call_id": active_call.id,
                    "route_length": len(active_call.route),
                    "current_location": new_location,
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar localização: {str(e)}"}), 500


@bp.route("/success/active")
def emergency_active_page():
    """Renderiza a página de sucesso para chamado de emergência ativo."""

    return render_template("emergency_active.html")


@bp.route("/success/aborted")
def emergency_aborted_page():
    """Renderiza a página de sucesso para chamado de emergência abortado."""

    return render_template("emergency_aborted.html")


@bp.route("/close-call", methods=["POST"])
def close_call():
    """Encerra o chamado ativo do usuário identificado pelo token NFC recebido."""

    data = request.get_json()
    token_nfc = data.get("token_nfc")
    if not token_nfc:
        return jsonify({"success": False, "error": "Token NFC não fornecido"}), 400
    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Usuário não encontrado para o token informado",
                }
            ),
            404,
        )
    active_call = EmergencyCall.query.filter_by(user_id=user.id, status="Ativo").first()
    if not active_call:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Nenhum chamado ativo encontrado para este usuário",
                }
            ),
            404,
        )
    active_call.status = "Encerrado"
    active_call.end_time = datetime.now().time()
    try:
        db.session.commit()
        return (
            jsonify({"success": True, "message": "Chamado encerrado com sucesso"}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": f"Erro ao encerrar chamado: {str(e)}"}),
            500,
        )


@bp.route("/add-contact", methods=["POST"])
def add_contact():
    """Cadastra um novo contato de emergência vinculado ao usuário do token NFC recebido."""

    data = request.get_json()
    token_nfc = data.get("token_nfc")
    contact_data = data.get("contact")
    if not token_nfc or not contact_data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Token NFC e dados do contato são obrigatórios",
                }
            ),
            400,
        )
    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Usuário não encontrado para o token informado",
                }
            ),
            404,
        )
    new_contact = Contact(
        user_id=user.id,
        nome=contact_data.get("nome"),
        telefone=contact_data.get("telefone"),
        email=contact_data.get("email"),
    )
    try:
        db.session.add(new_contact)
        db.session.commit()
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Contato cadastrado com sucesso",
                    "contact_id": new_contact.id,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {"success": False, "error": f"Erro ao cadastrar contato: {str(e)}"}
            ),
            500,
        )


@bp.route("/delete-contact/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    """Remove um contato de emergência pelo ID."""

    contact = Contact.query.get(contact_id)
    if not contact:
        return jsonify({"success": False, "error": "Contato não encontrado"}), 404

    try:
        db.session.delete(contact)
        db.session.commit()
        return (
            jsonify({"success": True, "message": "Contato removido com sucesso"}),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": f"Erro ao remover contato: {str(e)}"}),
            500,
        )


@bp.route("/calls/<token_nfc>", methods=["GET"])
def get_user_calls(token_nfc):
    """Retorna todos os chamados do usuário do token NFC informado e indica se há algum chamado ativo."""

    user = User.query.filter_by(token_nfc=token_nfc).first()
    if not user:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Usuário não encontrado para o token informado",
                }
            ),
            404,
        )
    calls = EmergencyCall.query.filter_by(user_id=user.id).all()
    calls_list = [
        {
            "id": call.id,
            "status": call.status,
            "date": str(call.date),
            "start_time": str(call.start_time),
            "end_time": str(call.end_time) if call.end_time else None,
            "route": call.route,
            "token_nfc": call.token_nfc,
            "localizacao_atual": call.localizacao_atual,
        }
        for call in calls
    ]
    has_active = any(call.status == "Ativo" for call in calls)
    return (
        jsonify({"success": True, "calls": calls_list, "has_active": has_active}),
        200,
    )


@bp.route("/nfc/auto/<token>", methods=["GET"])
def auto_emergency(token):
    """
    Cria um chamado de emergência imediatamente ao receber o token NFC e envia SMS para todos os contatos de emergência do usuário.
    Pode receber latitude e longitude como parâmetros de query string para salvar a localização inicial.
    """
    # Pega coordenadas da query string (opcional)
    latitude = request.args.get("lat")
    longitude = request.args.get("lng")

    user = User.query.filter_by(token_nfc=token).first()
    if not user:
        return jsonify({"success": False, "error": "Token NFC inválido"}), 404

    active_call = EmergencyCall.query.filter_by(user_id=user.id, status="Ativo").first()
    if active_call:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Já existe um chamado ativo para este usuário",
                }
            ),
            400,
        )

    # Prepara dados de localização se fornecidos
    route = []
    localizacao_atual = None
    if latitude and longitude:
        try:
            lat = float(latitude)
            lng = float(longitude)
            route = [{"lat": lat, "lng": lng}]
            localizacao_atual = f"{lat},{lng}"
        except ValueError:
            return (
                jsonify({"error": "Latitude e longitude devem ser números válidos"}),
                400,
            )

    new_call = EmergencyCall(
        user_id=user.id,
        status="Ativo",
        route=route,
        token_nfc=token,
        localizacao_atual=localizacao_atual,
    )

    try:
        db.session.add(new_call)
        db.session.commit()
        call_id = new_call.id

        # Busca contatos de emergência
        contatos = Contact.query.filter_by(user_id=user.id).all()
        # Monta e envia SMS para cada contato
        sms_errors = []
        for contato in contatos:
            link = f"https://8b18-190-103-168-170.ngrok-free.app/{token}/{call_id}"
            mensagem = f"ALERTA! {user.nome} precisa de ajuda. Acesse: {link}"
            try:
                enviar_sms(contato.telefone, mensagem)
            except Exception as e:
                error_msg = f"Erro ao enviar SMS para {contato.telefone}: {str(e)}"
                sms_errors.append(error_msg)
                print(error_msg)

        if sms_errors:
            return (
                jsonify(
                    {
                        "success": False,
                        "call_id": call_id,
                        "message": "Chamado criado mas houve erros no envio de SMS",
                        "sms_errors": sms_errors,
                    }
                ),
                201,
            )

        return (
            jsonify(
                {
                    "success": True,
                    "call_id": call_id,
                    "message": "Chamado de emergência criado e SMS enviados com sucesso",
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"success": False, "error": f"Erro ao criar chamado: {str(e)}"}),
            500,
        )


@bp.route("/heatmap", methods=["GET"])
def heatmap_page():
    """
    Renderiza uma página com um mapa de calor mostrando a frequência de chamados
    por localização, utilizando os dados de rota de todos os chamados.
    """
    try:
        # Busca todos os chamados que possuem rotas
        calls_with_routes = EmergencyCall.query.filter(
            EmergencyCall.route != None
        ).all()

        # Extrai todos os pontos de coordenadas de todas as rotas
        all_points = []
        for call in calls_with_routes:
            if call.route:  # Garante que a rota não está vazia
                # O formato esperado é (lat, lng, intensity)
                # Adicionamos uma intensidade padrão de 1.0 para cada ponto
                points = [
                    [point["lat"], point["lng"], 1.0]
                    for point in call.route
                    if "lat" in point and "lng" in point
                ]
                all_points.extend(points)

        # Renderiza o template, passando os pontos de calor
        return render_template("heatmap.html", heat_points=all_points)

    except Exception as e:
        # Em caso de erro, retorna uma mensagem amigável
        return f"Ocorreu um erro ao gerar o mapa de calor: {str(e)}", 500
