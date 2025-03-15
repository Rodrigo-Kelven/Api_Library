from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookBase(BaseModel):
    title: str = Field(..., title="Title of the book", max_length=255)
    description: Optional[str] = Field(None, title="Description of the book")
    author: str = Field(..., title="Author of the book", max_length=255)
    category: str = Field(..., title="Category of the book", max_length=100)
    isbn: Optional[str] = Field(None, title="ISBN of the book", max_length=13)
    publication_date: Optional[date] = Field(None, title="Publication date of the book")
    pages: Optional[int] = Field(None, title="Number of pages in the book", ge=1)
    available: bool = Field(True, title="Availability status of the book")

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
    id: int = Field(..., title="Unique identifier for the book")

    class Config:
        orm_mode = True