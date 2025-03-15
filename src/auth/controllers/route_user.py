from fastapi import APIRouter, Depends, status, Form
from src.auth.schemas.user import Token, User, UserResponse, UserResponseCreate, UserResponseEdit
from src.config.config_db import AsyncSessionLocal
from typing import List, Annotated
from src.auth.auth import *
from src.auth.services.services import ServicesAuthUser


routes_auth_auten = APIRouter()


# Rota de login
@routes_auth_auten.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_description="Informations of login",
    description="Route login user",
    name="Route login user"
)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await ServicesAuthUser.login_user(form_data)


# Rota para obter informações do usuário autenticado
@routes_auth_auten.get(
    path="/users/me/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponse,
    response_description="Informations user",
    description="Route get informations user",
    name="Route get informations user"
)
async def read_users_me(current_user: Annotated[User , Depends(get_current_active_user)]):
    check_permissions(current_user, Role.user)
    return current_user

# Rota para obter itens do usuário autenticado
@routes_auth_auten.get(
    path="/users/me/items/",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Informations items user",
    description="Route get items user",
    name="Route get items user"
)
async def read_own_items(current_user: Annotated[User , Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]

# Rota para criar um novo usuário
@routes_auth_auten.post(
    path="/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseCreate,
    response_description="Create user",
    description="Route create user",
    name="Route create user"
)
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
):
    return await ServicesAuthUser.create_user(username, email, full_name, password)


# Rota para listar todos os usuários (somente admin)
@routes_auth_auten.get(
    path="/users/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=List[UserResponse],
    response_description="Users",
    description="Route list users",
    name="Route list users"
)
async def get_users(current_user: Annotated[User , Depends(get_current_active_user)]):
    return await ServicesAuthUser.get_users(current_user)

# Rota para atualizar informações do usuário
@routes_auth_auten.put(
    path="/users/{username}",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    response_description="Update informations user",
    description="Route update informations user",
    name="Route update user"
)
async def update_user(username: str, user: UserResponseEdit, current_user: Annotated[User , Depends(get_current_active_user)]):
    return await ServicesAuthUser.update_user(username, user, current_user)

# Rota para deletar a conta do usuário
@routes_auth_auten.delete(
    path="/users/delete-account-me/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Informations delete account",
    name="Route delete user"
)
async def delete_user(current_user: Annotated[User  , Depends(get_current_active_user)]):
    return await ServicesAuthUser.delete_account(current_user)
