# app/models/user.py
from app.models.database import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(200))  # caminho/URL da foto
    token_nfc = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relacionamentos, e.g. contatos de emergência:
    contacts = db.relationship("Contact", backref="owner", lazy=True)
    calls = db.relationship("EmergencyCall", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"
