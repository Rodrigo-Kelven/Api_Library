from controllers.rota_home import rota_home
from controllers.rotas_books import routes_books
from auth.controllers.route_user import routes_auth_auten

from enum import Enum


# class para organizar Tags
class Tags(Enum):
    Home = "Home"
    Books = "Books"
    User = "string"


# funcao para armazenar todas as rotas em um unico lugar
def all_routes(app):
    app.include_router(rota_home, tags=[Tags.Home])
    app.include_router(routes_books, tags=[Tags.Books])
    app.include_router(routes_auth_auten, tags=[Tags.User])
   