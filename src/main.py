from fastapi import FastAPI
from config.config_db import Base_books, engine_books
from controllers.all_routes import all_routes
from auth.auth import LogRequestMiddleware, ExceptionHandlingMiddleware
from auth.config.config import config_CORS_auth
from auth.config.config_db import Base_auth, engine_auth
from config.config import config_CORS


app = FastAPI()


all_routes(app)


@app.on_event("startup")
async def startup_event():
    try:
        async with engine_auth.begin() as conn:
            await conn.run_sync(Base_auth.metadata.create_all)  # Cria as tabelas no banco de dados de usuários

        async with engine_books.begin() as conn:
            await conn.run_sync(Base_books.metadata.create_all)  # Cria as tabelas no banco de dados de livros
    except Exception as e:
        print(f"Erro ao criar tabelas: {str(e)}")


# Se tiver um evento de shutdown, adicione aqui também
@app.on_event("shutdown")
async def shutdown_event():
    await engine_books.dispose()
    await engine_auth.dispose()


# Adiciona o middleware ao FastAPI
app.add_middleware(LogRequestMiddleware)

# Adiciona o middleware de tratamento de exceções
app.add_middleware(ExceptionHandlingMiddleware)

config_CORS_auth(app)
config_CORS(app)
