from fastapi import APIRouter, Depends, status
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
        path="/books/",
        status_code=status.HTTP_200_OK,
        description="Router view all books in db",
        name="Router get all books",
        response_model=list[Book]
        )
async def read_items(db: AsyncSession = Depends(get_db)):
    return await BooksServices.get_all_books(db)