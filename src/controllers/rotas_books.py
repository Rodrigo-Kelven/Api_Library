from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.config_db import get_db
from schemas.books import Book, BookCreate
from service.services import BooksServices

routes_books = APIRouter()

@routes_books.post("/books/", response_model=Book)
async def create_item(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await BooksServices.create_book(book, db)


@routes_books.get("/books/{item_id}", response_model=Book)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_book(item_id, db)


@routes_books.put("/books/{item_id}", response_model=Book)
async def update_item(item_id: int, item: BookCreate, db: AsyncSession = Depends(get_db)):
    return await BooksServices.update_book(item_id, item, db)


@routes_books.delete("/books/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await BooksServices.delete_book(item_id, db)


@routes_books.get("/books/", response_model=list[Book])
async def read_items(db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_all_books(db)