from sqlalchemy import Column, Integer, String
from config.config_db import Base_books as Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)