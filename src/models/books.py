from sqlalchemy import Column, Integer, String, Boolean, Date
from config.config_db import Base_books as Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)
    isbn = Column(String(13), nullable=True)  # ISBN pode ter até 13 caracteres
    publication_date = Column(Date, nullable=True)
    pages = Column(Integer, nullable=True)  # Número de páginas
    available = Column(Boolean, default=True)  # Disponibilidade do livro

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', available={self.available})>"