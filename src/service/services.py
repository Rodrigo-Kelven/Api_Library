from typing import List, Optional
from src.schemas.books import BookCreate, BookUpdate
from src.config.config_db import get_db, redis_client
from fastapi import Depends, HTTPException, status
from src.models.books import Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import redis.asyncio as aioredis
import json
from fastapi.encoders import jsonable_encoder
from src.config.config import app_logger, db_logger
import time


class BooksServices:


    @staticmethod
    async def create_book_Service(book: BookCreate, db: AsyncSession = Depends(get_db)):
            # Armazena o novo livro no PostGree
            start_time_postgree = time.time() # inicia contagem
            db_item = Book(**book.dict()) # converte o dado enviado para dict
            db.add(db_item)

            try:
                await db.commit()  # await para operações assíncronas
                await db.refresh(db_item)  # await para operações assíncronas

            except Exception as e:
                await db.rollback()  # Reverte as alterações na sessão
                db_logger.error(msg=f"Erro ao registrar livro no PostgreSQL: {str(e)}")
                raise HTTPException(status_code=500, detail="Erro ao registrar livro no banco de dados.")

            end_time_postgree = time.time() # fim da contagem
            execution_time_postgree = end_time_postgree - start_time_postgree
            db_logger.info(msg=f"Tempo de execução em register book in Postgree: {execution_time_postgree} segundos.")
            app_logger.info(msg=f"Tempo de execução em register book in Postgree: {execution_time_postgree} segundos.")

            # Armazena o novo livro no cache Redis
            start_time = time.time()
            book_data = jsonable_encoder(db_item)
            await redis_client.set(f"book:{db_item.id}", json.dumps(book_data), ex=3600)  # Armazena por 1 hora
            end_time = time.time()

            execution_time = end_time - start_time
            db_logger.info(msg=f"Tempo de execução em register book in Redis: {execution_time} segundos.")
            app_logger.info(msg=f"Tempo de execução em register book in Redis: {execution_time} segundos.")
            

            return db_item

    @staticmethod
    async def get_book_Service(book_id: int, db: AsyncSession = Depends(get_db)):
        # Tenta obter o livro do cache Redis
        start_time = time.time()
        cached_book = await redis_client.get(f"book:{book_id}")
        end_time = time.time()

        execution_time = end_time - start_time

        if cached_book:
            db_logger.info(msg=f"Retornado do redis. Tempo de execução: {execution_time} segundos.")
            # Se o livro estiver no cache, retorne-o como um dicionário
            return json.loads(cached_book.decode('utf-8'))  # Decodifica e converte de volta para dicionário

        # Se não estiver no cache, consulta o banco de dados
        db_logger.info(msg="Retornado do Banco de dados.")
        start_time = time.time()
        result = await db.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().first()
        end_time = time.time()

        execution_time = end_time - start_time

        db_logger.info(msg=f"Tempo de execução em get book for ID: {execution_time} segundos.")
        app_logger.info(msg=f"Tempo de execução em get book for ID: {execution_time} segundos.")

        if book is None:
            app_logger.error(msg="Book not found!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")

        # Armazena o livro no cache Redis
        book_data = jsonable_encoder(book)  # Converte o objeto Book em um dicionário
        await redis_client.set(f"book:{book_id}", json.dumps(book_data), ex=3600)  # Armazena por 1 hora        

        return book_data  # Retorna o dicionário


    @staticmethod
    async def update_book_Service(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalars().first()
        db_logger.info(msg=f"Livro de id: {book_id} encontrado!")
        app_logger.info(msg=f"Livro de id: {book_id} encontrado!")
        

        if db_book is None:
            db_logger.error(msg="Book not found!")
            app_logger.error(msg="Book not found!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")
        
        start_time = time.time()
        try:
            # Atualiza os campos do livro
            db_book.title = book.title
            db_book.description = book.description
            db_book.author = book.author
            db_book.category = book.category

            await db.commit()
            await db.refresh(db_book)

        except:
            await db.rollback()  # Reverte as alterações na sessão

        end_time = time.time()
        execution_time = end_time - start_time
        db_logger.info(msg=f"Tempo de execução em update: {execution_time} segundos.")
        app_logger.info(msg=f"Tempo de execução em update: {execution_time} segundos.")

        # Atualiza o livro no cache Redis
        book_data = jsonable_encoder(db_book)
        await redis_client.set(f"book:{book_id}", json.dumps(book_data), ex=3600)  # Armazena por 1 hora
        db_logger.info(msg=f"Livro de id: {book_id} atualizado no Redis!")
        app_logger.info(msg=f"Livro de id: {book_id} atualizado no Redis!")

        return db_book



    @staticmethod
    async def delete_book_Service(book_id: int, db: AsyncSession = Depends(get_db)):
        # Busca o livro pelo ID
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalars().first()

        if db_book is None:
            db_logger.error(msg="Book not found!")
            app_logger.error(msg="Book not found!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!")

        start_time = time.time()

        try:
            await db.delete(db_book)
            await db.commit()
            db_logger.info(msg=f"Livro de id: {book_id} deletado!")
            app_logger.info(msg=f"Livro de id: {book_id} deletado!")
        except Exception as e:
            await db.rollback()  # Reverte as alterações na sessão
            db_logger.error(msg=f"Erro ao deletar livro no PostgreSQL: {str(e)}")
            app_logger.error(msg=f"Erro ao deletar livro no PostgreSQL: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro ao deletar livro no banco de dados.")

        end_time = time.time()
        execution_time = end_time - start_time
        db_logger.info(msg=f"Tempo de execução em delete: {execution_time} segundos.")
        app_logger.info(msg=f"Tempo de execução em delete: {execution_time} segundos.")

        # Remove o livro do cache Redis
        await redis_client.delete(f"book:{book_id}")
        db_logger.info(msg=f"Livro de id: {book_id} deletado do Redis!")
        app_logger.info(msg=f"Livro de id: {book_id} deletado do Redis!")

        return {"detail": "Book deleted!"}
    

    @staticmethod
    async def get_all_with_limit_books_Service(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 20):
        # Executa a consulta para selecionar todos os livros
        #result = await db.execute(select(Book))

        # faz a consulta com base nos limites passados
        consult = select(Book).offset(skip).limit(limit)
        # executa no db a consulta realiza e armazena o resultado
        result = await db.execute(consult)
        start_time = time.time()
        # Verifica se não há livros encontrados
        book = result.scalars().all()

        db_logger.info(msg="Livros retornados!")
        app_logger.info(msg="Livros retornados!")

        end_time = time.time()
        execution_time = end_time - start_time
        print("\n")

        db_logger.info(msg=f"Tempo de execução em busca com limites {skip}/{limit}: {execution_time} segundos.")
        app_logger.info(msg=f"Tempo de execução em busca com limites {skip}/{limit}: {execution_time} segundos.")
        if not book: # Verifica se a lista de livros está vazia
            db_logger.error(msg="Book not found!")
            app_logger.error(msg="Book not found!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No book found")
        return book  # Retorna uma lista de itens
    

    @staticmethod
    async def get_all_books_Service(db: AsyncSession = Depends(get_db)):
        # Executa a consulta para selecionar todos os livros
        start_time = time.time()
        result = await db.execute(select(Book))
        db_logger.info(msg="Livros retornados!")
        app_logger.info(msg="Livros retornados!")

        # Verifica se não há livros encontrados
        book = result.scalars().all()
        end_time = time.time()

        execution_time = end_time - start_time
        db_logger.info(msg=f"Tempo de execução: {execution_time} segundos.")
        app_logger.info(msg=f"Tempo de execução: {execution_time} segundos.")

        if not book: # Verifica se a lista de livros está vazia
            db_logger.error(msg="Book not found!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No book found")
        return book  # Retorna uma lista de itens
    

    @staticmethod
    async def get_filtered_books_Service(
        db: AsyncSession,
        title: Optional[str] = None,
        author: Optional[str] = None,
        category: Optional[str] = None,
        min_pages: Optional[int] = None,
        max_pages: Optional[int] = None,
        available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 10
        ) -> List[Book]:

        # Cria a consulta
        query = select(Book)

        # Aplicar filtros se fornecidos
        if title:
            query = query.where(Book.title.ilike(f"%{title}%"))

        if author:
            query = query.where(Book.author.ilike(f"%{author}%"))

        if category:
            query = query.where(Book.category.ilike(f"%{category}%"))

        if min_pages is not None:
            query = query.where(Book.pages >= min_pages)

        if max_pages is not None:
            query = query.where(Book.pages <= max_pages)

        if available is not None:
            query = query.where(Book.available == available)

        # Executa a consulta
        start_time_postgree = time.time()
        result = await db.execute(query.offset(skip).limit(limit))
        books = result.scalars().all()
        end_time_postgree = time.time()

        execution_time_postgree = end_time_postgree - start_time_postgree
        db_logger.info(msg=f"Tempo de execução em register book in Postgree: {execution_time_postgree} segundos.")
        app_logger.info(msg=f"Tempo de execução em register book in Postgree: {execution_time_postgree} segundos.")

        if not books:  # Verifica se a lista de livros está vazia
            db_logger.error(msg="Book not found!")
            app_logger.error(msg="Book not found!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No book found!")

        return books  # Retorna uma lista de itens
