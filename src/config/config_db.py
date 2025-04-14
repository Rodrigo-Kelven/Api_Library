from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import redis.asyncio as aioredis


Base_books = declarative_base()

# Use aiosqlite para SQLite
DATABASE_URL = "sqlite+aiosqlite:///./Banco_de_Dados/books_db.db" 

# Criação do engine assíncrono
engine_books = create_async_engine(DATABASE_URL, echo=True)

# Criação da sessão assíncrona
AsyncSessionLocal = sessionmaker(bind=engine_books, class_=AsyncSession, expire_on_commit=False)

# Função para obter a sessão do banco de dados
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Configuração do Redis
REDIS_URL = "redis://localhost:6379"  # URL do Redis
redis_client = aioredis.from_url(REDIS_URL) 
