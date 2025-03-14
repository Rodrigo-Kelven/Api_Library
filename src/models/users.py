from sqlalchemy import Column, Integer, String
from config.config_db import Base

class User(Base):
    __tablename__ = 'users'  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # ID do usuário
    username = Column(String, unique=True, index=True)  # Nome de usuário único
    email = Column(String, unique=True, index=True)  # Email único
    password = Column(String)  # Senha (deve ser armazenada de forma segura)

    def __repr__(self):
        return f"<User (id={self.id}, username={self.username}, email={self.email})>"