# app/models/contact.py
from app.models.base import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Contact {self.nome}>'
