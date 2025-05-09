from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, Request
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import get_current_user
from src.config.config_db import get_db
from src.schemas.books import Book, BookCreate, BookUpdate
from src.service.services import BooksServices
from src.config.config import limiter


routes_books = APIRouter()


# somente admin podem ter acesso
@routes_books.post(
        path="/books/",
        status_code=status.HTTP_201_CREATED,
        description="Route for register of books",
        name="Route register books",
        response_model=Book
        )
@limiter.limit("20/minute") # O ideal é 5
async def create_item(
    request: Request,
    book: BookCreate,
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
    db: AsyncSession = Depends(get_db),
    ): 
    # realiza o registro do livro
    return await BooksServices.create_book_Service(book, db)


# adicionar pesquisa por: author, nome, titulo, categoria, lingua, quantidade de paginas
@routes_books.get(
        path="/books/{book_id}",
        status_code=status.HTTP_200_OK,
        description="Route for search books of ID",
        name="Route search book for id",
        response_model=Book,
        )
@limiter.limit("30/minute")  # Limite mais alto para um endpoint de busca mais específica
async def read_item(
    request: Request,
    book_id: int,
    db: AsyncSession = Depends(get_db)
    ):
    # realiza um get passando o id do livro
    return await BooksServices.get_book_Service(book_id, db)


# somente admin podem ter acesso
@routes_books.put(
        path="/books/{book_id}",
        status_code=status.HTTP_201_CREATED,
        description="Route update book for ID",
        name="Route update books",
        response_model=Book
        )
@limiter.limit("20/minute") # O ideal é 5
async def update_item(
    request: Request,
    book_id: int,
    book: BookUpdate,
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
    db: AsyncSession = Depends(get_db),
    ):
    # realiza update de livros com o id passado
    return await BooksServices.update_book_Service(book_id, book, db)

# somente admin podem ter acesso
@routes_books.delete(
        path="/books/{book_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        description="Router delete book for ID",
        name="Route delete book",
        )
@limiter.limit("10/minute")  # Limite de 10 requisições por minuto, o ideal é 2
async def delete_item(
    request: Request,
    book_id: int,
    current_user: str = Depends(get_current_user), # Garante que o usuário está autenticado):
    db: AsyncSession = Depends(get_db),
    ):
    # realiza delete of books
    return await BooksServices.delete_book_Service(book_id, db)


@routes_books.get(
        path="/books-search-limit/",
        status_code=status.HTTP_200_OK,
        description="Router view  books with limit in db",
        name="Router get all books with limit",
        response_model=list[Book]
        )
@limiter.limit("30/minute")  # Limite de 30 requisições por minuto
async def read_items(
    request: Request,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 20
    ):
    # realiza um query que busca todos os livros com os parametros passasados
    return await BooksServices.get_all_with_limit_books_Service(db, skip=skip, limit=limit)


@routes_books.get(
        path="/books/",
        status_code=status.HTTP_200_OK,
        description="Router view all books  in db",
        name="Router get all books",
        response_model=list[Book]
        )
@limiter.limit("20/minute")  # Limite de 20 requisições por minuto
async def read_items(
    request: Request,
    db: AsyncSession = Depends(get_db)
    ):

    # realiza um query para pegar todos os livros da tabela
    return await BooksServices.get_all_books_Service(db)



@routes_books.get(
        path="/books/search-filters/",
        response_model=List[Book],
        status_code=status.HTTP_200_OK,
        description="List search with query books",
        name="Route search with query books"
    )
@limiter.limit("15/minute")  # Limite de 15 requisições por minuto
async def read_books(
    request: Request,
    title: Optional[str] = Query(None, description="Filtrar por título"),
    author: Optional[str] = Query(None, description="Filtrar por autor"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    min_pages: Optional[int] = Query(None, description="Filtrar por número mínimo de páginas"),
    max_pages: Optional[int] = Query(None, description="Filtrar por número máximo de páginas"),
    available: Optional[bool] = Query(None, description="Filtrar por disponibilidade"),
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db) # realiza a conexao com o banco de dados e procura na tebela
    ):

    # realiza a filtragem no services
    return await BooksServices.get_filtered_books_Service(
        db, title=title, author=author,
        category=category, min_pages=min_pages,
        max_pages=max_pages,
        available=available,
        skip=skip,
        limit=limit
        )