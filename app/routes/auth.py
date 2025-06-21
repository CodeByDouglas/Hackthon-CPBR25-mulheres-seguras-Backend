from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import db
from app.models.user import User
from app.models.contact import Contact
import secrets

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        # Validação dos dados obrigatórios do usuário
        required_fields = ["nome", "cpf", "email", "password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo {field} é obrigatório"}), 400

        # Validação do contato inicial
        if "contact" not in data:
            return (
                jsonify(
                    {
                        "error": "É necessário fornecer pelo menos um contato de emergência"
                    }
                ),
                400,
            )

        contact_data = data["contact"]
        contact_required_fields = ["nome", "telefone"]
        for field in contact_required_fields:
            if field not in contact_data:
                return (
                    jsonify({"error": f"Campo {field} é obrigatório no contato"}),
                    400,
                )

        # Verifica se email ou CPF já existem
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email já cadastrado"}), 400
        if User.query.filter_by(cpf=data["cpf"]).first():
            return jsonify({"error": "CPF já cadastrado"}), 400

        # Gera token NFC único
        token_nfc = secrets.token_hex(32)

        # Cria o usuário
        user = User(
            nome=data["nome"],
            cpf=data["cpf"],
            email=data["email"],
            password=generate_password_hash(data["password"]),
            token_nfc=token_nfc,
            photo=data.get("photo"),  # opcional
        )
        db.session.add(user)
        db.session.flush()  # Garante que user.id está disponível
        # Cria o contato
        contact = Contact(
            nome=contact_data["nome"],
            telefone=contact_data["telefone"],
            email=contact_data.get("email"),  # opcional
            user_id=user.id,
        )

        # Salva no banco
        db.session.add(contact)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Usuário cadastrado com sucesso",
                    "user": {
                        "id": user.id,
                        "nome": user.nome,
                        "email": user.email,
                        "token_nfc": user.token_nfc,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        # Validação dos dados obrigatórios
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        # Busca o usuário pelo email
        user = User.query.filter_by(email=data["email"]).first()

        # Verifica se o usuário existe e se a senha está correta
        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Email ou senha inválidos"}), 401

        # Faz o login do usuário
        login_user(user)

        return (
            jsonify(
                {
                    "message": "Login realizado com sucesso",
                    "user": {
                        "id": user.id,
                        "nome": user.nome,
                        "email": user.email,
                        "token_nfc": user.token_nfc,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
