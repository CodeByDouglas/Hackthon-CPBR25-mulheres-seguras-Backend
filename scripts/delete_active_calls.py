from app import create_app
from app.models.emergency_call import EmergencyCall
from app.models.database import db

app = create_app()
with app.app_context():
    deleted = EmergencyCall.query.filter_by(status="Ativo").delete()
    db.session.commit()
    print(f"Chamados ativos excluídos: {deleted}")
