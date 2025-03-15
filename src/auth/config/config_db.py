from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base



# Base para os modelos
Base_auth = declarative_base()

# URL do banco de dados SQLite
DATABASE_URL = "sqlite+aiosqlite:///./Banco_de_Dados/Users_db.db"  # Usando aiosqlite para SQLite

# Criação do engine assíncrono
engine_auth = create_async_engine(DATABASE_URL, echo=True)

# Criação do gerenciador de sessões assíncronas
AsyncSessionLocal = sessionmaker(bind=engine_auth, class_=AsyncSession, expire_on_commit=False)


async def get_user_db():
    async with AsyncSessionLocal() as session:
        yield session