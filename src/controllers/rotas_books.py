from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.config_db import get_db
from src.schemas.books import Book, BookCreate, BookUpdate
from src.service.services import BooksServices


routes_books = APIRouter()


# somente admin podem ter acesso
@routes_books.post(
        path="/books/",
        status_code=status.HTTP_201_CREATED,
        description="Route for register of books",
        name="Route register books",
        response_model=Book
        )
async def create_item(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await BooksServices.create_book(book, db)


# adicionar pesquisa por: author, nome, titulo, categoria, lingua, quantidade de paginas
@routes_books.get(
        path="/books/{book_id}",
        status_code=status.HTTP_200_OK,
        description="Route for search books of ID",
        name="Route search book for id",
        response_model=Book,
        )
async def read_item(book_id: int, db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_book(book_id, db)


# somente admin podem ter acesso
@routes_books.put(
        path="/books/{book_id}",
        status_code=status.HTTP_201_CREATED,
        description="Route update book for ID",
        name="Route update books",
        response_model=Book
        )
async def update_item(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    return await BooksServices.update_book(book_id, book, db)

# somente admin podem ter acesso
@routes_books.delete(
        path="/books/{book_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        description="Router delete book for ID",
        name="Route delete book",
        )
async def delete_item(book_id: int, db: AsyncSession = Depends(get_db)):
    return await BooksServices.delete_book(book_id, db)


# implementar limite de busca EX: limit 100, para evitar pesquisas repetitivas no DB, 
# causando repeticao de conexoes e gargalo 
# implementar juntamente com pagination no front
# possivel implementacao de Redis
@routes_books.get(
        path="/books-search-limit/",
        status_code=status.HTTP_200_OK,
        description="Router view  books with limit in db",
        name="Router get all books with limit",
        response_model=list[Book]
        )
async def read_items(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20
    ):
    return await BooksServices.get_all_with_limit_books(db, skip=skip, limit=limit)


@routes_books.get(
        path="/books/",
        status_code=status.HTTP_200_OK,
        description="Router view all books  in db",
        name="Router get all books",
        response_model=list[Book]
        )
async def read_items(db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_all_books(db)



@routes_books.get(
    path="/books/search-filters/",
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    description="List search with query books",
    name="Route search with query books"
    )
async def read_books(
    title: Optional[str] = Query(None, description="Filtrar por título"),
    author: Optional[str] = Query(None, description="Filtrar por autor"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    min_pages: Optional[int] = Query(None, description="Filtrar por número mínimo de páginas"),
    max_pages: Optional[int] = Query(None, description="Filtrar por número máximo de páginas"),
    available: Optional[bool] = Query(None, description="Filtrar por disponibilidade"),
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
    ):

    return await BooksServices.get_filtered_books(
        db, title=title, author=author,
        category=category, min_pages=min_pages,
        max_pages=max_pages,
        available=available,
        skip=skip,
        limit=limit
        )