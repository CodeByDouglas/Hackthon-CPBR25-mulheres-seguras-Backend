from app.models.base import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

class EmergencyCall(db.Model):
    __tablename__ = 'emergency_call'

    # PK
    id = Column(Integer, primary_key=True)

    # status do chamado: 'Ativo' ou 'Encerrado'
    status = Column(String(20), nullable=False, default='Ativo')

    # data do chamado
    date = Column(Date, nullable=False, default=lambda: datetime.utcnow().date())

    # horário de início
    start_time = Column(Time, nullable=False, default=lambda: datetime.utcnow().time())

    # horário de fim (pode ficar nulo até o encerramento)
    end_time = Column(Time, nullable=True)

    # rota: lista de [lat, lng], armazenada como JSON
    route = Column(db.JSON, nullable=False, default=list)

    # token NFC relacionado ao chamado
    token_nfc = Column(String(64), nullable=True)

    # última localização recebida
    localizacao_atual = Column(String(200), nullable=True)

    # relação com o usuário que abriu o chamado
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='calls')

    def __repr__(self):
        return f'<EmergencyCall {self.id} - {self.status}>'
