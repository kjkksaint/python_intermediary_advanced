from flask_login import UserMixin
from .banco import db, session
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
import datetime
import logging

logger = logging.getLogger(__name__)

class Consulta(db.Model):
    __tablename__ = 'consultas'
    id = Column(Integer, primary_key=True)
    cpf = Column(String(20), nullable=False)
    nome = Column(String(200))
    margem = Column(Float)
    conta = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.utcnow)
    raw = Column(Text)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # salve hash em produção

    @staticmethod
    def get_by_id(uid):
        return session.query(User).filter_by(id=int(uid)).first()

    @staticmethod
    def authenticate(username, password):
        # Para demo: compara plaintext. Troque por hashing (bcrypt).
        u = session.query(User).filter_by(username=username).first()
        if u and u.password == password:
            return u
        return None
