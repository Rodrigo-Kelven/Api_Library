from sqlalchemy import Column, Integer, String
from config.config_db import Base_books as Base

# se o nosql for usado, precisará refatorar, models, schemas, responses models, e write in databases


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    author = Column(String, nullable=False)
    category = Column(String, nullable=False)