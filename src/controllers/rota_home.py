from fastapi import APIRouter, Query, status, Request
from slowapi import Limiter
from src.config.config import limiter


rota_home = APIRouter()


@rota_home.get(
        path="/status",
        status_code=status.HTTP_200_OK,
        name="Rota Home Status",
        summary="Rota Home Status",
        description="Esta rota -> Home, pode ser passada um Query => Opcional!",
        response_description="Response Sucessfull"
        )
@limiter.limit("40/minute")
async def home(
    request: Request,
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


@rota_home.get(
        path="/",
        status_code=status.HTTP_200_OK,
        name="Rota Home",
        summary="Rota Home",
        description="Rota Home somente para testes",
        response_description="Response Sucessfull"
        )
@limiter.limit("40/minute")
async def home(request: Request):
    return  {"Hello":"World"}