import argparse
import random
from datetime import datetime, timedelta
from app import create_app
from app.models.database import db
from app.models.user import User
from app.models.emergency_call import EmergencyCall
from werkzeug.security import generate_password_hash

# --- Funções de Geração de Dados ---


def create_base_user():
    """Cria um usuário base para testes se ele não existir."""
    user = User.query.filter_by(email="maria@teste.com").first()
    if not user:
        user = User(
            nome="Maria Silva",
            cpf="123.456.789-00",
            email="maria@teste.com",
            password=generate_password_hash("senha123"),
            photo="static/img/2842c52d6ea675991dd4f1df2448327e.jpg",
            token_nfc="TOKEN_TESTE_123",
        )
        db.session.add(user)
        print("✅ Usuário base 'Maria Silva' criado.")
        return user
    print("ℹ️ Usuário base 'Maria Silva' já existe.")
    return user


def clear_all_data():
    """Limpa todas as tabelas do banco de dados."""
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f"Limpando tabela: {table.name}")
        db.session.execute(table.delete())
    db.session.commit()
    print("✅ Todas as tabelas foram limpas.")


def populate_brasilia_heatmap(user, num_calls=20, max_points=15):
    """Cria múltiplos chamados de emergência em Brasília para o mapa de calor."""
    LAT_MIN, LAT_MAX = -16.05, -15.50
    LON_MIN, LON_MAX = -48.25, -47.30

    def generate_point():
        lat = random.uniform(LAT_MIN, LAT_MAX)
        lng = random.uniform(LON_MIN, LON_MAX)
        return {"lat": lat, "lng": lng}

    print(f"Gerando {num_calls} chamados na região de Brasília...")
    for _ in range(num_calls):
        route = [generate_point() for _ in range(random.randint(5, max_points))]
        last_location = f"{route[-1]['lat']},{route[-1]['lng']}"
        start_dt = datetime.utcnow() - timedelta(days=random.randint(0, 30))

        new_call = EmergencyCall(
            user_id=user.id,
            status="Encerrado",
            route=route,
            token_nfc=user.token_nfc,
            localizacao_atual=last_location,
            date=start_dt.date(),
            start_time=start_dt.time(),
            end_time=(start_dt + timedelta(minutes=random.randint(5, 60))).time(),
        )
        db.session.add(new_call)
    print(f"✅ {num_calls} chamados de mock criados.")


# --- Lógica Principal do Script ---


def main():
    parser = argparse.ArgumentParser(
        description="Gerencia dados de teste no banco de dados."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Executa todas as ações: limpa, cria usuário e popula o heatmap.",
    )
    parser.add_argument(
        "--clear", action="store_true", help="Limpa todos os dados do banco."
    )
    parser.add_argument(
        "--heatmap",
        action="store_true",
        help="Popula o banco com dados para o heatmap de Brasília.",
    )

    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        if args.all:
            clear_all_data()
            db.create_all()  # Recria as tabelas
            user = create_base_user()
            populate_brasilia_heatmap(user)

        elif args.clear:
            clear_all_data()

        elif args.heatmap:
            user = User.query.filter_by(email="maria@teste.com").first()
            if not user:
                print("Usuário base não encontrado. Criando um novo...")
                user = create_base_user()
            populate_brasilia_heatmap(user)

        else:
            print("Nenhuma ação especificada. Use --help para ver as opções.")
            return

        db.session.commit()
        print("\nOperação concluída com sucesso!")


if __name__ == "__main__":
    main()
