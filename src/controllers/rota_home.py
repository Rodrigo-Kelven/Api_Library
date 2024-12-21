from fastapi import APIRouter, Query

rota_home = APIRouter()

@rota_home.get("/",
               status_code=200,
               name="Rota Home",
               summary="Rota Home",
               description="Esta rota -> Home, pode ser passada um Query => Opcional!",
               response_description="Response"
               )
async def home(
    name: str = Query(default=None, alias="Nome", title="name", description="Insira um nome -> Opcional", max_length=10)):

    if name:
        return {"Hello":f"{name.capitalize().strip()}"}
    return {"Hello":"World"}