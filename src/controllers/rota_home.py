from fastapi import APIRouter, Query, status

rota_home = APIRouter()

@rota_home.get(
        path="/status",
        status_code=status.HTTP_200_OK,
        name="Rota Home",
        summary="Rota Home",
        description="Esta rota -> Home, pode ser passada um Query => Opcional!",
        response_description="Response"
        )
async def home(
    name: str = Query(
        default=None,
        alias="Nome",
        title="name",
        description="Insira um nome -> Opcional",
        max_length=10
        )
    ):

    if name:
        return  {"Hello":f"{name.capitalize().strip()}"}
    return  {"Hello":"World"}