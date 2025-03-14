from fastapi import FastAPI
from config.config_db import Base, engine
from controllers.all_routes import all_routes

import os

# Crie o diretório Banco se não existir
if not os.path.exists('./Banco_de_Dados'):
    os.makedirs('./Banco_de_Dados')


app = FastAPI()


all_routes(app)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Se tiver um evento de shutdown, adicione aqui também
@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()
