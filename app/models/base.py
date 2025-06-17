# app/models/base.py
from app.models.database import db

# Função auxiliar para criar todos os modelos
def init_models():
    from app.models.user import User
    from app.models.contact import Contact
    from app.models.emergency_call import EmergencyCall
    return User, Contact, EmergencyCall 