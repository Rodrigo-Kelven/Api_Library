from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import redis.asyncio as aioredis



# URL do banco de dados PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/fastapi_db"

# Criação do engine assíncrono
engine_books = create_async_engine(DATABASE_URL, echo=True)

# Criação da sessão assíncrona
AsyncSessionLocal = sessionmaker(bind=engine_books, class_=AsyncSession, expire_on_commit=False)

Base_books = declarative_base()

# Função para obter a sessão do banco de dados
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Configuração do Redis
REDIS_URL = "redis://localhost:6379"  # URL do Redis
redis_client = aioredis.from_url(REDIS_URL)