from src.schemas.books import  BookCreate, BookUpdate
from src.config.config_db import get_db
from fastapi import Depends, HTTPException, status
from src.models.books import Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Para consultas assíncronas



class BooksServices:

    # funcao para pegar sessao do banco de dados
    get_db()

    @staticmethod
    async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
        db_item = Book(**book.dict())
        db.add(db_item)
        await db.commit()  # Use await para operações assíncronas
        await db.refresh(db_item)  # Use await para operações assíncronas       
        return db_item
    

    @staticmethod
    async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().first()
        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
        return book
    

    @staticmethod
    async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalars().first()
        if db_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
        
        db_book.title = book.title
        db_book.description = book.description
        db_book.author = book.author
        db_book.category = book.category
        await db.commit()
        await db.refresh(db_book)
        return db_book
    

    @staticmethod
    async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalars().first()
        if db_book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
        
        await db.delete(db_book)
        await db.commit()
        return {"detail": "Book deleted!"}
    

    @staticmethod
    async def get_all_books(db: AsyncSession = Depends(get_db)):
        # Executa a consulta para selecionar todos os livros
        result = await db.execute(select(Book))  

        # Verifica se não há livros encontrados
        book = result.scalars().all()
        if not book: # Verifica se a lista de livros está vazia
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No book found")
        return book  # Retorna uma lista de itens
