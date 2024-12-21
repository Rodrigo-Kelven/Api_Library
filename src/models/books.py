from typing import Optional
from sqlmodel import SQLModel, Field
#from pydantic import BaseModel

# Model de Book
class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Correção aqui
    nome: str = Field(..., alias="Nome")
    titulo: str = Field(..., alias="Titulo")
    categoria: str = Field(..., alias="Categoria")
    paginas: int = Field(..., alias="Paginas")
    autor: str = Field(..., alias="Autor")
    ano_publicacao: int = Field(..., alias="AnoPublicacao")
    editora: Optional[str] = Field(None, alias="Editora") 
    descricao: Optional[str] = Field(None, alias="Descricao")
    isbn: Optional[str] = Field(None, alias="ISBN")
    lingua: str = Field(..., alias="Lingua")
    

# Models de reposta de Book
class ResponseBook(SQLModel):
    nome: str = Field(..., alias="Nome")
    titulo: str = Field(..., alias="Titulo")
    categoria: str = Field(..., alias="Categoria")
    paginas: int = Field(..., alias="Paginas")
    autor: str = Field(..., alias="Autor")
    ano_publicacao: int = Field(..., alias="AnoPublicacao")
    editora: Optional[str] = Field(None, alias="Editora")
    descricao: Optional[str] = Field(None, alias="Descricao")
    isbn: Optional[str] = Field(None, alias="ISBN")
    lingua: str = Field(..., alias="Lingua")