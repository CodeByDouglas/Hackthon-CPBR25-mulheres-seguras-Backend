# app/models/contact.py
from app.models.database import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Contact(db.Model):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(120))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Contact {self.nome}>'
