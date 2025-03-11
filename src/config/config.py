#configuracoes
from config.config_db import create_db_and_tables_of_books, create_db_and_tables_of_users


print("\n")
create_db_and_tables_of_users()
print("############### Banco de dados de users criado com Sucesso! ###############")
create_db_and_tables_of_books()
print("############### Banco de dados de books criado com Sucesso! ###############")
print("\n")