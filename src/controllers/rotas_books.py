from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.config_db import get_db
from schemas.books import Item, ItemCreate
from service.services import BooksServices

routes_books = APIRouter()

@routes_books.post("/items/", response_model=Item)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await BooksServices.create_book(item, db)


@routes_books.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_book(item_id, db)


@routes_books.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await BooksServices.update_book(item_id, item, db)


@routes_books.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await BooksServices.delete_book(item_id, db)


@routes_books.get("/items/", response_model=list[Item])
async def read_items(db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_all_books(db)