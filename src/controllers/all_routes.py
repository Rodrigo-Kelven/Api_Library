from controllers.rota_home import rota_home
from controllers.rotas_books import rota_books
from controllers.rotas_users import rota_users
from enum import Enum


# class para organizar Tags
class Tags(Enum):
    Home = "Home"
    Books = "Books"
    User = "User"


# funcao para armazenar todas as rotas em um unico lugar
def all_routes(app):
    app.include_router(rota_home, tags=[Tags.Home])
    app.include_router(rota_books, tags=[Tags.Books])
    app.include_router(rota_users, tags=[[Tags.User]])