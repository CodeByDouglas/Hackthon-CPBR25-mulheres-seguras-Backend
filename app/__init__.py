# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from datetime import datetime
from app.models.database import db

# Inicialização das extensões
login_manager = LoginManager()
scheduler = APScheduler()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Configuração do app
    app.config.from_mapping({
        'SECRET_KEY': 'uma-chave-secreta-aqui',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///database.db',
        'SCHEDULER_API_ENABLED': True
    })

    # Inicialização das extensões com o app
    db.init_app(app)
    login_manager.init_app(app)
    scheduler.init_app(app)

    # Configuração do user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Importação dos blueprints
    with app.app_context():
        from app.routes.auth import bp as auth_bp
        from app.routes.users import bp as users_bp
        from app.routes.tracking import bp as contacts_bp
        from app.routes.emergency import bp as emergency_bp

        # Registro dos blueprints
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(users_bp, url_prefix='/users')
        app.register_blueprint(contacts_bp, url_prefix='/contacts')
        app.register_blueprint(emergency_bp, url_prefix='/emergency')

    return app
