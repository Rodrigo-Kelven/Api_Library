from schemas.books import  BookCreate
from config.config_db import get_db
from fastapi import Depends, HTTPException
from models.books import Book
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
    async def get_book(item_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == item_id))
        item = result.scalars().first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    

    @staticmethod
    async def update_book(item_id: int, item: BookCreate, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == item_id))
        db_item = result.scalars().first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        db_item.name = item.name
        db_item.description = item.description
        await db.commit()
        await db.refresh(db_item)
        return db_item
    

    @staticmethod
    async def delete_book(item_id: int, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == item_id))
        db_item = result.scalars().first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        await db.delete(db_item)
        await db.commit()
        return {"detail": "Item deleted"}
    

    @staticmethod
    async def get_all_books(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book))  # Consulta todos os itens
        return result.scalars().all()  # Retorna uma lista de itens
