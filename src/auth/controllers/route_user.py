from fastapi import APIRouter, Depends, HTTPException, status, Form, BackgroundTasks
from auth.schemas.user import Token, User, UserResponse, UserResponseCreate, UserResponseEdit
from config.config_db import AsyncSessionLocal
from auth.models.users import UserDB
from typing import List, Annotated
from auth.auth import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # Para consultas assíncronas


routes_auth_auten = APIRouter(prefix="/api-auten_auth")

# Rota de login
@routes_auth_auten.post(
    path="/login",
    response_description="Informations of login",
    description="Route login user",
    name="Route login user"
)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    async with AsyncSessionLocal() as db:
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role}, 
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

# Rota para obter informações do usuário autenticado
@routes_auth_auten.get(
    path="/users/me/",
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
    response_description="Informations items user",
    description="Route get items user",
    name="Route get items user"
)
async def read_own_items(current_user: Annotated[User , Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]

# Rota para criar um novo usuário
@routes_auth_auten.post(
    path="/users/",
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
    async with AsyncSessionLocal() as db:
        if await get_user(db, username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já registrado!")

        hashed_password = await get_password_hash(password)
        db_user = UserDB(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

# Rota para listar todos os usuários (somente admin)
@routes_auth_auten.get(
    path="/users/",
    response_model=List[UserResponse],
    response_description="Users",
    description="Route list users",
    name="Route list users"
)
async def get_users(current_user: Annotated[User , Depends(get_current_active_user)]):
    check_permissions(current_user, Role.admin)
    async with AsyncSessionLocal() as db:
        users = await db.execute(select(UserDB))
        return [UserResponse(**user.__dict__) for user in users.scalars()]

# Rota para atualizar informações do usuário
@routes_auth_auten.put(
    path="/users/{username}",
    response_model=UserResponse,
    response_description="Update informations user",
    description="Route update informations user",
    name="Route update user"
)
async def update_user(username: str, user: UserResponseEdit, current_user: Annotated[User , Depends(get_current_active_user)]):
    async with AsyncSessionLocal() as db:
        db_user = await get_user(db, username)

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado!")
        
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        
        await db.commit()
        await db.refresh(db_user)
        return db_user

# Rota para deletar a conta do usuário
@routes_auth_auten.delete(
 path="/users/delete-account-me/",
    response_description="Informations delete account",
    name="Route delete user"
)
async def delete_user(current_user: Annotated[User  , Depends(get_current_active_user)]):
    async with AsyncSessionLocal() as db:
        db_user = await get_user(db, current_user.username)

        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado!")
        
        await db.delete(db_user)
        await db.commit()
        return {"detail": f"Usuário {current_user.username} deletado com sucesso"}

# Função para enviar notificação por email
async def write_notification(email: str, message=""):
    with open("log.txt", mode="a") as email_file:
        content = f"notification for {email}: {message}\n"
        email_file.write(content)

@routes_auth_auten.post(
    "/send-notification/{email}",
    response_description="Send message email",
    description="Route send message email",
    name="Route send message email"
)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}