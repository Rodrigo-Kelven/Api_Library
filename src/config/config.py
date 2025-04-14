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


# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,  # Define o nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato da mensagem de log
    handlers=[
        logging.StreamHandler(),  # Envia logs para o console
        logging.FileHandler("app.log")  # Envia logs para um arquivo
    ]
)

logger = logging.getLogger(__name__)  # Cria um logger para o módulo atual
