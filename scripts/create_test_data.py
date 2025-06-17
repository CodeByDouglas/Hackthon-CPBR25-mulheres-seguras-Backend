from app import create_app
from app.models.database import db
from app.models.user import User
from app.models.emergency_call import EmergencyCall
from datetime import datetime

def create_test_data():
    app = create_app()
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()

        # Criar usuário de teste
        user = User(
            nome="Maria Silva",
            cpf="123.456.789-00",
            email="maria@teste.com",
            password="senha123",
            photo="https://via.placeholder.com/150",
            token_nfc="TOKEN_TESTE_123"
        )
        db.session.add(user)
        db.session.commit()

        # Criar chamado de emergência ATIVO
        emergency_call_active = EmergencyCall(
            status="Ativo",
            date=datetime.utcnow().date(),
            start_time=datetime.utcnow().time(),
            route=[
                {"lat": -23.550520, "lng": -46.633308},  # São Paulo
                {"lat": -23.550520, "lng": -46.633308},  # Mesma localização para teste
            ],
            token_nfc="TOKEN_TESTE_123",
            localizacao_atual="-23.550520,-46.633308",
            user_id=user.id
        )
        db.session.add(emergency_call_active)

        # Criar chamado de emergência ENCERRADO
        emergency_call_closed = EmergencyCall(
            status="Encerrado",
            date=datetime.utcnow().date(),
            start_time=datetime.utcnow().time(),
            end_time=datetime.utcnow().time(),
            route=[
                {"lat": -23.550520, "lng": -46.633308},  # São Paulo
            ],
            token_nfc="TOKEN_TESTE_123",
            localizacao_atual="-23.550520,-46.633308",
            user_id=user.id
        )
        db.session.add(emergency_call_closed)
        db.session.commit()

        print("Dados de teste criados com sucesso!")
        print(f"ID do usuário: {user.id}")
        print(f"ID do chamado ATIVO: {emergency_call_active.id}")
        print(f"ID do chamado ENCERRADO: {emergency_call_closed.id}")
        print(f"Token NFC: {user.token_nfc}")

if __name__ == "__main__":
    create_test_data() 