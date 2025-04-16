from fastapi import FastAPI, Request
from src.config.config_db import Base_books, engine_books
from src.controllers.all_routes import all_routes
from src.auth.auth import ExceptionHandlingMiddleware
from src.config.config import LogRequestMiddleware
from src.auth.config.config import config_CORS_auth
from src.auth.config.config_db import engine_auth, Base_auth
from src.config.config import config_CORS, rate_limit_Service, db_logger


app = FastAPI(
    title="API Library with FastAPI",
    debug=True,
    summary="Api Library",
    version="1.1.12",
    description="A Api Library é uma API Library projetada para facilitar a integração de diferentes serviços e plataformas," \
                "permitindo que desenvolvedores criem soluções robustas e escaláveis. Com uma arquitetura modular e flexível," \
                "a Api Library oferece uma ampla gama de funcionalidades para gerenciar dados, realizar autenticação, processar pagamentos e muito mais."
)

# Adiciona as rotas
all_routes(app)
@app.on_event("startup")
async def startup_event():
    try:
        # Criação das tabelas no banco de dados de usuários
        async with engine_auth.begin() as conn:
            await conn.run_sync(Base_auth.metadata.create_all)
            db_logger.info("Tabela UserDB criada com sucesso.")

        # Criação das tabelas no banco de dados de livros
        async with engine_books.begin() as conn:
            await conn.run_sync(Base_books.metadata.create_all)
            db_logger.info("Tabela BooksDB criada com sucesso.")

    except Exception as e:
        db_logger.error(f"Erro ao criar tabelas: {str(e)}.")


@app.on_event("shutdown")
async def shutdown_event():
    await engine_books.dispose()
    await engine_auth.dispose()
    db_logger.info("Conexões com os bancos de dados encerradas.")

# Adiciona o middleware ao FastAPI
app.add_middleware(LogRequestMiddleware)

# Adiciona o middleware de tratamento de exceções
app.add_middleware(ExceptionHandlingMiddleware)

# Configuração de CORS
config_CORS_auth(app)
config_CORS(app)
# configuracao do rate limit
rate_limit_Service(app)


