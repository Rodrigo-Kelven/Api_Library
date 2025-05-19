from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import RotatingFileHandler
import logging
import os


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
        #allow_origins=origins,
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
db_logger = setup_logger("db_logger", "logs/db.log", logging.ERROR)