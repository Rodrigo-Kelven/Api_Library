from fastapi.middleware.cors import CORSMiddleware
import logging


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
        allow_origins=origins,
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


import logging

# Diretório dos logs
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# Handler para logs de INFO
info_handler = logging.FileHandler("logs/info.log")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(log_format))

# Handler para logs de WARNING
warning_handler = logging.FileHandler("logs/warning.log")
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(logging.Formatter(log_format))

# Handler para logs de ERROR
error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(log_format))

# Console handler opcional
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format))

# Logger principal
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # Nível mínimo para o logger aceitar

# Adiciona todos os handlers ao logger
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


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

from logging.handlers import RotatingFileHandler
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