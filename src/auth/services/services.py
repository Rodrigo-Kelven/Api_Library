from fastapi import Depends, HTTPException, status, Form
from src.auth.schemas.user import Token, User, UserResponse, UserResponseEdit
from src.auth.models.users import UserDB
from src.config.config_db import AsyncSessionLocal
from sqlalchemy.future import select  # Para consultas assíncronas
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from src.auth.auth import *


class ServicesAuthUser:


    @staticmethod
    async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        async with AsyncSessionLocal() as db:
            # autenticar o usuário usando o e-mail
            user = await authenticate_user_by_email(db, form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "role": user.role}, 
                expires_delta=access_token_expires
            )
            return Token(access_token=access_token, token_type="bearer")


    @staticmethod
    async def create_user(
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        password: str = Form(...),
        ):
        async with AsyncSessionLocal() as db:
            # Verifica se o username já está registrado
            if await get_user(db, username):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já registrado!")

            # Verifica se o email já está registrado
            result = await db.execute(select(UserDB).where(UserDB.email == email))
            if result.scalars().first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado!")

            hashed_password = await get_password_hash(password)
            db_user = UserDB(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=hashed_password,
            )
            db.add(db_user)
            try:
                await db.commit()
                await db.refresh(db_user)
            except IntegrityError:
                await db.rollback()  # Reverte a transação em caso de erro
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar usuário. Verifique os dados fornecidos.")

            return db_user
        

    @staticmethod
    async def get_users(current_user: Annotated[User , Depends(get_current_active_user)]):
        check_permissions(current_user, Role.admin)
        async with AsyncSessionLocal() as db:
            users = await db.execute(select(UserDB))
            return [UserResponse(**user.__dict__) for user in users.scalars()]
        

    @staticmethod
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
        

    @staticmethod
    async def delete_account(current_user: Annotated[User  , Depends(get_current_active_user)]):
        async with AsyncSessionLocal() as db:
            db_user = await get_user(db, current_user.email)

            if not db_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado!")
            
            await db.delete(db_user)
            await db.commit()
            return {"detail": f"Usuário {current_user.username} deletado com sucesso"}