from fastapi import FastAPI

#configuracoes
from config.config import create_db_and_tables_of_books, create_db_and_tables_of_users

#rotas importadas
from controllers.rota_home import rota_home
from controllers.rotas_books import rota_books
from controllers.rotas_users import rota_users

app = FastAPI()

# criando o banco de dados de books e users
create_db_and_tables_of_books()
app.include_router(rota_home)
app.include_router(rota_books)
app.include_router(rota_users)

print("\n")
print("############### Banco de dados de users criado com Sucesso! ###############")
create_db_and_tables_of_users()
print("############### Banco de dados de books criado com Sucesso! ###############")
print("\n")