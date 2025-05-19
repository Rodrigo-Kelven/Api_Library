from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from src.config.config_db import Base_books as Base



class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, doc="id do livro")
    title = Column(String, index=True, doc="titulo do livro")
    description = Column(String, nullable=True, doc="descricao do livro")
    author = Column(String, nullable=False, doc="autor do livro")
    category = Column(String, nullable=False, doc="categoria do livro")
    isbn = Column(String(13), nullable=True, doc="isbn do livro")  # ISBN pode ter até 13 caracteres
    publication_date = Column(Date, nullable=True, doc="data de publicacao do livro")
    pages = Column(Integer, nullable=True, doc="quantidade paginas do livro")  # Número de páginas
    available = Column(Boolean, default=True, doc="avaliacao do livro")  # Disponibilidade do livro

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.available})>"
    

# somente uma anotação sobre a criação das tabelas
# class Autor(Base):
#     __tablename__ = 'autores'
    
#     id = Column(Integer, primary_key=True)
#     nome = Column(String, nullable=False)
#     sobrenome = Column(String, nullable=False)

#     livros = relationship('Livro', back_populates='autor')


# class Usuario():
#     __tablename__ = 'usuarios'
    
#     id = Column(Integer, primary_key=True)
#     nome = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)

#     emprestimos = relationship('Emprestimo', back_populates='usuario')

# class Emprestimo(Base):
#     __tablename__ = 'emprestimos'
    
#     id = Column(Integer, primary_key=True)
#     livro_id = Column(Integer, ForeignKey('livros.id'))
#     usuario_id = Column(Integer, ForeignKey('usuarios.id'))
#     data_emprestimo = Column(Date)
#     data_devolucao = Column(Date)

#     livro = relationship('Livro', back_populates='emprestimos')
#     usuario = relationship('Usuario', back_populates='emprestimos')

"""
USANDO ALEMBIC
"""

"""
Create all tables

Revision ID: abc123def456
Revises: 
Create Date: 2023-10-01 12:00:00.000000

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Criação da tabela autores
    op.create_table(
        'autores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('sobrenome', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criação da tabela livros
    op.create_table(
        'livros',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(), nullable=False),
        sa.Column('ano_publicacao', sa.Integer(), nullable=True),
        sa.Column('autor_id', sa.Integer(), sa.ForeignKey('autores.id')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criação da tabela usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criação da tabela emprestimos
    op.create_table(
        'emprestimos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('livro_id', sa.Integer(), sa.ForeignKey('livros.id')),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id')),
        sa.Column('data_emprestimo', sa.Date(), nullable=True),
        sa.Column('data_devolucao', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('emprestimos')
    op.drop_table('usuarios')
    op.drop_table('livros')
    op.drop_table('autores')
"""