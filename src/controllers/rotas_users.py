from fastapi import APIRouter, HTTPException, Depends, Query, Body, Path
from sqlmodel import Session, select
from typing import List

from config.config_db import get_session_users # `engine` esteja configurado no arquivo de config
from models.users import User, ResponseUser


rota_users = APIRouter(prefix="/api-library/users")


@rota_users.get("/list",
                status_code=200,
                name="Rota list users",
                summary="Rota list uses",
                description="Esta rota lista todos os usuarios",
                response_model=List[ResponseUser]
                )
async def list_users(session: Session = Depends(get_session_users)):
    statement = select(User)
    users = session.exec(statement).all()
    return users


@rota_users.post("/register-user",
                 status_code=201,
                 name="Rota register user",
                 summary="Rota register user",
                 description="Esta rota cria usuarios",
                response_model=ResponseUser)
async def register_user(*,
                       user: User,
                       session: Session = Depends(get_session_users),
                       ):
    session.add(user)
    session.commit()
    session.refresh(user)

    if user is None:
        raise HTTPException(status_code=404, detail="Erro, user not created :(")
    return user

@rota_users.get("/user/{user_id}",
                status_code=200,
                name="Rota search user with ID",
                summary="Rota search with ID",
                description="Esta rota procura o user por ID",
                response_model=ResponseUser
                )
async def read_user(
    user_id: int = Path(alias="user_id", description="Somente numeros inteiros! -> 0,1,2,3..."),
    session: Session = Depends(get_session_users)
    ):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return user

@rota_users.put("/user/{user_id}",
                status_code=200,
                name="Rota update user with ID",
                summary="Rota update user with ID",
                description="Esta rota atualiza o user por ID",
                response_model=User
                )
async def update_user(
        user_id: int,
        update_user: User,
        session: Session = Depends(get_session_users)
        ):
    statement = select(User).where(User.id == user_id)
    user_update = session.exec(statement).first()

    if user_update is None:
        raise HTTPException(status_code=404, detail="User not found!")
    
    user_update.nome = update_user.nome
    user_update.email == update_user.email
    user_update.username == update_user.username

    session.commit()
    session.refresh(user_update)
    return user_update


@rota_users.delete("/user/delete/{user_id}",
                   status_code=202,
                   name="Rota delete user with ID",
                   summary="Rota delete user with ID",
                   description="Esta rota deleta o user por ID"
                   )
async def delete_user(
    user_id: int = Path(alias="user_id", description="Somente numeros inteiros! -> 0,1,2,3..."),
    session: Session = Depends(get_session_users)
    ):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not Found!")
    
    session.delete(user)
    session.commit()
    message = {
        "Usuario deletado": {
            "Id":f"{user.id}",
            "Nome":f"{user.nome}",
            "Username":f"{user.username}",
            "Password":f"{user.password}"
        }
    }
    return message