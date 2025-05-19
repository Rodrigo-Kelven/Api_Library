from fastapi import Depends, HTTPException, status, Form
from src.auth.schemas.user import Token, User, UserResponse, UserResponseEdit
from src.auth.models.users import UserDB
from src.config.config_db import AsyncSessionLocal
from src.config.config import auth_logger
from sqlalchemy.future import select  # Para consultas assíncronas
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from src.auth.auth import (
    OAuth2PasswordRequestForm,
    authenticate_user_by_email,
    timedelta,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
    get_user,
    get_password_hash,
    check_permissions,
    Role
)


class ServicesAuthUser:


    @staticmethod
    async def login_user_Service(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        async with AsyncSessionLocal() as db:
            # autenticar o usuário usando o e-mail
            # este form_data.username nao recebe o username que foi passado em register, 
            # mas sim o username passado em login !!!!
            user = await authenticate_user_by_email(db, form_data.username, form_data.password)
            if not user:
                auth_logger.warning(msg="Usuario nao encontrado.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.email, "role": user.role}, 
                expires_delta=access_token_expires
            )
            auth_logger.info(msg=f"Usuário {form_data.username} logado com sucesso.")
            return Token(access_token=access_token, token_type="bearer")


    @staticmethod
    async def create_user_Service(
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        password: str = Form(...),
    ):
        # Inicia a sessão com o banco de dados
        async with AsyncSessionLocal() as db:
            try:
                # Verifica se o username já está registrado
                user_with_username = await db.execute(select(UserDB).where(UserDB.username == username))
                if user_with_username.scalars().first():
                    auth_logger.warning(msg="Username já registrado!")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username já registrado!")

                # Verifica se o email já está registrado
                user_with_email = await db.execute(select(UserDB).where(UserDB.email == email))
                if user_with_email.scalars().first():
                    auth_logger.warning(msg="Email já registrado!")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado!")

                # Criação do usuário com senha criptografada
                hashed_password = await get_password_hash(password)
                db_user = UserDB(
                    username=username,
                    email=email,
                    full_name=full_name,
                    hashed_password=hashed_password,
                )
                
                # Adiciona o usuário à sessão do banco
                db.add(db_user)
                await db.commit()  # Commit para persistir a transação
                await db.refresh(db_user)  # Refresh para garantir que o db_user tenha os dados mais recentes
                auth_logger.info(msg=f"Usuario registrado: {username}.")
                return db_user

            except IntegrityError:
                await db.rollback()  # Reverte a transação em caso de erro
                auth_logger.warning(msg="Erro ao criar usuário. Verifique os dados fornecidos.")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar usuário. Verifique os dados fornecidos.")

            # except Exception as e:
            #     # Log de erros gerais e lançamento de exceção
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {str(e)}")
        

    @staticmethod
    async def get_users_Service(current_user: Annotated[User , Depends(get_current_active_user)]):
        check_permissions(current_user, Role.admin)
        async with AsyncSessionLocal() as db:
            users = await db.execute(select(UserDB))
            return [UserResponse(**user.__dict__) for user in users.scalars()]
        

    @staticmethod
    async def update_user_Service(email: str, user: UserResponseEdit, current_user: Annotated[User , Depends(get_current_active_user)]):
        async with AsyncSessionLocal() as db:
            db_user = await get_user(db, email)

            if not db_user:
                auth_logger.error(msg="Usuário não encontrado!")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado!")
            
            for key, value in user.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            
            await db.commit()
            await db.refresh(db_user)
            auth_logger.info(msg=f"Usuário {user.username} atualizado!")
            return db_user
        

    @staticmethod
    async def delete_account_Service(current_user: Annotated[User  , Depends(get_current_active_user)]):
        async with AsyncSessionLocal() as db:
            db_user = await get_user(db, current_user.email)

            if not db_user:
                auth_logger.error(msg="Usuário não encontrado!")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado!")
            
            await db.delete(db_user)
            await db.commit()
            auth_logger.info(msg=f"Usuário {current_user.username} deletado com sucesso!")
            return {"detail": f"Usuário {current_user.username} deletado com sucesso."}