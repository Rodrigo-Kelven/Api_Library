from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from logging.handlers import RotatingFileHandler
import logging
import os
from slowapi import Limiter
from slowapi.util import get_remote_address



# rate limit configurado, caso altere algo, documente.
def rate_limit_Service(app):

    # Manipulador de Exceções para Rate Limit Exceeded
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        # Verificando se o atributo 'headers' existe
        headers = getattr(exc, 'headers', None)
        
        # Se headers existir, tenta pegar o 'Retry-After'
        if headers:
            retry_after = headers.get("Retry-After")
        else:
            retry_after = None
        
        # Caso o 'Retry-After' não esteja disponível, define o tempo de espera padrão
        if retry_after:
            wait_time = int(retry_after)
        else:
            wait_time = 60  # Tempo de espera padrão em segundos

        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Limite de requisições excedido. Tente novamente em {wait_time} segundos."
            },
            headers={"Retry-After": str(wait_time)},
        )




# CORS configurado, caso tenha mais implementacoes, documente!
def config_CORS(app):

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost:5173/", # react
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["X-Custom-Header"],
        max_age=3600,
    )
"""
Ao permitir todas as origens (allow_origins=["*"]), você deve ter cuidado,
pois isso pode expor sua API a riscos de segurança.
É sempre melhor restringir as origens permitidas ao mínimo necessário
"""


"""
### Resumo visual
### Nível configurado	Logs que ele aceita
-----------------------------------------------
* DEBUG	    DEBUG, INFO, WARNING, ERROR, CRITICAL
* INFO	    INFO, WARNING, ERROR, CRITICAL
* WARNING	WARNING, ERROR, CRITICAL
* ERROR	    ERROR, CRITICAL
* CRITICAL	CRITICAL
"""

os.makedirs("logs", exist_ok=True)
# Formato padrão
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Cria e retorna um logger com arquivo próprio."""
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False  # Evita que os logs se repitam no console

    return logger

# Loggers separados
app_logger = setup_logger("app_logger", "logs/app.log", logging.INFO)
auth_logger = setup_logger("auth_logger", "logs/auth.log", logging.INFO)
#db_logger = setup_logger("db_logger", "logs/db.log", logging.ERROR)
db_logger = setup_logger("db_logger", "logs/db.log", logging.INFO)



# Configurar o log de Request e Response
logging.basicConfig(level=logging.INFO)


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Requisição recebida: {request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Resposta enviada com status {response.status_code}")
        return response


# decoracor do rate limit de auth
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"],
    storage_uri="redis://my-redis:6379/2",
    )