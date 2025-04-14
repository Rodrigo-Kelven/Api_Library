from fastapi import FastAPI
from src.config.config_db import Base_books, engine_books
from src.controllers.all_routes import all_routes
from src.auth.auth import LogRequestMiddleware, ExceptionHandlingMiddleware
from src.auth.config.config import config_CORS_auth
from src.auth.config.config_db import Base_auth, engine_auth
from src.config.config import config_CORS


app = FastAPI(
    title="API Library with FastAPI",
    debug=True,
    summary="Api Library",
    version="0.1.6",
    description="A Api Library é uma API Library projetada para facilitar a integração de diferentes serviços e plataformas," \
    "permitindo que desenvolvedores criem soluções robustas e escaláveis. Com uma arquitetura modular e flexível," \
    "a Api Library oferece uma ampla gama de funcionalidades para gerenciar dados, realizar autenticação, processar pagamentos e muito mais."
)


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



