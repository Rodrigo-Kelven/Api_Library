from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookBase(BaseModel):
    title: str = Field(..., title="Title of the book", description="Titulo do livro", max_length=255)
    description: Optional[str] = Field(None, title="Description of the book", description="Descricao do livro")
    author: str = Field(..., title="Author of the book", description="autor do livro", max_length=255)
    category: str = Field(..., title="Category of the book", description="Categoria do livro" ,max_length=100)
    isbn: Optional[str] = Field(None, title="ISBN of the book", description="Número Padrão Internacional de Livro", max_length=13)
    publication_date: Optional[date] = Field(None, title="Publication date of the book", description="data de publicacao do livro")
    pages: Optional[int] = Field(None, title="Number of pages in the book", description="paginas totais do livro" ,ge=1)
    available: bool = Field(True, title="Availability status of the book", description="avalicao do livro, STARS")

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    pages: Optional[int] = None
    available: Optional[bool] = None

class Book(BookBase):
    id: int = Field(..., title="Unique identifier for the book", description="Id do livro")

    class Config:
        orm_mode = True