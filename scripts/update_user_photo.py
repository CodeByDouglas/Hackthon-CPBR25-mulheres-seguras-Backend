from app import create_app
from app.models.user import User
from app.models.database import db

app = create_app()

with app.app_context():
    user = User.query.get(1)
    if user:
        user.photo = 'static/img/2842c52d6ea675991dd4f1df2448327e.jpg'
        db.session.commit()
        print('Foto atualizada com sucesso!')
    else:
        print('Usuário não encontrado.') 