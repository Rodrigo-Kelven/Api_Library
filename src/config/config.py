from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from typing import Generator

# configurações do banco de dados, cria dentro da pasta -> Bando_de_Dados automaticamente
sqlite_file_name_books = "Banco_de_Dados/database_books.db" # -> nome do db
sqlite_url_books = f"sqlite:///{sqlite_file_name_books}" # -> url do db


# Configuração da engine do SQLAlchemy para SQLite
connect_args = {"check_same_thread": False}
engine_books = create_engine(sqlite_url_books, connect_args=connect_args)

# Função para criar as tabelas no banco de dados
def create_db_and_tables_of_books():
    SQLModel.metadata.create_all(engine_books)

# Função para obter/fornecer a sessão de banco de dados 
def get_session_books() -> Generator[Session, None, None]:
    with Session(engine_books) as session:
        yield session


########################## Users #############################
sqlite_file_name_users = "Banco_de_Dados/database_users.db" # -> nome do db
sqlite_url_users = f"sqlite:///{sqlite_file_name_users}" # n-> url do db

# Configuração da engine do SQLAlchemy para SQLite
connect_args = {"check_same_thread": False}
engine_users = create_engine(sqlite_url_users, connect_args=connect_args)

# Função para criar as tabelas no banco de dados
def create_db_and_tables_of_users():
    SQLModel.metadata.create_all(engine_users)

# Função para obter/fornecer a sessão de banco de dados 
def get_session_users() -> Generator[Session, None, None]:
    with Session(engine_users) as session:
        yield session