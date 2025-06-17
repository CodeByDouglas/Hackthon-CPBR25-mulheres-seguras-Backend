# app/models/base.py
from app import db

# Importação dos modelos
from app.models.user import User
from app.models.contact import Contact
from app.models.emergency_call import EmergencyCall

# Função auxiliar para criar todos os modelos
def init_models():
    return User, Contact, EmergencyCall 