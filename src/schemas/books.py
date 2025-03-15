from pydantic import BaseModel
from typing import  Optional


# Schema para o livro
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    author: str
    category: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
