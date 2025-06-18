from app import create_app, db
from app.models.user import User
from app.models.emergency_call import EmergencyCall

app = create_app()

def check_route():
    active_call = EmergencyCall.query.filter_by(status="Ativo").first()
    if active_call:
        print(f"ID do chamado: {active_call.id}")
        print(f"Status: {active_call.status}")
        print(f"Localização atual: {active_call.localizacao_atual}")
        print("Rota completa:")
        for point in active_call.route:
            print(f"  - {point}")
    else:
        print("Nenhum chamado ativo encontrado")

if __name__ == "__main__":
    with app.app_context():
        check_route()
        user = User.query.filter_by(token_nfc='TOKEN TESTE_123').first()
        if user:
            print(f'Token antigo: {user.token_nfc}')
            user.token_nfc = 'TOKEN_TESTE_123'
            db.session.commit()
            print(f'Token atualizado: {user.token_nfc}')
        else:
            print('Usuário com token antigo não encontrado.') 